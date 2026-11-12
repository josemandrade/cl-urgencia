"""Medicamento indicado al alta (perfil DAUIndicacionMedicamento).

status = active, intent = order, medication[x] solo CodeableConcept.
Solo se informa si existe al menos un medicamento al alta.

Acepta ``local_id``: el PUT condicional del Bundle exige un
``identifier`` local del HIS (Ruling Task 7/8/9), con el sistema de la
guía y valor ``<DAU>-1``.
"""

from .constants import LOCAL_ID_SYSTEMS, PROFILE_BASE
from .validate import (
    check_profile,
    check_reference,
    check_resource_type,
)

PROFILE_ID = "dau-indicacion-medicamento"


def build_medication_request(data):
    """Construye un MedicationRequest DAU (sin ``id``).

    Entrada: ``{"medication_text", "dosage_text"?, "subject",
    "encounter", "local_id"?}``.
    """
    if not data.get("medication_text"):
        raise ValueError("se requiere medication_text")
    if not data.get("subject"):
        raise ValueError("se requiere subject")
    if not data.get("encounter"):
        raise ValueError("se requiere encounter")
    med = {
        "resourceType": "MedicationRequest",
        "meta": {"profile": [PROFILE_BASE + PROFILE_ID]},
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {"text": data["medication_text"]},
        "subject": {"reference": data["subject"]},
        "encounter": {"reference": data["encounter"]},
    }
    if data.get("dosage_text"):
        med["dosageInstruction"] = [{"text": data["dosage_text"]}]
    if data.get("local_id"):
        med["identifier"] = [
            {
                "system": LOCAL_ID_SYSTEMS["medicamento"],
                "value": data["local_id"],
            }
        ]
    return med


def validate_medication_request(resource):
    """Errores del MedicationRequest contra DAUIndicacionMedicamento."""
    errors = []
    check_resource_type(resource, "MedicationRequest", errors)
    check_profile(resource, PROFILE_ID, errors)
    if resource.get("status") != "active":
        errors.append("status 1..1: debe ser active")
    if resource.get("intent") != "order":
        errors.append("intent 1..1: debe ser order")
    medication = resource.get("medicationCodeableConcept")
    if not isinstance(medication, dict) or (
        not medication.get("text") and not medication.get("coding")
    ):
        errors.append(
            "medicationCodeableConcept 1..1: falta medication[x]"
        )
    if "medicationReference" in resource:
        errors.append(
            "medication[x] solo CodeableConcept: medicationReference no "
            "permitido"
        )
    check_reference(resource.get("subject"), "subject", errors)
    check_reference(resource.get("encounter"), "encounter", errors)
    return errors
