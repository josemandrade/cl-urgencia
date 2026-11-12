"""PI-2: constructores de consultas FHIR simples y Subscription.

La red hace pull del Repositorio FHIR (operations.md PI-2). Cada búsqueda
enlaza al perfil IHE que la apoya (PDQm, QEDm, MHD), pero la guía lo hace
con una búsqueda FHIR simple: este módulo construye la URL FHIR, no una
transacción IHE. La suscripción es una Subscription FHIR, no DSUB.
"""

from .constants import DEIS_SYSTEM, RUN_SYSTEM
from .identifiers import validate_run


def build_encounter_search_by_patient(run: str) -> dict:
    """GET /Encounter?patient.identifier=<sistema RUN>|<RUN>&class=EMER
    (QEDm parcial, PCC-44). RUN con DV inválido -> ValueError.
    """
    if not validate_run(run):
        raise ValueError(f"RUN con DV inválido: {run!r}")
    return {
        "method": "GET",
        "url": f"Encounter?patient.identifier={RUN_SYSTEM}|{run}&class=EMER",
    }


def build_encounter_search_by_provider(deis_code: str) -> dict:
    """GET /Encounter?service-provider.identifier=<sistema DEIS>|<código>
    &class=EMER&status=arrived (QEDm parcial, PCC-44): pacientes
    actualmente en urgencia en un establecimiento.
    """
    if not deis_code:
        raise ValueError("código DEIS vacío")
    return {
        "method": "GET",
        "url": (
            "Encounter?service-provider.identifier="
            f"{DEIS_SYSTEM}|{deis_code}&class=EMER&status=arrived"
        ),
    }


def build_condition_search(encounter_id: str) -> dict:
    """GET /Condition?encounter=Encounter/[id] (QEDm parcial, PCC-44):
    diagnósticos (hipótesis y diagnóstico de egreso) de una atención.
    `encounter_id` vacío -> ValueError.
    """
    if not encounter_id:
        raise ValueError("encounter_id vacío")
    return {
        "method": "GET",
        "url": f"Condition?encounter=Encounter/{encounter_id}",
    }


def build_document_search(encounter_id: str) -> dict:
    """GET /DocumentReference?encounter=Encounter/[id] (MHD parcial,
    ITI-67): documento del DAU de una atención. Búsqueda FHIR simple, no
    una transacción MHD. `encounter_id` vacío -> ValueError.
    """
    if not encounter_id:
        raise ValueError("encounter_id vacío")
    return {
        "method": "GET",
        "url": f"DocumentReference?encounter=Encounter/{encounter_id}",
    }


def build_encounter_subscription(channel_type: str, endpoint: str) -> dict:
    """Subscription FHIR sobre Encounter class=EMER (PI-2).

    Sin perfil IHE: es una Subscription FHIR, no DSUB (el Repositorio es
    un repositorio FHIR, no un registro XDS). `criteria` =
    ``Encounter?class=EMER``, `status` = ``requested``. El canal es un
    detalle de implementación y se pasa como parámetro; el único canal
    soportado es ``rest-hook``; cualquier otro -> ValueError explícito.
    """
    if channel_type != "rest-hook":
        raise ValueError(f"canal de suscripción no soportado: {channel_type!r}")
    if not endpoint:
        raise ValueError("endpoint de suscripción vacío")
    return {
        "resourceType": "Subscription",
        "status": "requested",
        "criteria": "Encounter?class=EMER",
        "channel": {"type": channel_type, "endpoint": endpoint},
    }


def build_patient_search(run: str) -> dict:
    """GET /Patient?identifier=<sistema RUN>|<RUN> (PDQm parcial, ITI-78/119).

    RUN con DV inválido -> ValueError antes de construir la consulta.
    """
    if not validate_run(run):
        raise ValueError(f"RUN con DV inválido: {run!r}")
    return {"method": "GET", "url": f"Patient?identifier={RUN_SYSTEM}|{run}"}
