"""Validación compartida de recursos contra los perfiles DAU.

Ayudas pequeñas que usan los validadores de cada módulo. Cada
``validate_<recurso>`` devuelve ``list[str]``; lista vacía = válido.
Comprueban campos requeridos, cardinalidades, sistemas y códigos de los
bindings, y los invariantes del perfil. No hacen llamadas de red.
"""

from .constants import PROFILE_BASE


def profile_url(profile_id):
    """Canónica del perfil DAU a partir de su id (``dau-paciente``, ...)."""
    return PROFILE_BASE + profile_id


def check_profile(resource, profile_id, errors):
    """El recurso debe declarar el perfil DAU que le corresponde."""
    profiles = resource.get("meta", {}).get("profile", [])
    if profile_url(profile_id) not in profiles:
        errors.append(
            "meta.profile debe incluir %s" % profile_url(profile_id)
        )


def check_resource_type(resource, expected, errors):
    if resource.get("resourceType") != expected:
        errors.append(
            "resourceType debe ser %s" % expected
        )


def first_coding(codeable):
    """Primer coding de un CodeableConcept, o None."""
    if not isinstance(codeable, dict):
        return None
    codings = codeable.get("coding")
    if not isinstance(codings, list) or not codings:
        return None
    return codings[0] if isinstance(codings[0], dict) else None


def check_coding_direct(coding, system, allowed_codes, field, errors):
    """Un Coding directo (``{"code": ..., "system": ...}``), como
    ``Encounter.class`` (que no es un CodeableConcept)."""
    if not isinstance(coding, dict) or not coding.get("code"):
        errors.append("%s: falta code" % field)
        return
    if system is not None and coding.get("system") != system:
        errors.append("%s: system debe ser %s" % (field, system))
    if allowed_codes is not None and coding.get("code") not in allowed_codes:
        errors.append(
            "%s: code debe ser uno de %s"
            % (field, sorted(allowed_codes))
        )


def check_coding(codeable, system, allowed_codes, field, errors):
    """Un CodeableConcept con un coding cuyo sistema y código sean los dados."""
    coding = first_coding(codeable)
    if coding is None:
        errors.append("%s: falta coding" % field)
        return
    if system is not None and coding.get("system") != system:
        errors.append(
            "%s: system debe ser %s" % (field, system)
        )
    if allowed_codes is not None and coding.get("code") not in allowed_codes:
        errors.append(
            "%s: code debe ser uno de %s"
            % (field, sorted(allowed_codes))
        )
    if not coding.get("code"):
        errors.append("%s: falta code" % field)


def check_reference(value, field, errors):
    """Una Reference con ``reference`` no vacío."""
    if not isinstance(value, dict) or not value.get("reference"):
        errors.append("%s: falta reference" % field)


def check_identifier(identifier, field, errors, system=None,
                     validate_value=None):
    """Un Identifier con value; system y valor validados si se pasan."""
    if not isinstance(identifier, dict):
        errors.append("%s: falta identifier" % field)
        return
    value = identifier.get("value")
    if not value:
        errors.append("%s: falta identifier.value" % field)
        return
    if system is not None and "system" in identifier \
            and identifier["system"] != system:
        errors.append("%s: identifier.system debe ser %s" % (field, system))
    if validate_value is not None and not validate_value(value):
        errors.append("%s: identifier.value no válido: %s" % (field, value))
