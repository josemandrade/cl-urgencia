"""Tests for dau.bundles — Tasks 10, 11 y 12, RED first."""

import unittest

from dau.bundles import (
    build_abandonment_bundle,
    build_admission_bundle,
    build_discharge_bundle,
)
from dau.conditions import validate_condition
from dau.documents import validate_document_reference
from dau.encounters import validate_encounter
from dau.medications import validate_medication_request
from dau.patients import validate_patient
from dau.providers import validate_organization, validate_practitioner

from tests.golden import assert_bundle_golden_equal

PATIENT_DATA = {
    "run": "12345678-5",
    "family": "Pérez",
    "given": "Juan",
    "gender": "male",
    "birth_date": "1980-05-15",
}

ORGANIZATION_DATA = {"deis_code": "12345", "name": "Hospital de Prueba"}

PRACTITIONER_DATA = {
    "run": "98765432-5",
    "family": "González",
    "given": "María",
}

ENCOUNTER_BASE = {
    "dau_id": "SYN-URG-001",
    "deis_code": "12345",
    "period_start": "2026-11-11T10:05:00-03:00",
    "attender_start": "2026-11-11T10:15:00-03:00",
    "reason": "Dolor torácico",
}

ADMISSION_INPUT = {
    "patient": PATIENT_DATA,
    "organization": ORGANIZATION_DATA,
    "practitioner": PRACTITIONER_DATA,
    "encounter": dict(ENCOUNTER_BASE),
    "timestamp": "2026-11-11T10:05:00-03:00",
}

ADMISSION_UUIDS = {
    "patient": "11111111-1111-1111-1111-111111111111",
    "organization": "22222222-2222-2222-2222-222222222222",
    "practitioner": "33333333-3333-3333-3333-333333333333",
    "encounter": "44444444-4444-4444-4444-444444444444",
}

CONDITION_EGRESO = {
    "clinical_status": "active",
    "verification_status": "confirmed",
    "code": "I46.9",
    "code_system": "http://hl7.org/fhir/sid/icd-10",
    "code_display": "Paro cardíaco, no especificado",
    "recorded_date": "2026-11-11T14:20:00-03:00",
    "local_id": "SYN-URG-001-1",
}

MEDICATION_DATA = {
    "medication_text": "Paracetamol 500 mg",
    "dosage_text": "1 comprimido cada 8 horas por 5 días",
    "local_id": "SYN-URG-001-1",
}

DOCUMENT_ALTA = {
    "type_code": "59258-4",
    "url": "https://his.ejemplo.cl/dau/SYN-URG-001.pdf",
    "date": "2026-11-11T14:25:00-03:00",
    "local_id": "SYN-URG-001-1",
}

DISCHARGE_INPUT = {
    "patient": PATIENT_DATA,
    "organization": ORGANIZATION_DATA,
    "practitioner": PRACTITIONER_DATA,
    "encounter": {
        **ENCOUNTER_BASE,
        "period_end": "2026-11-11T14:20:00-03:00",
        "destino": "03",
    },
    "condition": CONDITION_EGRESO,
    "medication": MEDICATION_DATA,
    "document": DOCUMENT_ALTA,
    "timestamp": "2026-11-11T14:25:00-03:00",
}

DISCHARGE_UUIDS = {
    "encounter": "44444444-4444-4444-4444-444444444444",
    "condition": "55555555-5555-5555-5555-555555555555",
    "medication": "66666666-6666-6666-6666-666666666666",
    "document": "77777777-7777-7777-7777-777777777777",
}

CONDITION_HIPOTESIS = {
    "clinical_status": "active",
    "verification_status": "provisional",
    "code": "R07.4",
    "code_system": "http://hl7.org/fhir/sid/icd-10",
    "code_display": "Dolor en el pecho, no especificado",
    "recorded_date": "2026-11-11T11:00:00-03:00",
    "local_id": "SYN-URG-002-1",
}

DOCUMENT_ABANDONO = {
    "type_code": "34111-5",
    "url": "https://his.ejemplo.cl/dau/SYN-URG-002.pdf",
    "date": "2026-11-11T11:35:00-03:00",
    "local_id": "SYN-URG-002-1",
}

ABANDONMENT_INPUT = {
    "patient": PATIENT_DATA,
    "organization": ORGANIZATION_DATA,
    "practitioner": PRACTITIONER_DATA,
    "encounter": {
        **ENCOUNTER_BASE,
        "dau_id": "SYN-URG-002",
        "period_end": "2026-11-11T11:30:00-03:00",
        "tipo": "2",
    },
    "condition": CONDITION_HIPOTESIS,
    "document": DOCUMENT_ABANDONO,
    "timestamp": "2026-11-11T11:35:00-03:00",
}

ABANDONMENT_UUIDS = {
    "encounter": "88888888-8888-8888-8888-888888888888",
    "condition": "99999999-9999-9999-9999-999999999999",
    "document": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
}

BUNDLE_PROFILE = (
    "https://josemandrade.github.io/cl-urgencia/"
    "StructureDefinition/dau-bundle-aviso"
)


def _references(obj):
    """Todas las cadenas en campos ``reference`` de un Bundle."""
    found = []
    if isinstance(obj, dict):
        if set(obj.keys()) == {"reference"}:
            found.append(obj["reference"])
        else:
            for value in obj.values():
                found.extend(_references(value))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(_references(item))
    return found


class TestAdmissionBundle(unittest.TestCase):
    def test_matches_golden(self):
        bundle = build_admission_bundle(ADMISSION_INPUT, ADMISSION_UUIDS)
        self.assertEqual(bundle["resourceType"], "Bundle")
        self.assertEqual(bundle["type"], "transaction")
        self.assertEqual(bundle["meta"]["profile"], [BUNDLE_PROFILE])
        assert_bundle_golden_equal(
            self, bundle, "Bundle-ejemplo-bundle-admision.json"
        )

    def test_no_id_in_bundle_or_resources(self):
        bundle = build_admission_bundle(ADMISSION_INPUT, ADMISSION_UUIDS)
        self.assertNotIn("id", bundle)
        for entry in bundle["entry"]:
            self.assertNotIn("id", entry["resource"])

    def test_no_logical_reference_to_an_entry(self):
        # Ruling Task 10/11/12: las referencias internas van por fullUrl.
        bundle = build_admission_bundle(ADMISSION_INPUT, ADMISSION_UUIDS)
        refs = _references(bundle)
        self.assertNotIn("Patient/ejemplo-paciente", refs)
        self.assertNotIn("Organization/ejemplo-establecimiento", refs)
        self.assertNotIn("Practitioner/ejemplo-profesional", refs)
        self.assertIn(
            "urn:uuid:11111111-1111-1111-1111-111111111111", refs
        )

    def test_entry_requests(self):
        bundle = build_admission_bundle(ADMISSION_INPUT, ADMISSION_UUIDS)
        requests = [e["request"] for e in bundle["entry"]]
        self.assertEqual(
            requests[0],
            {
                "method": "POST",
                "url": "Patient",
                "ifNoneExist": (
                    "identifier=urn:oid:2.16.840.1.113883.2.22.1.152"
                    ".787300|12345678-5"
                ),
            },
        )
        self.assertEqual(
            requests[3],
            {
                "method": "PUT",
                "url": (
                    "Encounter?identifier=https://interoperabilidad"
                    ".minsal.cl/fhir/sid/dau/12345|SYN-URG-001"
                ),
            },
        )

    def test_default_uuids_are_generated(self):
        bundle = build_admission_bundle(ADMISSION_INPUT)
        full_urls = [e["fullUrl"] for e in bundle["entry"]]
        self.assertEqual(len(set(full_urls)), 4)
        for full_url in full_urls:
            self.assertTrue(full_url.startswith("urn:uuid:"))
            self.assertEqual(len(full_url), len("urn:uuid:") + 36)

    def test_resources_validate(self):
        bundle = build_admission_bundle(ADMISSION_INPUT, ADMISSION_UUIDS)
        resources = {
            e["resource"]["resourceType"]: e["resource"]
            for e in bundle["entry"]
        }
        self.assertEqual(validate_patient(resources["Patient"]), [])
        self.assertEqual(
            validate_organization(resources["Organization"]), []
        )
        self.assertEqual(
            validate_practitioner(resources["Practitioner"]), []
        )
        self.assertEqual(validate_encounter(resources["Encounter"]), [])


class TestDischargeBundle(unittest.TestCase):
    def test_matches_golden(self):
        bundle = build_discharge_bundle(DISCHARGE_INPUT, DISCHARGE_UUIDS)
        self.assertEqual(bundle["type"], "transaction")
        self.assertEqual(bundle["meta"]["profile"], [BUNDLE_PROFILE])
        assert_bundle_golden_equal(
            self, bundle, "Bundle-ejemplo-bundle-alta.json"
        )

    def test_without_medication_has_3_entries(self):
        data = {k: v for k, v in DISCHARGE_INPUT.items()
                if k != "medication"}
        bundle = build_discharge_bundle(data, DISCHARGE_UUIDS)
        self.assertEqual(len(bundle["entry"]), 3)
        self.assertEqual(
            [e["resource"]["resourceType"] for e in bundle["entry"]],
            ["Encounter", "Condition", "DocumentReference"],
        )

    def test_no_id_and_internal_references_rewritten(self):
        bundle = build_discharge_bundle(DISCHARGE_INPUT, DISCHARGE_UUIDS)
        self.assertNotIn("id", bundle)
        for entry in bundle["entry"]:
            self.assertNotIn("id", entry["resource"])
        refs = _references(bundle)
        self.assertNotIn("Condition/ejemplo-diagnostico-egreso", refs)
        self.assertNotIn("Encounter/ejemplo-encuentro-alta", refs)
        self.assertIn(
            "urn:uuid:55555555-5555-5555-5555-555555555555", refs
        )

    def test_resources_validate(self):
        bundle = build_discharge_bundle(DISCHARGE_INPUT, DISCHARGE_UUIDS)
        resources = {
            e["resource"]["resourceType"]: e["resource"]
            for e in bundle["entry"]
        }
        self.assertEqual(validate_encounter(resources["Encounter"]), [])
        self.assertEqual(validate_condition(resources["Condition"]), [])
        self.assertEqual(
            validate_medication_request(resources["MedicationRequest"]),
            [],
        )
        self.assertEqual(
            validate_document_reference(
                resources["DocumentReference"]
            ),
            [],
        )


class TestAbandonmentBundle(unittest.TestCase):
    def test_matches_golden(self):
        bundle = build_abandonment_bundle(
            ABANDONMENT_INPUT, ABANDONMENT_UUIDS
        )
        self.assertEqual(bundle["type"], "transaction")
        self.assertEqual(bundle["meta"]["profile"], [BUNDLE_PROFILE])
        assert_bundle_golden_equal(
            self, bundle, "Bundle-ejemplo-bundle-abandono.json"
        )

    def test_no_discharge_disposition(self):
        bundle = build_abandonment_bundle(
            ABANDONMENT_INPUT, ABANDONMENT_UUIDS
        )
        encounter = bundle["entry"][0]["resource"]
        self.assertEqual(encounter["resourceType"], "Encounter")
        self.assertNotIn("hospitalization", encounter)

    def test_resources_validate(self):
        bundle = build_abandonment_bundle(
            ABANDONMENT_INPUT, ABANDONMENT_UUIDS
        )
        resources = {
            e["resource"]["resourceType"]: e["resource"]
            for e in bundle["entry"]
        }
        self.assertEqual(validate_encounter(resources["Encounter"]), [])
        self.assertEqual(validate_condition(resources["Condition"]), [])
        self.assertEqual(
            validate_document_reference(
                resources["DocumentReference"]
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
