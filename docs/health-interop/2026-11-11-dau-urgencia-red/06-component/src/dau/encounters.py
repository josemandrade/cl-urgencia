"""Encuentro de urgencia (DAUEncuentroUrgencia y variantes alta/abandono).

Un solo Encounter por episodio, actualizado por PUT condicional por ID
DAU. Admisión: status ``arrived``; alta: status ``finished`` con
``dischargeDisposition`` 01–06 y diagnóstico de egreso (use DD);
abandono: status ``finished`` con la extensión tipoAbandono (1 NEA /
2 fuga), sin dischargeDisposition ni destino.

Referencias lógicas (``Patient/ejemplo-paciente``, ...): el ensamblador
de Bundle las reescribe a los ``fullUrl urn:uuid:`` (Task 10).
"""

from datetime import datetime

from .constants import (
    DESTINO_ALTA,
    DESTINO_ALTA_SYSTEM,
    PROFILE_BASE,
    TIPO_ABANDONO,
    TIPO_ABANDONO_SYSTEM,
)
from .identifiers import dau_system
from .validate import (
    check_coding,
    check_coding_direct,
    check_profile,
    check_reference,
    check_resource_type,
    first_coding,
)

PROFILE_ADMISSION = "dau-encuentro-urgencia"
PROFILE_DISCHARGE = "dau-encuentro-urgencia-alta"
PROFILE_ABANDONMENT = "dau-encuentro-urgencia-abandono"

ACT_CODE_SYSTEM = "http://terminology.hl7.org/CodeSystem/v3-ActCode"
PARTICIPATION_SYSTEM = (
    "http://terminology.hl7.org/CodeSystem/v3-ParticipationType"
)
DIAGNOSIS_ROLE_SYSTEM = (
    "http://terminology.hl7.org/CodeSystem/diagnosis-role"
)
REASON_MAX_LENGTH = 200
DESTINO_NEEDS_DESTINATION = {"01", "02", "04"}


def _participant(code, display, practitioner, period_start=None):
    participant = {
        "type": [
            {
                "coding": [
                    {
                        "code": code,
                        "system": PARTICIPATION_SYSTEM,
                        "display": display,
                    }
                ]
            }
        ],
        "individual": {"reference": practitioner},
    }
    if period_start is not None:
        participant["period"] = {"start": period_start}
    return participant


def _base_encounter(data, profile_id, status):
    dau_id = data.get("dau_id")
    deis_code = data.get("deis_code")
    if not dau_id:
        raise ValueError("se requiere dau_id")
    if not deis_code:
        raise ValueError("se requiere deis_code")
    if not data.get("period_start"):
        raise ValueError("se requiere period_start")
    if not data.get("patient"):
        raise ValueError("se requiere patient")
    if not data.get("provider"):
        raise ValueError("se requiere provider")
    if not data.get("practitioner"):
        raise ValueError("se requiere practitioner")
    encounter = {
        "resourceType": "Encounter",
        "meta": {"profile": [PROFILE_BASE + profile_id]},
        "status": status,
        "class": {
            "code": "EMER",
            "system": ACT_CODE_SYSTEM,
            "display": "Emergencia",
        },
        "identifier": [
            {"system": dau_system(deis_code), "value": dau_id}
        ],
        "subject": {"reference": data["patient"]},
        "serviceProvider": {"reference": data["provider"]},
        "period": {"start": data["period_start"]},
    }
    if data.get("attender_start"):
        encounter["participant"] = [
            _participant(
                "ATND", "atendiente", data["practitioner"],
                data["attender_start"],
            )
        ]
    if data.get("reason"):
        encounter["reasonCode"] = [{"text": data["reason"]}]
    return encounter


def build_admission_encounter(data):
    """Construye el Encounter de admisión (status ``arrived``)."""
    return _base_encounter(data, PROFILE_ADMISSION, "arrived")


def build_discharge_encounter(data):
    """Construye el Encounter de alta (status ``finished``).

    Entrada: como la admisión, más ``period_end``, ``destino`` (01–06) y
    ``diagnosis_condition`` (referencia al Condition de egreso).
    ``destination`` (referencia a Organization) es obligatoria cuando el
    destino es 01, 02 o 04 (invariante dau-alta-destino).
    """
    destino = data.get("destino")
    if destino not in DESTINO_ALTA:
        raise ValueError(
            "destino debe ser uno de %s" % sorted(DESTINO_ALTA)
        )
    if not data.get("period_end"):
        raise ValueError("se requiere period_end")
    if not data.get("diagnosis_condition"):
        raise ValueError("se requiere diagnosis_condition")
    encounter = _base_encounter(data, PROFILE_DISCHARGE, "finished")
    encounter["diagnosis"] = [
        {
            "use": {
                "coding": [
                    {
                        "code": "DD",
                        "system": DIAGNOSIS_ROLE_SYSTEM,
                        "display": "Diagnóstico de egreso",
                    }
                ]
            },
            "condition": {"reference": data["diagnosis_condition"]},
        }
    ]
    # El participante DIS (quien da el alta) va tras el ATND.
    encounter.setdefault("participant", []).append(
        _participant("DIS", "quien da el alta", data["practitioner"])
    )
    encounter["period"]["end"] = data["period_end"]
    encounter["hospitalization"] = {
        "dischargeDisposition": {
            "coding": [
                {
                    "code": destino,
                    "system": DESTINO_ALTA_SYSTEM,
                    "display": DESTINO_ALTA[destino],
                }
            ]
        }
    }
    if data.get("destination"):
        encounter["hospitalization"]["destination"] = {
            "reference": data["destination"]
        }
    return encounter


def build_abandonment_encounter(data):
    """Construye el Encounter de abandono (status ``finished``).

    Entrada: como la admisión, más ``period_end``, ``tipo`` (1 NEA /
    2 fuga) y ``diagnosis_condition`` (referencia a la hipótesis;
    sin ``use``). Sin dischargeDisposition ni destination.
    """
    tipo = data.get("tipo")
    if tipo not in TIPO_ABANDONO:
        raise ValueError(
            "tipo debe ser uno de %s" % sorted(TIPO_ABANDONO)
        )
    if not data.get("period_end"):
        raise ValueError("se requiere period_end")
    encounter = _base_encounter(data, PROFILE_ABANDONMENT, "finished")
    encounter["extension"] = [
        {
            "url": PROFILE_BASE + "dau-tipo-abandono",
            "valueCodeableConcept": {
                "coding": [
                    {
                        "code": tipo,
                        "system": TIPO_ABANDONO_SYSTEM,
                        "display": TIPO_ABANDONO[tipo],
                    }
                ]
            },
        }
    ]
    encounter["period"]["end"] = data["period_end"]
    if data.get("diagnosis_condition"):
        encounter["diagnosis"] = [
            {"condition": {"reference": data["diagnosis_condition"]}}
        ]
    return encounter


def _parse_datetime(value):
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def _variant(resource):
    profiles = resource.get("meta", {}).get("profile", [])
    for profile_id in (
        PROFILE_DISCHARGE,
        PROFILE_ABANDONMENT,
        PROFILE_ADMISSION,
    ):
        if PROFILE_BASE + profile_id in profiles:
            return profile_id
    return None


def validate_encounter(resource):
    """Errores del Encounter contra su perfil DAU; [] = válido.

    Comprueba los campos base, la variante (alta/abandono) según
    ``meta.profile`` y los invariantes dau-enc-period, dau-enc-reason
    y dau-alta-destino.
    """
    errors = []
    check_resource_type(resource, "Encounter", errors)
    variant = _variant(resource)
    if variant is None:
        errors.append(
            "meta.profile debe ser un perfil DAUEncuentroUrgencia"
        )
        variant = PROFILE_ADMISSION
    else:
        check_profile(resource, variant, errors)

    identifiers = resource.get("identifier")
    if not isinstance(identifiers, list) or not identifiers:
        errors.append("identifier 1..*: falta identifier")
    else:
        for ident in identifiers:
            system = ident.get("system", "")
            if "/fhir/sid/dau/" not in system:
                errors.append(
                    "identifier.system debe ser el sistema del ID DAU"
                )
            if not ident.get("value"):
                errors.append("identifier.value 1..1: falta value")

    if resource.get("status") not in (
        "arrived",
        "finished",
        "entered-in-error",
    ):
        errors.append("status 1..1: debe ser arrived, finished o "
                      "entered-in-error")
    check_coding_direct(
        resource.get("class"), ACT_CODE_SYSTEM, {"EMER"}, "class", errors
    )
    check_reference(resource.get("subject"), "subject", errors)
    check_reference(
        resource.get("serviceProvider"), "serviceProvider", errors
    )

    participants = resource.get("participant", [])
    atnd = [
        p for p in participants
        if first_coding(p.get("type", {})) is not None
        and first_coding(p.get("type", {})).get("code") == "ATND"
    ]
    if len(atnd) > 1:
        errors.append("participant[atnd] 0..1: más de un ATND")
    for part in atnd:
        if not part.get("period", {}).get("start"):
            errors.append(
                "participant[atnd].period.start 1..1: falta start"
            )
        check_reference(part.get("individual"),
                        "participant[atnd].individual", errors)

    period = resource.get("period")
    if not isinstance(period, dict) or not period.get("start"):
        errors.append("period.start 1..1: falta start")
    elif period.get("end"):
        # Invariante dau-enc-period.
        start = _parse_datetime(period["start"])
        end = _parse_datetime(period["end"])
        if start is not None and end is not None and end < start:
            errors.append(
                "dau-enc-period: period.end anterior a period.start"
            )
        elif start is None or end is None \
                and period["end"] < period["start"]:
            errors.append(
                "dau-enc-period: period.end anterior a period.start"
            )

    reason_codes = resource.get("reasonCode", [])
    for reason in reason_codes:
        text = reason.get("text", "")
        # Invariante dau-enc-reason.
        if not text:
            errors.append("reasonCode.text 1..1: falta text")
        elif len(text) > REASON_MAX_LENGTH:
            errors.append(
                "dau-enc-reason: reasonCode.text supera 200 caracteres"
            )

    hospitalization = resource.get("hospitalization", {})
    discharge = hospitalization.get("dischargeDisposition")
    destination = hospitalization.get("destination")
    diagnoses = resource.get("diagnosis", [])

    if variant == PROFILE_DISCHARGE:
        if resource.get("status") != "finished":
            errors.append("alta: status debe ser finished")
        if not period or not period.get("end"):
            errors.append("alta: period.end 1..1: falta end")
        if discharge is None:
            errors.append(
                "alta: hospitalization.dischargeDisposition 1..1: falta"
            )
        else:
            check_coding(
                discharge, DESTINO_ALTA_SYSTEM, set(DESTINO_ALTA),
                "hospitalization.dischargeDisposition", errors,
            )
            # Invariante dau-alta-destino.
            code = first_coding(discharge)
            if code is not None and code.get("code") in \
                    DESTINO_NEEDS_DESTINATION and destination is None:
                errors.append(
                    "dau-alta-destino: destino %s exige destination"
                    % code.get("code")
                )
        if not diagnoses:
            errors.append("alta: diagnosis 1..*: falta diagnosis")
        for diag in diagnoses:
            use = first_coding(diag.get("use", {}))
            if use is None or use.get("code") != "DD":
                errors.append(
                    "alta: diagnosis.use debe ser DD "
                    "(diagnóstico de egreso)"
                )
            check_reference(
                diag.get("condition"), "diagnosis.condition", errors
            )
    elif variant == PROFILE_ABANDONMENT:
        if resource.get("status") != "finished":
            errors.append("abandono: status debe ser finished")
        if not period or not period.get("end"):
            errors.append("abandono: period.end 1..1: falta end")
        extensions = [
            e for e in resource.get("extension", [])
            if e.get("url") == PROFILE_BASE + "dau-tipo-abandono"
        ]
        if len(extensions) != 1:
            errors.append(
                "abandono: extension tipoAbandono 1..1: debe haber una"
            )
        else:
            check_coding(
                extensions[0].get("valueCodeableConcept"),
                TIPO_ABANDONO_SYSTEM, set(TIPO_ABANDONO),
                "extension tipoAbandono", errors,
            )
        if discharge is not None:
            errors.append(
                "abandono: hospitalization.dischargeDisposition 0..0"
            )
        if destination is not None:
            errors.append(
                "abandono: hospitalization.destination 0..0"
            )
        for diag in diagnoses:
            if "use" in diag:
                errors.append("abandono: diagnosis.use 0..0")
            check_reference(
                diag.get("condition"), "diagnosis.condition", errors
            )
    else:  # admisión
        if resource.get("status") == "finished":
            errors.append(
                "admisión: status finished usa la variante alta/abandono"
            )
    return errors
