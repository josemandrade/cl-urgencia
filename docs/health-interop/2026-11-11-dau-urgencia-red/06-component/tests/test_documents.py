"""Tests for dau.documents (DAUDocumentoUrgencia) — Task 9, RED first."""

import unittest

from dau.constants import LOCAL_ID_SYSTEMS
from dau.documents import build_document_reference, validate_document_reference

from tests.golden import assert_golden_equal

ALTA_DATA = {
    "type_code": "59258-4",
    "subject": "Patient/ejemplo-paciente",
    "encounter": "Encounter/ejemplo-encuentro-alta",
    "url": "https://his.ejemplo.cl/dau/SYN-URG-001.pdf",
    "date": "2026-11-11T14:25:00-03:00",
    "local_id": "SYN-URG-001-1",
}

ABANDONO_DATA = {
    "type_code": "34111-5",
    "subject": "Patient/ejemplo-paciente",
    "encounter": "Encounter/ejemplo-encuentro-abandono",
    "url": "https://his.ejemplo.cl/dau/SYN-URG-002.pdf",
    "date": "2026-11-11T11:35:00-03:00",
    "local_id": "SYN-URG-002-1",
}

PROFILE = (
    "https://josemandrade.github.io/cl-urgencia/"
    "StructureDefinition/dau-documento-urgencia"
)


class TestBuildDocumentReference(unittest.TestCase):
    def test_alta_matches_golden(self):
        # Coincide con el golden salvo id/meta, el identificador local
        # (Ruling Task 7/8/9) y el contentType (Ruling Task 9).
        doc = build_document_reference(ALTA_DATA)
        self.assertEqual(doc["meta"]["profile"], [PROFILE])
        self.assertNotIn("id", doc)
        self.assertEqual(doc["status"], "current")
        assert_golden_equal(
            self, doc, "DocumentReference-ejemplo-documento-alta.json",
            local_id="SYN-URG-001-1",
            local_system=LOCAL_ID_SYSTEMS["documento"],
        )

    def test_abandono_matches_golden(self):
        doc = build_document_reference(ABANDONO_DATA)
        assert_golden_equal(
            self, doc, "DocumentReference-ejemplo-documento-abandono.json",
            local_id="SYN-URG-002-1",
            local_system=LOCAL_ID_SYSTEMS["documento"],
        )

    def test_content_type_always_pdf(self):
        # Ruling Task 9: el perfil fija contentType = application/pdf.
        for data in (ALTA_DATA, ABANDONO_DATA):
            doc = build_document_reference(data)
            self.assertEqual(
                doc["content"][0]["attachment"]["contentType"],
                "application/pdf",
            )

    def test_local_identifier_included(self):
        doc = build_document_reference(ALTA_DATA)
        self.assertEqual(
            doc["identifier"],
            [
                {
                    "system": LOCAL_ID_SYSTEMS["documento"],
                    "value": "SYN-URG-001-1",
                }
            ],
        )

    def test_invalid_loinc_rejected(self):
        with self.assertRaises(ValueError):
            build_document_reference({**ALTA_DATA, "type_code": "12345-6"})

    def test_missing_url_rejected(self):
        with self.assertRaises(ValueError):
            build_document_reference(
                {k: v for k, v in ALTA_DATA.items() if k != "url"}
            )


class TestValidateDocumentReference(unittest.TestCase):
    def test_valid_alta(self):
        self.assertEqual(
            validate_document_reference(build_document_reference(ALTA_DATA)),
            [],
        )

    def test_valid_abandono(self):
        self.assertEqual(
            validate_document_reference(
                build_document_reference(ABANDONO_DATA)
            ),
            [],
        )

    def test_other_loinc_error(self):
        doc = build_document_reference(ALTA_DATA)
        doc["type"]["coding"][0]["code"] = "34133-9"
        self.assertTrue(validate_document_reference(doc))

    def test_missing_content_type_error(self):
        doc = build_document_reference(ALTA_DATA)
        del doc["content"][0]["attachment"]["contentType"]
        self.assertTrue(validate_document_reference(doc))

    def test_wrong_content_type_error(self):
        doc = build_document_reference(ALTA_DATA)
        doc["content"][0]["attachment"]["contentType"] = "text/html"
        self.assertTrue(validate_document_reference(doc))

    def test_missing_url_error(self):
        doc = build_document_reference(ALTA_DATA)
        del doc["content"][0]["attachment"]["url"]
        self.assertTrue(validate_document_reference(doc))

    def test_missing_encounter_error(self):
        doc = build_document_reference(ALTA_DATA)
        del doc["context"]["encounter"]
        self.assertTrue(validate_document_reference(doc))

    def test_missing_date_error(self):
        doc = build_document_reference(ALTA_DATA)
        del doc["date"]
        self.assertTrue(validate_document_reference(doc))


if __name__ == "__main__":
    unittest.main()
