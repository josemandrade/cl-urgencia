"""Paciente de urgencia (perfil DAUPaciente).

Entrada plana snake_case::

    {"run": "12345678-5", "family": "Pérez", "given": "Juan",
     "gender": "male", "birth_date": "1980-05-15"}

o, en NN (persona sin identificar)::

    {"ficha_local": "F-123", "gender": "unknown"}

El RUN se valida estrictamente (PI-0: DV inválido -> se rechaza).
"""

from .constants import PROFILE_BASE, RUN_SYSTEM
from .identifiers import validate_run
from .validate import (
    check_identifier,
    check_profile,
    check_resource_type,
)

PROFILE_ID = "dau-paciente"
GENDERS = {"male", "female", "other", "unknown"}

# CL-Core CSTipoIdentificador, código 12: número de ficha clínica
# sistema local (ver 04-mapping-table.md).
FICHA_LOCAL_SYSTEM = (
    "https://hl7chile.cl/fhir/ig/clcore/CodeSystem/CSTipoIdentificador"
)


def build_patient(data):
    """Construye un Patient DAU (sin ``id``) a partir de datos planos."""
    run = data.get("run")
    ficha_local = data.get("ficha_local")
    if run is not None and not validate_run(run):
        raise ValueError("RUN con DV inválido: %s" % run)
    if run is None and ficha_local is None:
        raise ValueError("se requiere run o ficha_local")
    gender = data.get("gender")
    if gender is None:
        raise ValueError("se requiere gender")
    patient = {
        "resourceType": "Patient",
        "meta": {"profile": [PROFILE_BASE + PROFILE_ID]},
    }
    identifiers = []
    if run is not None:
        identifiers.append({"system": RUN_SYSTEM, "value": run})
    if ficha_local is not None:
        identifiers.append(
            {
                "type": {
                    "coding": [
                        {
                            "system": FICHA_LOCAL_SYSTEM,
                            "code": "12",
                            "display": "Número de ficha clínica sistema local",
                        }
                    ]
                },
                "use": "temp",
                "value": ficha_local,
            }
        )
    patient["identifier"] = identifiers
    if data.get("family"):
        patient["name"] = [
            {"family": data["family"], "given": [data["given"]]}
        ]
    patient["gender"] = gender
    if data.get("birth_date"):
        patient["birthDate"] = data["birth_date"]
    return patient


def validate_patient(resource):
    """Errores del Patient contra DAUPaciente; [] = válido."""
    errors = []
    check_resource_type(resource, "Patient", errors)
    check_profile(resource, PROFILE_ID, errors)
    identifiers = resource.get("identifier")
    if not isinstance(identifiers, list) or not identifiers:
        errors.append("identifier 1..*: falta identifier")
    else:
        run_ids = [
            i for i in identifiers if i.get("system") == RUN_SYSTEM
        ]
        for ident in run_ids:
            check_identifier(
                ident, "identifier[run]", errors,
                system=RUN_SYSTEM, validate_value=validate_run,
            )
        ficha_ids = [
            i for i in identifiers if i.get("use") == "temp"
        ]
        for ident in ficha_ids:
            check_identifier(ident, "identifier[fichaLocal]", errors)
        if not run_ids and not ficha_ids:
            errors.append(
                "identifier: se requiere RUN o ficha local (NN)"
            )
    if resource.get("gender") not in GENDERS:
        errors.append("gender 1..1: debe ser uno de %s" % sorted(GENDERS))
    names = resource.get("name")
    if names is not None:
        if not isinstance(names, list) or not names \
                or not names[0].get("family"):
            errors.append("name: falta family")
    return errors
