"""Tests for dau.responses — Task 20, RED first."""

import unittest

from dau.encounters import build_discharge_encounter
from dau.responses import (
    build_correction_encounter,
    check_admission_allowed,
    handle_bus_response,
)
from tests.test_encounters import DISCHARGE_DATA


class TestHandleBusResponse(unittest.TestCase):
    def test_200_applied(self):
        result = handle_bus_response(
            200, {"resourceType": "Bundle", "type": "transaction-response"}
        )
        self.assertEqual(result["outcome"], "applied")

    def test_400_correct_and_resend(self):
        body = {
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "error",
                    "code": "invalid",
                    "diagnostics": "El recurso no es válido",
                }
            ],
        }
        result = handle_bus_response(400, body)
        self.assertEqual(result["outcome"], "correct_and_resend")
        self.assertIn("no es válido", result["detail"])

    def test_412_ambiguous(self):
        result = handle_bus_response(
            412,
            {
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "error",
                        "code": "multiple-matches",
                        "diagnostics": "El identificador es ambiguo",
                    }
                ],
            },
        )
        self.assertEqual(result["outcome"], "ambiguous")

    def test_422_mpi_identity_unresolved(self):
        body = {
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "error",
                    "code": "not-found",
                    "diagnostics": (
                        "La identidad no se resolvió en el MPI"
                    ),
                }
            ],
        }
        result = handle_bus_response(422, body)
        self.assertEqual(result["outcome"], "identity_unresolved")

    def test_422_other_correct_and_resend(self):
        body = {
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "error",
                    "code": "invalid",
                    "diagnostics": "El recurso no es válido",
                }
            ],
        }
        result = handle_bus_response(422, body)
        self.assertEqual(result["outcome"], "correct_and_resend")

    def test_unhandled_status_raises(self):
        with self.assertRaises(ValueError):
            handle_bus_response(500, {})


class TestCorrection(unittest.TestCase):
    def test_correction_keeps_dau_id_changes_only_status(self):
        encounter = build_discharge_encounter(DISCHARGE_DATA)
        corrected = build_correction_encounter(encounter)
        self.assertEqual(corrected["status"], "entered-in-error")
        self.assertEqual(
            corrected["identifier"], encounter["identifier"]
        )
        expected = dict(encounter)
        expected["status"] = "entered-in-error"
        self.assertEqual(corrected, expected)


class TestAdmissionForClosedEpisode(unittest.TestCase):
    def test_admission_for_closed_episode_rejected(self):
        with self.assertRaises(ValueError):
            check_admission_allowed("finished")

    def test_admission_for_open_episode_allowed(self):
        self.assertIsNone(check_admission_allowed("arrived"))
        self.assertIsNone(check_admission_allowed(None))


if __name__ == "__main__":
    unittest.main()
