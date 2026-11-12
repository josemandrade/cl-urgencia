"""Identificadores: RUN chileno y sistema del ID DAU.

El RUN se escribe sin puntos y con guión antes del DV (`12345678-5`), como
en los ejemplos de la guía. La validación del DV es estricta (PI-0: un RUN
con DV inválido se rechaza).
"""

from .constants import dau_system as _dau_system


def dau_system(deis_code: str) -> str:
    """Sistema del ID DAU para un establecimiento (por código DEIS)."""
    return _dau_system(deis_code)


def run_dv(body: str) -> str:
    """DV (módulo 11) del cuerpo numérico de un RUN.

    Dígitos de derecha a izquierda con multiplicadores 2, 3, 4, 5, 6, 7, 2,
    3, ...; DV = 11 - (suma % 11); 11 -> "0", 10 -> "K".
    """
    multipliers = [2, 3, 4, 5, 6, 7]
    total = 0
    for i, digit in enumerate(reversed(body)):
        total += int(digit) * multipliers[i % len(multipliers)]
    remainder = 11 - (total % 11)
    if remainder == 11:
        return "0"
    if remainder == 10:
        return "K"
    return str(remainder)


def validate_run(run: str) -> bool:
    """True si el RUN tiene formato `12345678-5` y el DV es correcto.

    Acepta `K` o `k` como DV. Rechaza puntos, DV ausente, y cualquier
    formato que no sea 7 u 8 dígitos, guión y un dígito o K.
    """
    if not isinstance(run, str):
        return False
    if "." in run:
        return False
    parts = run.split("-")
    if len(parts) != 2:
        return False
    body, dv = parts
    if not body.isdigit() or len(body) not in (7, 8):
        return False
    if len(dv) != 1 or (not dv.isdigit() and dv.upper() != "K"):
        return False
    return run_dv(body) == dv.upper()
