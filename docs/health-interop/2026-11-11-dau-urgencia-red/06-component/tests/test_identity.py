"""Tests for dau.identity (PI-0 identity resolution) — Task 13, RED first."""

import unittest

from dau.identity import resolve_identity


class TestResolveIdentity(unittest.TestCase):
    def test_invalid_run_rejected(self):
        # PI-0: RUN con DV inválido se rechaza (los RUN de ejemplo de la
        # guía, 12345678-9 y 98765432-1, tienen DV inválido: calculado 5).
        self.assertEqual(
            resolve_identity("12345678-9", "found"), "rejected_invalid_run"
        )
        self.assertEqual(
            resolve_identity("98765432-1", "not_found"), "rejected_invalid_run"
        )

    def test_found_resolved(self):
        self.assertEqual(resolve_identity("12345678-5", "found"), "resolved")

    def test_not_found_created(self):
        # Identidad no encontrada: se crea en el MPI.
        self.assertEqual(resolve_identity("12345678-5", "not_found"), "created")

    def test_duplicate_rejected_to_reconciliation(self):
        # Duplicada o contradictoria: se rechaza a conciliación.
        self.assertEqual(
            resolve_identity("12345678-5", "duplicate"),
            "rejected_to_reconciliation",
        )

    def test_mpi_down_transient_error(self):
        # MPI caído: error transitorio.
        self.assertEqual(resolve_identity("12345678-5", "down"), "transient_error")

    def test_unknown_mpi_result_raises(self):
        with self.assertRaises(ValueError):
            resolve_identity("12345678-5", "unknown")


if __name__ == "__main__":
    unittest.main()
