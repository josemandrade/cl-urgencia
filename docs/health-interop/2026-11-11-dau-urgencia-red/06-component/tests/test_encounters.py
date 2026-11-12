"""Tests for dau.encounters — Tasks 4, 5 y 6, RED first."""

import unittest

from dau.encounters import (
    build_abandonment_encounter,
    build_admission_encounter,
    build_discharge_encounter,
    validate_encounter,
)

from tests.golden import assert_golden_equal

ADMISSION_DATA = {
    "dau_id": "SYN-URG-001",
    "deis_code": "12345",
    "patient": "Patient/ejemplo-paciente",
    "provider": "Organization/ejemplo-establecimiento",
    "practitioner": "Practitioner/ejemplo-profesional",
    "period_start": "2026-11-11T10:05:00-03:00",
    "attender_start": "2026-11-11T10:15:00-03:00",
    "reason": "Dolor torácico",
}

DISCHARGE_DATA = {
    **ADMISSION_DATA,
    "period_end": "2026-11-11T14:20:00-03:00",
    "destino": "03",
    "diagnosis_condition": "Condition/ejemplo-diagnostico-egreso",
}

ABANDONMENT_DATA = {
    "dau_id": "SYN-URG-002",
    "deis_code": "12345",
    "patient": "Patient/ejemplo-paciente",
    "provider": "Organization/ejemplo-establecimiento",
    "practitioner": "Practitioner/ejemplo-profesional",
    "period_start": "2026-11-11T10:05:00-03:00",
    "attender_start": "2026-11-11T10:15:00-03:00",
    "reason": "Dolor torácico",
    "period_end": "2026-11-11T11:30:00-03:00",
    "tipo": "2",
    "diagnosis_condition": "Condition/ejemplo-hipotesis",
}

PROFILE_BASE = "https://josemandrade.github.io/cl-urgencia/StructureDefinition/"


class TestBuildAdmissionEncounter(unittest.TestCase):
    def test_matches_golden(self):
        enc = build_admission_encounter(ADMISSION_DATA)
        self.assertEqual(
            enc["meta"]["profile"], [PROFILE_BASE + "dau-encuentro-urgencia"]
        )
        self.assertNotIn("id", enc)
        assert_golden_equal(
            self, enc, "Encounter-ejemplo-encuentro-admision.json"
        )

    def test_missing_dau_id_rejected(self):
        with self.assertRaises(ValueError):
            build_admission_encounter(
                {k: v for k, v in ADMISSION_DATA.items() if k != "dau_id"}
            )


class TestValidateEncounterAdmission(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(
            validate_encounter(build_admission_encounter(ADMISSION_DATA)), []
        )

    def test_period_end_before_start(self):
        # Invariante dau-enc-period.
        enc = build_admission_encounter(ADMISSION_DATA)
        enc["period"]["end"] = "2026-11-11T09:00:00-03:00"
        self.assertTrue(validate_encounter(enc))

    def test_reason_too_long(self):
        # Invariante dau-enc-reason: máximo 200 caracteres.
        enc = build_admission_encounter(
            {**ADMISSION_DATA, "reason": "x" * 201}
        )
        self.assertTrue(validate_encounter(enc))

    def test_reason_200_chars_ok(self):
        enc = build_admission_encounter(
            {**ADMISSION_DATA, "reason": "x" * 200}
        )
        self.assertEqual(validate_encounter(enc), [])


class TestBuildDischargeEncounter(unittest.TestCase):
    def test_matches_golden(self):
        enc = build_discharge_encounter(DISCHARGE_DATA)
        self.assertEqual(
            enc["meta"]["profile"],
            [PROFILE_BASE + "dau-encuentro-urgencia-alta"],
        )
        self.assertNotIn("id", enc)
        assert_golden_equal(
            self, enc, "Encounter-ejemplo-encuentro-alta.json"
        )

    def test_destino_01_with_destination_ok(self):
        # Invariante dau-alta-destino: 01/02/04 exigen destination.
        enc = build_discharge_encounter(
            {
                **DISCHARGE_DATA,
                "destino": "01",
                "destination": "Organization/ejemplo-establecimiento",
            }
        )
        self.assertEqual(validate_encounter(enc), [])

    def test_invalid_destino_rejected(self):
        with self.assertRaises(ValueError):
            build_discharge_encounter({**DISCHARGE_DATA, "destino": "07"})


class TestValidateEncounterDischarge(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(
            validate_encounter(build_discharge_encounter(DISCHARGE_DATA)),
            [],
        )

    def test_destino_07_error(self):
        enc = build_discharge_encounter(DISCHARGE_DATA)
        enc["hospitalization"]["dischargeDisposition"]["coding"][0][
            "code"
        ] = "07"
        self.assertTrue(validate_encounter(enc))

    def test_destino_01_without_destination_error(self):
        # Invariante dau-alta-destino.
        enc = build_discharge_encounter(
            {**DISCHARGE_DATA, "destino": "01",
             "destination": "Organization/ejemplo-establecimiento"}
        )
        del enc["hospitalization"]["destination"]
        self.assertTrue(validate_encounter(enc))

    def test_missing_diagnosis_dd_error(self):
        enc = build_discharge_encounter(DISCHARGE_DATA)
        del enc["diagnosis"]
        self.assertTrue(validate_encounter(enc))

    def test_diagnosis_without_dd_use_error(self):
        enc = build_discharge_encounter(DISCHARGE_DATA)
        del enc["diagnosis"][0]["use"]
        self.assertTrue(validate_encounter(enc))

    def test_missing_period_end_error(self):
        enc = build_discharge_encounter(DISCHARGE_DATA)
        del enc["period"]["end"]
        self.assertTrue(validate_encounter(enc))


class TestBuildAbandonmentEncounter(unittest.TestCase):
    def test_matches_golden(self):
        enc = build_abandonment_encounter(ABANDONMENT_DATA)
        self.assertEqual(
            enc["meta"]["profile"],
            [PROFILE_BASE + "dau-encuentro-urgencia-abandono"],
        )
        self.assertNotIn("id", enc)
        assert_golden_equal(
            self, enc, "Encounter-ejemplo-encuentro-abandono.json"
        )

    def test_invalid_tipo_rejected(self):
        with self.assertRaises(ValueError):
            build_abandonment_encounter({**ABANDONMENT_DATA, "tipo": "3"})

    def test_tipo_nea_ok(self):
        enc = build_abandonment_encounter({**ABANDONMENT_DATA, "tipo": "1"})
        self.assertEqual(
            enc["extension"][0]["valueCodeableConcept"]["coding"][0][
                "display"
            ],
            "NEA",
        )


class TestValidateEncounterAbandonment(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(
            validate_encounter(
                build_abandonment_encounter(ABANDONMENT_DATA)
            ),
            [],
        )

    def test_tipo_3_error(self):
        enc = build_abandonment_encounter(ABANDONMENT_DATA)
        enc["extension"][0]["valueCodeableConcept"]["coding"][0][
            "code"
        ] = "3"
        self.assertTrue(validate_encounter(enc))

    def test_with_discharge_disposition_error(self):
        enc = build_abandonment_encounter(ABANDONMENT_DATA)
        enc["hospitalization"] = {
            "dischargeDisposition": {
                "coding": [
                    {
                        "code": "05",
                        "system": "https://josemandrade.github.io/"
                        "cl-urgencia/CodeSystem/dau-destino-alta",
                        "display": "Domicilio",
                    }
                ]
            }
        }
        self.assertTrue(validate_encounter(enc))

    def test_with_destination_error(self):
        enc = build_abandonment_encounter(ABANDONMENT_DATA)
        enc["hospitalization"] = {
            "destination": {"reference": "Organization/ejemplo-establecimiento"}
        }
        self.assertTrue(validate_encounter(enc))

    def test_diagnosis_with_use_error(self):
        enc = build_abandonment_encounter(ABANDONMENT_DATA)
        enc["diagnosis"][0]["use"] = {
            "coding": [
                {
                    "code": "DD",
                    "system": "http://terminology.hl7.org/"
                    "CodeSystem/diagnosis-role",
                }
            ]
        }
        self.assertTrue(validate_encounter(enc))

    def test_missing_tipo_extension_error(self):
        enc = build_abandonment_encounter(ABANDONMENT_DATA)
        del enc["extension"]
        self.assertTrue(validate_encounter(enc))


if __name__ == "__main__":
    unittest.main()
