"""Tests for dau.search (PI-2 queries + Subscription) — Tasks 14–18, RED first."""

import unittest

from dau.search import (
    build_condition_search,
    build_document_search,
    build_encounter_search_by_patient,
    build_encounter_search_by_provider,
    build_encounter_subscription,
    build_patient_search,
)


class TestBuildPatientSearch(unittest.TestCase):
    def test_exact_url(self):
        # operations.md PI-2: GET /Patient?identifier=<sistema RUN>|<RUN>.
        self.assertEqual(
            build_patient_search("12345678-5"),
            {
                "method": "GET",
                "url": (
                    "Patient?identifier="
                    "urn:oid:2.16.840.1.113883.2.22.1.152.787300|12345678-5"
                ),
            },
        )

    def test_invalid_run_raises_before_building(self):
        # RUN con DV inválido -> error antes de construir la consulta.
        with self.assertRaises(ValueError):
            build_patient_search("12345678-9")
        with self.assertRaises(ValueError):
            build_patient_search("98765432-1")


class TestBuildEncounterSearch(unittest.TestCase):
    def test_by_patient_exact_url(self):
        # operations.md PI-2: GET /Encounter?patient.identifier=...&class=EMER.
        self.assertEqual(
            build_encounter_search_by_patient("12345678-5"),
            {
                "method": "GET",
                "url": (
                    "Encounter?patient.identifier="
                    "urn:oid:2.16.840.1.113883.2.22.1.152.787300|12345678-5"
                    "&class=EMER"
                ),
            },
        )

    def test_by_patient_invalid_run_raises(self):
        with self.assertRaises(ValueError):
            build_encounter_search_by_patient("12345678-9")

    def test_by_provider_exact_url(self):
        # operations.md PI-2: pacientes actualmente en urgencia en un
        # establecimiento.
        self.assertEqual(
            build_encounter_search_by_provider("12345"),
            {
                "method": "GET",
                "url": (
                    "Encounter?service-provider.identifier="
                    "https://interoperabilidad.minsal.cl/fhir/ig/tei/"
                    "CodeSystem/CSEstablecimientoDestino|12345"
                    "&class=EMER&status=arrived"
                ),
            },
        )

    def test_by_provider_empty_code_raises(self):
        with self.assertRaises(ValueError):
            build_encounter_search_by_provider("")


class TestBuildConditionSearch(unittest.TestCase):
    def test_exact_url(self):
        # operations.md PI-2: GET /Condition?encounter=Encounter/[id].
        self.assertEqual(
            build_condition_search("SYN-URG-001"),
            {
                "method": "GET",
                "url": "Condition?encounter=Encounter/SYN-URG-001",
            },
        )

    def test_empty_encounter_id_raises(self):
        with self.assertRaises(ValueError):
            build_condition_search("")
        with self.assertRaises(ValueError):
            build_condition_search(None)


class TestBuildDocumentSearch(unittest.TestCase):
    def test_exact_url(self):
        # operations.md PI-2: GET /DocumentReference?encounter=Encounter/[id].
        self.assertEqual(
            build_document_search("SYN-URG-001"),
            {
                "method": "GET",
                "url": "DocumentReference?encounter=Encounter/SYN-URG-001",
            },
        )

    def test_empty_encounter_id_raises(self):
        with self.assertRaises(ValueError):
            build_document_search("")
        with self.assertRaises(ValueError):
            build_document_search(None)


class TestBuildEncounterSubscription(unittest.TestCase):
    def test_rest_hook_subscription(self):
        # operations.md PI-2: Subscription FHIR sobre Encounter class=EMER
        # (sin perfil IHE: no es DSUB). El canal es un detalle de
        # implementación y se pasa como parámetro.
        self.assertEqual(
            build_encounter_subscription(
                "rest-hook", "https://red.ejemplo.cl/fhir/notify"
            ),
            {
                "resourceType": "Subscription",
                "status": "requested",
                "criteria": "Encounter?class=EMER",
                "channel": {
                    "type": "rest-hook",
                    "endpoint": "https://red.ejemplo.cl/fhir/notify",
                },
            },
        )

    def test_unsupported_channel_raises(self):
        # Canal no soportado (p. ej. email) -> error explícito.
        with self.assertRaises(ValueError):
            build_encounter_subscription("email", "a@ejemplo.cl")

    def test_empty_endpoint_raises(self):
        with self.assertRaises(ValueError):
            build_encounter_subscription("rest-hook", "")


if __name__ == "__main__":
    unittest.main()
