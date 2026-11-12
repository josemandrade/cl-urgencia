"""Tests for dau.patients (DAUPaciente) — Task 2, RED first."""

import unittest

from dau.patients import build_patient, validate_patient

from tests.golden import assert_golden_equal

PATIENT_DATA = {
    "run": "12345678-5",
    "family": "Pérez",
    "given": "Juan",
    "gender": "male",
    "birth_date": "1980-05-15",
}

PROFILE = (
    "https://josemandrade.github.io/cl-urgencia/"
    "StructureDefinition/dau-paciente"
)


class TestBuildPatient(unittest.TestCase):
    def test_matches_golden(self):
        # El paciente SYN-URG-001 coincide con el golden salvo el RUN
        # (normalizado, Ruling Task 2) y id/meta (quitados del golden).
        patient = build_patient(PATIENT_DATA)
        self.assertEqual(patient["meta"]["profile"], [PROFILE])
        self.assertNotIn("id", patient)
        assert_golden_equal(
            self, patient, "Patient-ejemplo-paciente.json"
        )

    def test_invalid_run_rejected(self):
        # Ruling Task 2 / PI-0: un RUN con DV inválido se rechaza.
        with self.assertRaises(ValueError):
            build_patient({**PATIENT_DATA, "run": "12345678-9"})

    def test_nn_patient_with_ficha_local(self):
        # NN: ficha clínica local como identificador, gender unknown,
        # sin nombre ni fecha de nacimiento.
        patient = build_patient({"ficha_local": "F-123", "gender": "unknown"})
        identifiers = patient["identifier"]
        self.assertEqual(len(identifiers), 1)
        self.assertEqual(identifiers[0]["use"], "temp")
        self.assertEqual(identifiers[0]["value"], "F-123")
        self.assertEqual(patient["gender"], "unknown")
        self.assertNotIn("name", patient)
        self.assertNotIn("birthDate", patient)
        self.assertEqual(validate_patient(patient), [])


class TestValidatePatient(unittest.TestCase):
    def test_valid_patient(self):
        self.assertEqual(validate_patient(build_patient(PATIENT_DATA)), [])

    def test_missing_run(self):
        patient = build_patient(PATIENT_DATA)
        del patient["identifier"]
        errors = validate_patient(patient)
        self.assertTrue(errors)

    def test_invalid_run_dv(self):
        patient = build_patient(PATIENT_DATA)
        patient["identifier"][0]["value"] = "12345678-9"
        errors = validate_patient(patient)
        self.assertTrue(errors)

    def test_missing_gender(self):
        patient = build_patient(PATIENT_DATA)
        del patient["gender"]
        errors = validate_patient(patient)
        self.assertTrue(errors)

    def test_wrong_resource_type(self):
        patient = build_patient(PATIENT_DATA)
        patient["resourceType"] = "Organization"
        self.assertTrue(validate_patient(patient))


if __name__ == "__main__":
    unittest.main()
