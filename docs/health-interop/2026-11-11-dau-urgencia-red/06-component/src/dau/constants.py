"""Constantes de la guía DAU (05-implementation-guide/).

Sistemas, códigos y canónicas, copiados de operations.md, del FSH y de la
tabla de mapeo. Nada que no esté en la guía.
"""

# Canónica de la guía y base de los perfiles DAU.
GUIDE_CANONICAL = "https://josemandrade.github.io/cl-urgencia"
PROFILE_BASE = GUIDE_CANONICAL + "/StructureDefinition/"

# Sistemas de identificadores.
RUN_SYSTEM = "urn:oid:2.16.840.1.113883.2.22.1.152.787300"
DEIS_SYSTEM = (
    "https://interoperabilidad.minsal.cl/fhir/ig/tei/CodeSystem/CSEstablecimientoDestino"
)
ICD10_SYSTEM = "http://hl7.org/fhir/sid/icd-10"
SNOMED_SYSTEM = "http://snomed.info/sct"
LOINC_SYSTEM = "http://loinc.org"

# Sistemas de identificadores locales del HIS (de los PUT condicionales de
# la guía; dominio ficticio de ejemplo, `his.ejemplo.cl`).
LOCAL_ID_SYSTEMS = {
    "diagnostico": "https://his.ejemplo.cl/fhir/sid/diagnostico",
    "medicamento": "https://his.ejemplo.cl/fhir/sid/medicamento",
    "documento": "https://his.ejemplo.cl/fhir/sid/documento",
}


def dau_system(deis_code: str) -> str:
    """Sistema del ID DAU para un establecimiento (por código DEIS)."""
    return f"https://interoperabilidad.minsal.cl/fhir/sid/dau/{deis_code}"


# Destino al alta de urgencia (ValueSet DAUDestinoAlta, códigos 01–06).
DESTINO_ALTA_SYSTEM = GUIDE_CANONICAL + "/CodeSystem/dau-destino-alta"
DESTINO_ALTA = {
    "01": "Hospitalización",
    "02": "Traslado",
    "03": "Fallecido",
    "04": "Derivación",
    "05": "Domicilio",
    "06": "Otro",
}

# Tipo de abandono (CodeSystem DAUTipoAbandonoCS): 1 NEA, 2 fuga.
TIPO_ABANDONO_SYSTEM = GUIDE_CANONICAL + "/CodeSystem/dau-tipo-abandono"
TIPO_ABANDONO = {
    "1": "NEA",
    "2": "Fuga",
}

# Tipo de documento (ValueSet DAUTipoDocumento).
DOC_TYPES = {
    "59258-4": "Resumen de alta de urgencia",
    "34111-5": "Nota de urgencia",
}
