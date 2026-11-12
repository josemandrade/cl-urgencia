"""Tests for dau.conditions (DAUDiagnosticoUrgencia) — Task 7, RED first."""

import unittest

from dau.conditions import build_condition, validate_condition
from dau.constants import ICD10_SYSTEM, LOCAL_ID_SYSTEMS

from tests.golden import assert_golden_equal

EGRESO_DATA = {
    "clinical_status": "active",
    "verification_status": "confirmed",
    "code": "I46.9",
    "code_system": ICD10_SYSTEM,
    "code_display": "Paro cardíaco, no especificado",
    "subject": "Patient/ejemplo-paciente",
    "encounter": "Encounter/ejemplo-encuentro-alta",
    "recorded_date": "2026-11-11T14:20:00-03:00",
    "local_id": "SYN-URG-001-1",
}

HIPOTESIS_DATA = {
    "clinical_status": "active",
    "verification_status": "provisional",
    "code": "R07.4",
    "code_system": ICD10_SYSTEM,
    "code_display": "Dolor en el pecho, no especificado",
    "subject": "Patient/ejemplo-paciente",
    "encounter": "Encounter/ejemplo-encuentro-abandono",
    "recorded_date": "2026-11-11T11:00:00-03:00",
    "local_id": "SYN-URG-002-1",
}

PROFILE = (
    "https://josemandrade.github.io/cl-urgencia/"
    "StructureDefinition/dau-diagnostico-urgencia"
)


class TestBuildCondition(unittest.TestCase):
    def test_egreso_matches_golden(self):
        # Coincide con el golden salvo id/meta y el identificador local
        # añadido (Ruling Task 7/8/9: el PUT condicional lo exige).
        cond = build_condition(EGRESO_DATA)
        self.assertEqual(cond["meta"]["profile"], [PROFILE])
        self.assertNotIn("id", cond)
        assert_golden_equal(
            self, cond, "Condition-ejemplo-diagnostico-egreso.json",
            local_id="SYN-URG-001-1",
            local_system=LOCAL_ID_SYSTEMS["diagnostico"],
        )

    def test_hipotesis_matches_golden(self):
        cond = build_condition(HIPOTESIS_DATA)
        assert_golden_equal(
            self, cond, "Condition-ejemplo-hipotesis.json",
            local_id="SYN-URG-002-1",
            local_system=LOCAL_ID_SYSTEMS["diagnostico"],
        )

    def test_local_identifier_included(self):
        cond = build_condition(EGRESO_DATA)
        self.assertEqual(
            cond["identifier"],
            [
                {
                    "system": LOCAL_ID_SYSTEMS["diagnostico"],
                    "value": "SYN-URG-001-1",
                }
            ],
        )

    def test_without_local_id_no_identifier(self):
        data = {k: v for k, v in EGRESO_DATA.items() if k != "local_id"}
        self.assertNotIn("identifier", build_condition(data))


class TestValidateCondition(unittest.TestCase):
    def test_valid_egreso(self):
        self.assertEqual(
            validate_condition(build_condition(EGRESO_DATA)), []
        )

    def test_valid_hipotesis(self):
        self.assertEqual(
            validate_condition(build_condition(HIPOTESIS_DATA)), []
        )

    def test_code_without_system_error(self):
        cond = build_condition(EGRESO_DATA)
        del cond["code"]["coding"][0]["system"]
        self.assertTrue(validate_condition(cond))

    def test_missing_code_error(self):
        cond = build_condition(EGRESO_DATA)
        del cond["code"]
        self.assertTrue(validate_condition(cond))

    def test_missing_clinical_status_error(self):
        cond = build_condition(EGRESO_DATA)
        del cond["clinicalStatus"]
        self.assertTrue(validate_condition(cond))

    def test_missing_subject_error(self):
        cond = build_condition(EGRESO_DATA)
        del cond["subject"]
        self.assertTrue(validate_condition(cond))

    def test_missing_encounter_error(self):
        cond = build_condition(EGRESO_DATA)
        del cond["encounter"]
        self.assertTrue(validate_condition(cond))


if __name__ == "__main__":
    unittest.main()
