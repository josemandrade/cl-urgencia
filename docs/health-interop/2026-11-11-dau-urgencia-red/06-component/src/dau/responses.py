"""Respuestas del Bus y correcciones (PI-1, operations.md).

- ``200`` (transaction-response): el aviso se aplicó.
- ``400`` / ``422`` (OperationOutcome): no se aplica nada; el HIS
  corrige y reenvía. En ``422``, si el OperationOutcome señala que la
  identidad no se resolvió en el MPI, el resultado es
  ``identity_unresolved``; si no, ``correct_and_resend``.
- ``412``: el identificador condicional es ambiguo.
- Corrección: se reenvía el Encounter con ``status = entered-in-error``.
  No se envía la admisión de un episodio ya cerrado (el PUT lo
  reabriría).
"""

import copy


def _issue_text(body):
    """Primer diagnostics del OperationOutcome, si lo hay."""
    if isinstance(body, dict):
        issues = body.get("issue") or []
        for issue in issues:
            if isinstance(issue, dict) and issue.get("diagnostics"):
                return issue["diagnostics"]
    return None


def _mentions_mpi(body):
    """¿El OperationOutcome habla de identidad / MPI?"""
    texts = []

    def _walk(obj):
        if isinstance(obj, dict):
            for value in obj.values():
                _walk(value)
        elif isinstance(obj, list):
            for item in obj:
                _walk(item)
        elif isinstance(obj, str):
            texts.append(obj.lower())

    _walk(body)
    joined = " ".join(texts)
    return "mpi" in joined or "identidad" in joined \
        or "identity" in joined


def handle_bus_response(status, body):
    """Resultado de una respuesta del Bus.

    Devuelve ``{"outcome", "detail"}`` con outcome en ``applied`` |
    ``correct_and_resend`` | ``ambiguous`` | ``identity_unresolved``.
    Un status fuera de lo que la guía define (200 / 400–499) da
    ``ValueError``: no se inventa un resultado para él.
    """
    if status == 200:
        return {"outcome": "applied", "detail": body}
    if status == 412:
        return {
            "outcome": "ambiguous",
            "detail": _issue_text(body)
            or "identificador condicional ambiguo",
        }
    if status == 422 and _mentions_mpi(body):
        return {
            "outcome": "identity_unresolved",
            "detail": _issue_text(body)
            or "la identidad no se resolvió en el MPI",
        }
    if 400 <= status <= 499:
        return {
            "outcome": "correct_and_resend",
            "detail": _issue_text(body) or body,
        }
    raise ValueError(
        "status de respuesta no contemplado por la guía: %s" % status
    )


def build_correction_encounter(encounter):
    """Copia del Encounter con ``status = entered-in-error``.

    La corrección conserva el ID DAU y cambia solo el status; el resto
    del recurso queda intacto.
    """
    corrected = copy.deepcopy(encounter)
    corrected["status"] = "entered-in-error"
    return corrected


def check_admission_allowed(existing_status):
    """¿Se puede enviar la admisión de este episodio?

    ``existing_status`` es el status del Encounter ya existente, o
    ``None`` si no hay episodio. Un episodio ya cerrado (``finished``)
    rechaza la admisión con ``ValueError``: el PUT lo reabriría.
    """
    if existing_status == "finished":
        raise ValueError(
            "no se envía la admisión de un episodio ya cerrado"
        )
    return None
