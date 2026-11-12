"""Diagnóstico de urgencia (perfil DAUDiagnosticoUrgencia).

Hipótesis (verificationStatus = provisional) o diagnóstico de egreso
(verificationStatus = confirmed). El código es CIE-10 (preferente),
SNOMED CT o solo texto; TAPSA no se acepta.

Acepta ``local_id``: el PUT condicional del Bundle exige un
``identifier`` local del HIS (Ruling Task 7/8/9), con el sistema de la
guía y valor ``<DAU>-1``.
"""

from .constants import (
    ICD10_SYSTEM,
    LOCAL_ID_SYSTEMS,
    PROFILE_BASE,
    SNOMED_SYSTEM,
)
from .validate import (
    check_coding,
    check_profile,
    check_reference,
    check_resource_type,
    first_coding,
)

PROFILE_ID = "dau-diagnostico-urgencia"
CLINICAL_SYSTEM = "http://terminology.hl7.org/CodeSystem/condition-clinical"
VERIFICATION_SYSTEM = (
    "http://terminology.hl7.org/CodeSystem/condition-ver-status"
)
CLINICAL_DISPLAY = {
    "active": "Activo",
    "recurrence": "Recurrencia",
    "relapse": "Recaída",
    "inactive": "Inactivo",
    "remission": "Remisión",
    "resolved": "Resuelto",
}
VERIFICATION_DISPLAY = {
    "unconfirmed": "Sin confirmar",
    "provisional": "Provisional",
    "differential": "Diferencial",
    "confirmed": "Confirmado",
    "refuted": "Refutado",
    "entered-in-error": "Ingresado por error",
}
CODE_SYSTEMS = {ICD10_SYSTEM, SNOMED_SYSTEM}


def _status_coding(system, code, display_map):
    return {
        "coding": [
            {
                "code": code,
                "system": system,
                "display": display_map.get(code, code),
            }
        ]
    }


def build_condition(data):
    """Construye un Condition DAU (sin ``id``).

    Entrada: ``{"clinical_status", "verification_status", "code",
    "code_system", "code_display"?, "subject", "encounter",
    "recorded_date"?, "local_id"?}``. Con solo ``code_text`` (sin
    ``code``/``code_system``) el código va como texto.
    """
    clinical = data.get("clinical_status")
    verification = data.get("verification_status")
    if clinical not in CLINICAL_DISPLAY:
        raise ValueError(
            "clinical_status debe ser uno de %s"
            % sorted(CLINICAL_DISPLAY)
        )
    if verification not in VERIFICATION_DISPLAY:
        raise ValueError(
            "verification_status debe ser uno de %s"
            % sorted(VERIFICATION_DISPLAY)
        )
    if data.get("code"):
        if not data.get("code_system"):
            raise ValueError("code exige code_system")
        if data["code_system"] not in CODE_SYSTEMS:
            raise ValueError(
                "code_system debe ser CIE-10 o SNOMED CT"
            )
        code = {
            "coding": [
                {
                    "code": data["code"],
                    "system": data["code_system"],
                }
            ]
        }
        if data.get("code_display"):
            code["coding"][0]["display"] = data["code_display"]
    elif data.get("code_text"):
        code = {"text": data["code_text"]}
    else:
        raise ValueError("se requiere code o code_text")
    if not data.get("subject"):
        raise ValueError("se requiere subject")
    if not data.get("encounter"):
        raise ValueError("se requiere encounter")
    condition = {
        "resourceType": "Condition",
        "meta": {"profile": [PROFILE_BASE + PROFILE_ID]},
        "clinicalStatus": _status_coding(
            CLINICAL_SYSTEM, clinical, CLINICAL_DISPLAY
        ),
        "verificationStatus": _status_coding(
            VERIFICATION_SYSTEM, verification, VERIFICATION_DISPLAY
        ),
        "code": code,
        "subject": {"reference": data["subject"]},
        "encounter": {"reference": data["encounter"]},
    }
    if data.get("recorded_date"):
        condition["recordedDate"] = data["recorded_date"]
    if data.get("local_id"):
        condition["identifier"] = [
            {
                "system": LOCAL_ID_SYSTEMS["diagnostico"],
                "value": data["local_id"],
            }
        ]
    return condition


def validate_condition(resource):
    """Errores del Condition contra DAUDiagnosticoUrgencia."""
    errors = []
    check_resource_type(resource, "Condition", errors)
    check_profile(resource, PROFILE_ID, errors)
    check_coding(
        resource.get("clinicalStatus"), CLINICAL_SYSTEM,
        set(CLINICAL_DISPLAY), "clinicalStatus", errors,
    )
    check_coding(
        resource.get("verificationStatus"), VERIFICATION_SYSTEM,
        set(VERIFICATION_DISPLAY), "verificationStatus", errors,
    )
    code = resource.get("code")
    if not isinstance(code, dict):
        errors.append("code 1..1: falta code")
    else:
        coding = first_coding(code)
        if coding is not None:
            if not coding.get("system"):
                errors.append("code: código sin sistema")
            elif coding["system"] not in CODE_SYSTEMS:
                errors.append(
                    "code: system debe ser CIE-10 o SNOMED CT"
                )
            if not coding.get("code"):
                errors.append("code: falta code")
        elif not code.get("text"):
            errors.append("code: falta coding o text")
    check_reference(resource.get("subject"), "subject", errors)
    check_reference(resource.get("encounter"), "encounter", errors)
    return errors
