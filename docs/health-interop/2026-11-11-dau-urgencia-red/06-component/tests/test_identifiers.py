"""Tests for dau.identifiers (RUN validation) — Task 1, RED first."""

import unittest

from dau.identifiers import dau_system, run_dv, validate_run


class TestValidateRun(unittest.TestCase):
    def test_valid_run_patient(self):
        # RUN sintético del componente (DV válido, verificado por programa).
        self.assertTrue(validate_run("12345678-5"))

    def test_guide_example_run_is_dv_invalid(self):
        # Ruling Task 2: el RUN de ejemplo de la guía (12345678-9) NO pasa el
        # DV chileno (el DV calculado es 5). PI-0 exige rechazarlo.
        self.assertFalse(validate_run("12345678-9"))

    def test_valid_run_professional(self):
        self.assertTrue(validate_run("98765432-5"))

    def test_guide_example_professional_run_is_dv_invalid(self):
        self.assertFalse(validate_run("98765432-1"))

    def test_valid_run_with_k(self):
        # 11111112: suma 34, 34 % 11 = 1, DV = 10 -> K (verificado a mano).
        self.assertEqual(run_dv("11111112"), "K")
        self.assertTrue(validate_run("11111112-K"))
        self.assertTrue(validate_run("11111112-k"))

    def test_rejects_dots(self):
        # La guía: RUN sin puntos (con guión antes del DV).
        self.assertFalse(validate_run("12.345.678-5"))

    def test_rejects_missing_dv_and_garbage(self):
        self.assertFalse(validate_run("12345678"))
        self.assertFalse(validate_run("12345678-"))
        self.assertFalse(validate_run(""))
        self.assertFalse(validate_run("ABCDEF12-3"))
        self.assertFalse(validate_run("1234567-5"))

    def test_dau_system(self):
        self.assertEqual(
            dau_system("12345"),
            "https://interoperabilidad.minsal.cl/fhir/sid/dau/12345",
        )


if __name__ == "__main__":
    unittest.main()
