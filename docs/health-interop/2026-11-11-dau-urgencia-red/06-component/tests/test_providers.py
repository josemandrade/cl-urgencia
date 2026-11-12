"""Tests for dau.providers — Task 3, RED first."""

import unittest

from dau.providers import (
    build_organization,
    build_practitioner,
    validate_organization,
    validate_practitioner,
)

from tests.golden import assert_golden_equal

ORG_DATA = {"deis_code": "12345", "name": "Hospital de Prueba"}
PRACT_DATA = {"run": "98765432-5", "family": "González", "given": "María"}
ORG_PROFILE = (
    "https://josemandrade.github.io/cl-urgencia/"
    "StructureDefinition/dau-prestador-organizacional"
)
PRACT_PROFILE = (
    "https://josemandrade.github.io/cl-urgencia/"
    "StructureDefinition/dau-prestador-profesional"
)


class TestBuildOrganization(unittest.TestCase):
    def test_matches_golden(self):
        org = build_organization(ORG_DATA)
        self.assertEqual(org["meta"]["profile"], [ORG_PROFILE])
        self.assertNotIn("id", org)
        assert_golden_equal(
            self, org, "Organization-ejemplo-establecimiento.json"
        )

    def test_missing_name_rejected(self):
        with self.assertRaises(ValueError):
            build_organization({"deis_code": "12345"})

    def test_missing_deis_rejected(self):
        with self.assertRaises(ValueError):
            build_organization({"name": "Hospital de Prueba"})


class TestValidateOrganization(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(
            validate_organization(build_organization(ORG_DATA)), []
        )

    def test_missing_identifier(self):
        org = build_organization(ORG_DATA)
        del org["identifier"]
        self.assertTrue(validate_organization(org))

    def test_missing_name(self):
        org = build_organization(ORG_DATA)
        del org["name"]
        self.assertTrue(validate_organization(org))


class TestBuildPractitioner(unittest.TestCase):
    def test_matches_golden(self):
        # El RUN del golden (98765432-1) se normaliza a 98765432-5
        # (Ruling Task 2).
        pract = build_practitioner(PRACT_DATA)
        self.assertEqual(pract["meta"]["profile"], [PRACT_PROFILE])
        self.assertNotIn("id", pract)
        assert_golden_equal(
            self, pract, "Practitioner-ejemplo-profesional.json"
        )

    def test_invalid_run_rejected(self):
        with self.assertRaises(ValueError):
            build_practitioner({**PRACT_DATA, "run": "98765432-1"})


class TestValidatePractitioner(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(
            validate_practitioner(build_practitioner(PRACT_DATA)), []
        )

    def test_invalid_run_dv(self):
        pract = build_practitioner(PRACT_DATA)
        pract["identifier"][0]["value"] = "98765432-1"
        self.assertTrue(validate_practitioner(pract))

    def test_missing_identifier(self):
        pract = build_practitioner(PRACT_DATA)
        del pract["identifier"]
        self.assertTrue(validate_practitioner(pract))

    def test_missing_name(self):
        pract = build_practitioner(PRACT_DATA)
        del pract["name"]
        self.assertTrue(validate_practitioner(pract))


if __name__ == "__main__":
    unittest.main()
