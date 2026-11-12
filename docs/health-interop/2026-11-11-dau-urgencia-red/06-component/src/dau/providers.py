"""Prestadores (perfiles DAUPrestadorOrganizacional y DAUPrestadorProfesional).

Nota sobre ``identifier.system``: los perfiles FSH fijan el sistema
(DEIS para Organization, RUN para Practitioner), pero los ejemplos
compilados por SUSHI llevan el identificador SOLO con ``value``
(sin ``system``). Los builders reproducen el ejemplo compilado tal
cual — es lo que la comparación con goldens exige (ver Ruling
propuesta Task 3 en el informe) — y los validadores comprueban el
sistema solo cuando está presente.
"""

from .constants import DEIS_SYSTEM, PROFILE_BASE, RUN_SYSTEM
from .identifiers import validate_run
from .validate import (
    check_identifier,
    check_profile,
    check_resource_type,
)


def build_organization(data):
    """Construye un Organization DAU (sin ``id``).

    Entrada: ``{"deis_code": "12345", "name": "Hospital de Prueba"}``.
    """
    deis_code = data.get("deis_code")
    name = data.get("name")
    if not deis_code:
        raise ValueError("se requiere deis_code")
    if not name:
        raise ValueError("se requiere name")
    return {
        "resourceType": "Organization",
        "meta": {
            "profile": [
                PROFILE_BASE + "dau-prestador-organizacional"
            ]
        },
        # Como en el ejemplo compilado: solo value, sin system.
        "identifier": [{"value": deis_code}],
        "name": name,
    }


def validate_organization(resource):
    """Errores del Organization contra DAUPrestadorOrganizacional."""
    errors = []
    check_resource_type(resource, "Organization", errors)
    check_profile(resource, "dau-prestador-organizacional", errors)
    identifiers = resource.get("identifier")
    if not isinstance(identifiers, list) or len(identifiers) != 1:
        errors.append("identifier 1..1: falta identifier")
    else:
        check_identifier(
            identifiers[0], "identifier", errors, system=DEIS_SYSTEM
        )
    if not resource.get("name"):
        errors.append("name 1..1: falta name")
    return errors


def build_practitioner(data):
    """Construye un Practitioner DAU (sin ``id``).

    Entrada: ``{"run": "98765432-5", "family": "González",
    "given": "María"}``. El RUN se valida estrictamente (PI-0).
    """
    run = data.get("run")
    if run is not None and not validate_run(run):
        raise ValueError("RUN con DV inválido: %s" % run)
    if not run:
        raise ValueError("se requiere run")
    if not data.get("family"):
        raise ValueError("se requiere family")
    return {
        "resourceType": "Practitioner",
        "meta": {
            "profile": [PROFILE_BASE + "dau-prestador-profesional"]
        },
        # Como en el ejemplo compilado: solo value, sin system.
        "identifier": [{"value": run}],
        "name": [
            {"family": data["family"], "given": [data["given"]]}
        ],
    }


def validate_practitioner(resource):
    """Errores del Practitioner contra DAUPrestadorProfesional."""
    errors = []
    check_resource_type(resource, "Practitioner", errors)
    check_profile(resource, "dau-prestador-profesional", errors)
    identifiers = resource.get("identifier")
    if not isinstance(identifiers, list) or len(identifiers) != 1:
        errors.append("identifier 1..1: falta identifier")
    else:
        check_identifier(
            identifiers[0], "identifier", errors,
            system=RUN_SYSTEM, validate_value=validate_run,
        )
    names = resource.get("name")
    if not isinstance(names, list) or not names \
            or not names[0].get("family"):
        errors.append("name 1..1: falta name.family")
    return errors
