"""Documento de urgencia (perfil DAUDocumentoUrgencia).

Resumen de alta (LOINC 59258-4) o nota de urgencia (LOINC 34111-5).
El PDF del DAU se publica por ``content.attachment.url``.

El perfil fija ``contentType = application/pdf`` (patternCode en la
StructureDefinition): el builder lo pone siempre, aunque el ejemplo
compilado por SUSHI lo omita (Ruling Task 9).

Acepta ``local_id``: el PUT condicional del Bundle exige un
``identifier`` local del HIS (Ruling Task 7/8/9), con el sistema de la
guía y valor ``<DAU>-1``.
"""

from .constants import (
    DOC_TYPES,
    LOCAL_ID_SYSTEMS,
    LOINC_SYSTEM,
    PROFILE_BASE,
)
from .validate import (
    check_coding,
    check_profile,
    check_reference,
    check_resource_type,
)

PROFILE_ID = "dau-documento-urgencia"
PDF_CONTENT_TYPE = "application/pdf"


def build_document_reference(data):
    """Construye un DocumentReference DAU (sin ``id``).

    Entrada: ``{"type_code" (59258-4 | 34111-5), "subject",
    "encounter", "url", "date", "local_id"?}``.
    """
    type_code = data.get("type_code")
    if type_code not in DOC_TYPES:
        raise ValueError(
            "type_code debe ser uno de %s" % sorted(DOC_TYPES)
        )
    if not data.get("subject"):
        raise ValueError("se requiere subject")
    if not data.get("encounter"):
        raise ValueError("se requiere encounter")
    if not data.get("url"):
        raise ValueError("se requiere url")
    if not data.get("date"):
        raise ValueError("se requiere date")
    doc = {
        "resourceType": "DocumentReference",
        "meta": {"profile": [PROFILE_BASE + PROFILE_ID]},
        "status": "current",
        "type": {
            "coding": [
                {
                    "code": type_code,
                    "system": LOINC_SYSTEM,
                    "display": DOC_TYPES[type_code],
                }
            ]
        },
        "subject": {"reference": data["subject"]},
        "context": {
            "encounter": [{"reference": data["encounter"]}]
        },
        "content": [
            {
                "attachment": {
                    "contentType": PDF_CONTENT_TYPE,
                    "url": data["url"],
                }
            }
        ],
        "date": data["date"],
    }
    if data.get("local_id"):
        doc["identifier"] = [
            {
                "system": LOCAL_ID_SYSTEMS["documento"],
                "value": data["local_id"],
            }
        ]
    return doc


def validate_document_reference(resource):
    """Errores del DocumentReference contra DAUDocumentoUrgencia."""
    errors = []
    check_resource_type(resource, "DocumentReference", errors)
    check_profile(resource, PROFILE_ID, errors)
    if resource.get("status") != "current":
        errors.append("status 1..1: debe ser current")
    check_coding(
        resource.get("type"), LOINC_SYSTEM, set(DOC_TYPES),
        "type", errors,
    )
    check_reference(resource.get("subject"), "subject", errors)
    context = resource.get("context", {})
    encounters = context.get("encounter", [])
    if not isinstance(encounters, list) or not encounters:
        errors.append("context.encounter 1..1: falta encounter")
    else:
        for encounter in encounters:
            check_reference(encounter, "context.encounter", errors)
    content = resource.get("content")
    if not isinstance(content, list) or not content:
        errors.append("content 1..1: falta content")
    else:
        attachment = content[0].get("attachment", {})
        if not attachment.get("url"):
            errors.append(
                "content.attachment.url 1..1: falta url"
            )
        if attachment.get("contentType") is None:
            errors.append(
                "content.attachment.contentType: falta (el perfil fija "
                "application/pdf)"
            )
        elif attachment["contentType"] != PDF_CONTENT_TYPE:
            errors.append(
                "content.attachment.contentType debe ser application/pdf"
            )
    if not resource.get("date"):
        errors.append("date 1..1: falta date")
    return errors
