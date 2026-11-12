"""Tests for dau.medications (DAUIndicacionMedicamento) — Task 8, RED first."""

import unittest

from dau.constants import LOCAL_ID_SYSTEMS
from dau.medications import build_medication_request, validate_medication_request

from tests.golden import assert_golden_equal

MED_DATA = {
    "medication_text": "Paracetamol 500 mg",
    "dosage_text": "1 comprimido cada 8 horas por 5 días",
    "subject": "Patient/ejemplo-paciente",
    "encounter": "Encounter/ejemplo-encuentro-alta",
    "local_id": "SYN-URG-001-1",
}

PROFILE = (
    "https://josemandrade.github.io/cl-urgencia/"
    "StructureDefinition/dau-indicacion-medicamento"
)


class TestBuildMedicationRequest(unittest.TestCase):
    def test_matches_golden(self):
        med = build_medication_request(MED_DATA)
        self.assertEqual(med["meta"]["profile"], [PROFILE])
        self.assertNotIn("id", med)
        self.assertEqual(med["status"], "active")
        self.assertEqual(med["intent"], "order")
        assert_golden_equal(
            self, med, "MedicationRequest-ejemplo-medicamento-alta.json",
            local_id="SYN-URG-001-1",
            local_system=LOCAL_ID_SYSTEMS["medicamento"],
        )

    def test_local_identifier_included(self):
        med = build_medication_request(MED_DATA)
        self.assertEqual(
            med["identifier"],
            [
                {
                    "system": LOCAL_ID_SYSTEMS["medicamento"],
                    "value": "SYN-URG-001-1",
                }
            ],
        )

    def test_without_medication_text_rejected(self):
        with self.assertRaises(ValueError):
            build_medication_request(
                {k: v for k, v in MED_DATA.items()
                 if k != "medication_text"}
            )


class TestValidateMedicationRequest(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(
            validate_medication_request(build_medication_request(MED_DATA)),
            [],
        )

    def test_missing_medication_error(self):
        med = build_medication_request(MED_DATA)
        del med["medicationCodeableConcept"]
        self.assertTrue(validate_medication_request(med))

    def test_missing_subject_error(self):
        med = build_medication_request(MED_DATA)
        del med["subject"]
        self.assertTrue(validate_medication_request(med))

    def test_missing_encounter_error(self):
        med = build_medication_request(MED_DATA)
        del med["encounter"]
        self.assertTrue(validate_medication_request(med))

    def test_wrong_status_error(self):
        med = build_medication_request(MED_DATA)
        med["status"] = "draft"
        self.assertTrue(validate_medication_request(med))

    def test_wrong_intent_error(self):
        med = build_medication_request(MED_DATA)
        med["intent"] = "plan"
        self.assertTrue(validate_medication_request(med))


if __name__ == "__main__":
    unittest.main()
