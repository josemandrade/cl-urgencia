"""Ensamblador de los tres Bundles transaccionales (PI-1).

Cada aviso es un Bundle ``type=transaction`` sobre un solo Encounter
por episodio (guía v0.2.0):

- admisión: POST de los maestros (Patient, Organization, Practitioner)
  con ``ifNoneExist`` + PUT condicional del Encounter por ID DAU.
- alta: 4 PUT condicionales (Encounter, Condition, MedicationRequest,
  DocumentReference); sin medicamento, 3 entradas.
- abandono: 3 PUT condicionales (Encounter, Condition hipótesis,
  DocumentReference).

Referencias: los builders emiten referencias lógicas
(``Patient/ejemplo-paciente``, ...). El ensamblador las reescribe a
los ``fullUrl urn:uuid:`` de las entradas del propio Bundle (Ruling
Task 10/11/12). Las referencias a recursos que NO son entradas de este
Bundle (p. ej. el Patient en el Bundle de alta, ya creado por el de
admisión) quedan lógicas, como en los ejemplos compilados de la guía.
Los recursos se emiten SIN ``Resource.id``.

Los nombres lógicos ``ejemplo-*`` son los de los ejemplos de la guía
y solo existen como anclas internas antes de la reescritura.
"""

import copy
import uuid as uuidlib

from .conditions import build_condition
from .constants import (
    DEIS_SYSTEM,
    LOCAL_ID_SYSTEMS,
    PROFILE_BASE,
    RUN_SYSTEM,
)
from .documents import build_document_reference
from .encounters import (
    build_abandonment_encounter,
    build_admission_encounter,
    build_discharge_encounter,
)
from .identifiers import dau_system
from .medications import build_medication_request
from .patients import build_patient
from .providers import build_organization, build_practitioner

BUNDLE_PROFILE = "dau-bundle-aviso"

LOGICAL = {
    "patient": "Patient/ejemplo-paciente",
    "organization": "Organization/ejemplo-establecimiento",
    "practitioner": "Practitioner/ejemplo-profesional",
    "encounter_admission": "Encounter/ejemplo-encuentro-admision",
    "encounter_discharge": "Encounter/ejemplo-encuentro-alta",
    "encounter_abandonment": "Encounter/ejemplo-encuentro-abandono",
    "condition_discharge": "Condition/ejemplo-diagnostico-egreso",
    "condition_abandonment": "Condition/ejemplo-hipotesis",
    "medication": "MedicationRequest/ejemplo-medicamento-alta",
    "document_discharge": "DocumentReference/ejemplo-documento-alta",
    "document_abandonment": "DocumentReference/ejemplo-documento-abandono",
}


def _full_url(uuids, key):
    """``urn:uuid:`` fijo por ``uuids`` o generado."""
    value = (uuids or {}).get(key) or str(uuidlib.uuid4())
    return "urn:uuid:" + value


def _rewrite_references(resource, mapping):
    """Reescribe las referencias lógicas de un recurso según ``mapping``."""
    if isinstance(resource, dict):
        if set(resource.keys()) == {"reference"} \
                and resource["reference"] in mapping:
            return {"reference": mapping[resource["reference"]]}
        return {
            key: _rewrite_references(value, mapping)
            for key, value in resource.items()
        }
    if isinstance(resource, list):
        return [_rewrite_references(item, mapping) for item in resource]
    return resource


def _assemble(entries, mapping, timestamp):
    """Bundle transaction con las entradas ya reescritas."""
    rewritten = []
    for full_url, resource, request in entries:
        rewritten.append(
            {
                "fullUrl": full_url,
                "resource": _rewrite_references(resource, mapping),
                "request": request,
            }
        )
    return {
        "resourceType": "Bundle",
        "meta": {"profile": [PROFILE_BASE + BUNDLE_PROFILE]},
        "type": "transaction",
        "timestamp": timestamp,
        "entry": rewritten,
    }


def _masters(data, uuids):
    """Los tres maestros + sus fullUrl y el mapa lógico -> fullUrl."""
    patient = build_patient(data["patient"])
    organization = build_organization(data["organization"])
    practitioner = build_practitioner(data["practitioner"])
    full_urls = {
        "patient": _full_url(uuids, "patient"),
        "organization": _full_url(uuids, "organization"),
        "practitioner": _full_url(uuids, "practitioner"),
    }
    mapping = {
        LOGICAL["patient"]: full_urls["patient"],
        LOGICAL["organization"]: full_urls["organization"],
        LOGICAL["practitioner"]: full_urls["practitioner"],
    }
    return patient, organization, practitioner, full_urls, mapping


def _master_requests(data):
    """Requests POST con ifNoneExist de los tres maestros."""
    return {
        "patient": {
            "method": "POST",
            "url": "Patient",
            "ifNoneExist": "identifier=%s|%s"
            % (RUN_SYSTEM, data["patient"]["run"]),
        },
        "organization": {
            "method": "POST",
            "url": "Organization",
            "ifNoneExist": "identifier=%s|%s"
            % (DEIS_SYSTEM, data["organization"]["deis_code"]),
        },
        "practitioner": {
            "method": "POST",
            "url": "Practitioner",
            "ifNoneExist": "identifier=%s|%s"
            % (RUN_SYSTEM, data["practitioner"]["run"]),
        },
    }


def _encounter_put_request(data):
    return {
        "method": "PUT",
        "url": "Encounter?identifier=%s|%s"
        % (
            dau_system(data["encounter"]["deis_code"]),
            data["encounter"]["dau_id"],
        ),
    }


def _put_request(resource_type, local_id):
    return {
        "method": "PUT",
        "url": "%s?identifier=%s|%s"
        % (
            resource_type,
            LOCAL_ID_SYSTEMS[
                {
                    "Condition": "diagnostico",
                    "MedicationRequest": "medicamento",
                    "DocumentReference": "documento",
                }[resource_type]
            ],
            local_id,
        ),
    }


def build_admission_bundle(data, uuids=None):
    """Bundle de admisión (PI-1): maestros + PUT del Encounter.

    Entrada: ``{"patient", "organization", "practitioner", "encounter",
    "timestamp"?}``; ``encounter`` con los campos de
    ``build_admission_encounter`` (sin las referencias, que pone el
    ensamblador). ``timestamp`` por defecto: ``period_start``.
    """
    patient, organization, practitioner, full_urls, mapping = _masters(
        data, uuids
    )
    encounter_data = {
        **data["encounter"],
        "patient": LOGICAL["patient"],
        "provider": LOGICAL["organization"],
        "practitioner": LOGICAL["practitioner"],
    }
    encounter = build_admission_encounter(encounter_data)
    encounter_url = _full_url(uuids, "encounter")
    mapping[LOGICAL["encounter_admission"]] = encounter_url
    requests = _master_requests(data)
    entries = [
        (full_urls["patient"], patient, requests["patient"]),
        (full_urls["organization"], organization,
         requests["organization"]),
        (full_urls["practitioner"], practitioner,
         requests["practitioner"]),
        (encounter_url, encounter, _encounter_put_request(data)),
    ]
    timestamp = data.get("timestamp") or data["encounter"]["period_start"]
    return _assemble(entries, mapping, timestamp)


def build_discharge_bundle(data, uuids=None):
    """Bundle de alta (PI-1): 4 PUT condicionales (3 sin medicamento).

    Entrada: como la admisión, con ``encounter`` de alta
    (``period_end``, ``destino``, ``destination``?), ``condition``,
    ``medication``? y ``document``. ``timestamp`` por defecto: la fecha
    del documento o ``period_end``.
    """
    encounter_data = {
        **data["encounter"],
        "patient": LOGICAL["patient"],
        "provider": LOGICAL["organization"],
        "practitioner": LOGICAL["practitioner"],
        "diagnosis_condition": LOGICAL["condition_discharge"],
    }
    encounter = build_discharge_encounter(encounter_data)
    condition = build_condition(
        {
            **data["condition"],
            "subject": LOGICAL["patient"],
            "encounter": LOGICAL["encounter_discharge"],
        }
    )
    document = build_document_reference(
        {
            **data["document"],
            "subject": LOGICAL["patient"],
            "encounter": LOGICAL["encounter_discharge"],
        }
    )
    full_urls = {
        "encounter": _full_url(uuids, "encounter"),
        "condition": _full_url(uuids, "condition"),
        "document": _full_url(uuids, "document"),
    }
    mapping = {
        LOGICAL["encounter_discharge"]: full_urls["encounter"],
        LOGICAL["condition_discharge"]: full_urls["condition"],
        LOGICAL["document_discharge"]: full_urls["document"],
    }
    entries = [
        (full_urls["encounter"], encounter, _encounter_put_request(data)),
        (
            full_urls["condition"],
            condition,
            _put_request("Condition", data["condition"]["local_id"]),
        ),
    ]
    if data.get("medication"):
        medication = build_medication_request(
            {
                **data["medication"],
                "subject": LOGICAL["patient"],
                "encounter": LOGICAL["encounter_discharge"],
            }
        )
        full_urls["medication"] = _full_url(uuids, "medication")
        mapping[LOGICAL["medication"]] = full_urls["medication"]
        entries.append(
            (
                full_urls["medication"],
                medication,
                _put_request(
                    "MedicationRequest",
                    data["medication"]["local_id"],
                ),
            )
        )
    entries.append(
        (
            full_urls["document"],
            document,
            _put_request(
                "DocumentReference", data["document"]["local_id"]
            ),
        )
    )
    timestamp = (
        data.get("timestamp")
        or data["document"].get("date")
        or data["encounter"]["period_end"]
    )
    return _assemble(entries, mapping, timestamp)


def build_abandonment_bundle(data, uuids=None):
    """Bundle de abandono (PI-1): 3 PUT condicionales.

    Entrada: como la admisión, con ``encounter`` de abandono
    (``period_end``, ``tipo``), ``condition`` (hipótesis) y ``document``.
    ``timestamp`` por defecto: la fecha del documento o ``period_end``.
    """
    encounter_data = {
        **data["encounter"],
        "patient": LOGICAL["patient"],
        "provider": LOGICAL["organization"],
        "practitioner": LOGICAL["practitioner"],
        "diagnosis_condition": LOGICAL["condition_abandonment"],
    }
    encounter = build_abandonment_encounter(encounter_data)
    condition = build_condition(
        {
            **data["condition"],
            "subject": LOGICAL["patient"],
            "encounter": LOGICAL["encounter_abandonment"],
        }
    )
    document = build_document_reference(
        {
            **data["document"],
            "subject": LOGICAL["patient"],
            "encounter": LOGICAL["encounter_abandonment"],
        }
    )
    full_urls = {
        "encounter": _full_url(uuids, "encounter"),
        "condition": _full_url(uuids, "condition"),
        "document": _full_url(uuids, "document"),
    }
    mapping = {
        LOGICAL["encounter_abandonment"]: full_urls["encounter"],
        LOGICAL["condition_abandonment"]: full_urls["condition"],
        LOGICAL["document_abandonment"]: full_urls["document"],
    }
    entries = [
        (full_urls["encounter"], encounter, _encounter_put_request(data)),
        (
            full_urls["condition"],
            condition,
            _put_request("Condition", data["condition"]["local_id"]),
        ),
        (
            full_urls["document"],
            document,
            _put_request(
                "DocumentReference", data["document"]["local_id"]
            ),
        ),
    ]
    timestamp = (
        data.get("timestamp")
        or data["document"].get("date")
        or data["encounter"]["period_end"]
    )
    return _assemble(entries, mapping, timestamp)


def rewrite_references(resource, mapping):
    """Reescritura pública de referencias lógicas a ``urn:uuid:``."""
    return _rewrite_references(copy.deepcopy(resource), mapping)
