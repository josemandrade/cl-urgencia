"""CLI del componente DAU.

Uso::

    PYTHONPATH=src python3 -m dau.cli <operación> <entrada.json>

Lee la entrada sintética JSON, ejecuta la operación y escribe el
resultado JSON por stdout. La CLI no hace llamadas de red: construye
Bundles, consultas y peticiones; el envío es trabajo de ``client.py``.

Operaciones: ``admission-bundle``, ``discharge-bundle``,
``abandonment-bundle``, ``patient-search``,
``encounter-search-by-patient``, ``encounter-search-by-provider``,
``condition-search``, ``document-search``, ``subscription``,
``pdf-download``, ``resolve-identity``, ``bus-response``.

Las entradas de ejemplo están en ``examples/`` (una por operación).
"""

import json
import sys

from .access import build_pdf_download
from .bundles import (
    build_abandonment_bundle,
    build_admission_bundle,
    build_discharge_bundle,
)
from .identity import resolve_identity
from .responses import handle_bus_response
from .search import (
    build_condition_search,
    build_document_search,
    build_encounter_search_by_patient,
    build_encounter_search_by_provider,
    build_encounter_subscription,
    build_patient_search,
)

USAGE = (
    "uso: python3 -m dau.cli <operación> <entrada.json>\n"
    "operaciones: admission-bundle, discharge-bundle, "
    "abandonment-bundle, patient-search, encounter-search-by-patient, "
    "encounter-search-by-provider, condition-search, document-search, "
    "subscription, pdf-download, resolve-identity, bus-response"
)


def _bundle(operation, data):
    builders = {
        "admission-bundle": build_admission_bundle,
        "discharge-bundle": build_discharge_bundle,
        "abandonment-bundle": build_abandonment_bundle,
    }
    return builders[operation](data, data.get("uuids"))


OPERATIONS = {
    "admission-bundle": lambda data: _bundle("admission-bundle", data),
    "discharge-bundle": lambda data: _bundle("discharge-bundle", data),
    "abandonment-bundle": lambda data: _bundle(
        "abandonment-bundle", data
    ),
    "patient-search": lambda data: build_patient_search(data["run"]),
    "encounter-search-by-patient": lambda data: (
        build_encounter_search_by_patient(data["run"])
    ),
    "encounter-search-by-provider": lambda data: (
        build_encounter_search_by_provider(data["deis_code"])
    ),
    "condition-search": lambda data: build_condition_search(
        data["encounter_id"]
    ),
    "document-search": lambda data: build_document_search(
        data["encounter_id"]
    ),
    "subscription": lambda data: build_encounter_subscription(
        data["channel_type"], data["endpoint"]
    ),
    "pdf-download": lambda data: build_pdf_download(
        data["document_reference"], data["token"]
    ),
    "resolve-identity": lambda data: resolve_identity(
        data["run"], data["mpi_result"]
    ),
    "bus-response": lambda data: handle_bus_response(
        data["status"], data.get("body")
    ),
}


def main(argv=None):
    """Punto de entrada de la CLI; devuelve el código de salida."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2 or argv[0] not in OPERATIONS:
        print(USAGE, file=sys.stderr)
        return 2
    operation, input_path = argv
    try:
        with open(input_path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as error:
        print("no se pudo leer %s: %s" % (input_path, error),
              file=sys.stderr)
        return 2
    try:
        result = OPERATIONS[operation](data)
    except (KeyError, ValueError) as error:
        print("entrada inválida: %s" % error, file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
