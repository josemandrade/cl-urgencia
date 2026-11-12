"""PI-0: resultado de la resolución de identidad del paciente.

La identidad se resuelve contra el MPI MINSAL dentro del Bus (operations.md
PI-0; PIXm parcial, ITI-83/ITI-104). El HIS no llama a PIXm: la resolución
ocurre dentro del Bus, como parte de la transacción. Este módulo solo
codifica el resultado, sin llamadas de red.
"""

from .identifiers import validate_run

# Resultado del MPI, tal como lo reporta el Bus.
MPI_RESULTS = ("found", "not_found", "duplicate", "down")


def resolve_identity(run: str, mpi_result: str) -> str:
    """Resultado de resolver la identidad de un paciente por su RUN.

    - RUN con DV inválido -> ``rejected_invalid_run`` (PI-0: se rechaza).
    - ``found`` -> ``resolved``.
    - ``not_found`` -> ``created`` (se crea en el MPI).
    - ``duplicate`` -> ``rejected_to_reconciliation`` (duplicada o
      contradictoria: se rechaza a conciliación).
    - ``down`` -> ``transient_error`` (MPI caído: error transitorio).
    """
    if not validate_run(run):
        return "rejected_invalid_run"
    if mpi_result == "found":
        return "resolved"
    if mpi_result == "not_found":
        return "created"
    if mpi_result == "duplicate":
        return "rejected_to_reconciliation"
    if mpi_result == "down":
        return "transient_error"
    raise ValueError(f"mpi_result desconocido: {mpi_result!r}")
