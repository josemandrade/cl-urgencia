"""Tests for dau.client and dau.cli — Task 21, RED first."""

import json
import os
import subprocess
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from dau.client import DauClient

HERE = os.path.dirname(__file__)
COMPONENT_DIR = os.path.dirname(HERE)


class _MockHandler(BaseHTTPRequestHandler):
    """Mock del Bus/Repositorio: registra la petición y responde."""

    requests = []

    def _record(self, body=b""):
        _MockHandler.requests.append(
            {
                "method": self.command,
                "path": self.path,
                "authorization": self.headers.get("Authorization"),
                "content_type": self.headers.get("Content-Type"),
                "body": body,
            }
        )

    def _send_json(self, status, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/fhir+json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        self._record(body)
        if "force400" in self.path:
            self._send_json(
                400,
                {
                    "resourceType": "OperationOutcome",
                    "issue": [
                        {
                            "severity": "error",
                            "code": "invalid",
                            "diagnostics": "El recurso no es válido",
                        }
                    ],
                },
            )
        elif self.path.endswith("/Subscription"):
            self._send_json(
                201,
                {"resourceType": "Subscription", "status": "requested"},
            )
        else:
            self._send_json(
                200,
                {"resourceType": "Bundle", "type": "transaction-response"},
            )

    def do_GET(self):
        self._record()
        if "force400" in self.path:
            self._send_json(
                400,
                {
                    "resourceType": "OperationOutcome",
                    "issue": [{"severity": "error", "code": "invalid"}],
                },
            )
        elif self.path.endswith(".pdf"):
            data = b"%PDF-1.4 sintetico"
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self._send_json(
                200,
                {
                    "resourceType": "Bundle",
                    "type": "searchset",
                    "total": 1,
                },
            )

    def log_message(self, *args):
        pass


class TestDauClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), _MockHandler
        )
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(
            target=cls.server.serve_forever, daemon=True
        )
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        _MockHandler.requests.clear()

    def _client(self):
        return DauClient(
            "http://127.0.0.1:%d/fhir" % self.port,
            token="token-sintetico",
        )

    def test_post_bundle_sends_json_with_auth(self):
        client = self._client()
        with open(
            os.path.join(
                HERE, "goldens", "Bundle-ejemplo-bundle-admision.json"
            ),
            encoding="utf-8",
        ) as fh:
            bundle = json.load(fh)
        status, body = client.post_bundle(bundle)
        self.assertEqual(status, 200)
        self.assertEqual(body["type"], "transaction-response")
        request = _MockHandler.requests[0]
        self.assertEqual(request["method"], "POST")
        self.assertEqual(request["path"], "/fhir")
        self.assertEqual(
            request["authorization"], "Bearer token-sintetico"
        )
        self.assertEqual(
            request["content_type"], "application/fhir+json"
        )
        self.assertEqual(
            json.loads(request["body"])["type"], "transaction"
        )

    def test_search_gets_exact_url_with_auth(self):
        client = self._client()
        status, body = client.search(
            {
                "method": "GET",
                "url": (
                    "Patient?identifier=urn:oid:2.16.840.1.113883"
                    ".2.22.1.152.787300|12345678-5"
                ),
            }
        )
        self.assertEqual(status, 200)
        self.assertEqual(body["type"], "searchset")
        request = _MockHandler.requests[0]
        self.assertEqual(request["method"], "GET")
        self.assertIn("Patient?identifier=", request["path"])
        self.assertEqual(
            request["authorization"], "Bearer token-sintetico"
        )

    def test_http_error_returns_status_and_body(self):
        client = self._client()
        status, body = client.search(
            {"method": "GET", "url": "Patient?force400=1"}
        )
        self.assertEqual(status, 400)
        self.assertEqual(body["resourceType"], "OperationOutcome")

    def test_get_pdf_returns_bytes(self):
        client = self._client()
        status, data = client.get_pdf(
            {
                "method": "GET",
                "url": "http://127.0.0.1:%d/dau/SYN-URG-001.pdf"
                % self.port,
                "headers": {"Authorization": "Bearer token-sintetico"},
            }
        )
        self.assertEqual(status, 200)
        self.assertTrue(data.startswith(b"%PDF"))

    def test_no_token_no_authorization_header(self):
        client = DauClient(
            "http://127.0.0.1:%d/fhir" % self.port
        )
        client.search({"method": "GET", "url": "Patient?identifier=x"})
        self.assertIsNone(_MockHandler.requests[0]["authorization"])


def _run_cli(*args):
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.join(COMPONENT_DIR, "src")
    return subprocess.run(
        [sys.executable, "-m", "dau.cli", *args],
        cwd=COMPONENT_DIR,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestCli(unittest.TestCase):
    def _example(self, name):
        return os.path.join(COMPONENT_DIR, "examples", name)

    def test_bundles_from_examples(self):
        cases = [
            ("admission-bundle", "admission-bundle.json", 4),
            ("discharge-bundle", "discharge-bundle.json", 4),
            ("abandonment-bundle", "abandonment-bundle.json", 3),
        ]
        for operation, example, entries in cases:
            with self.subTest(operation=operation):
                proc = _run_cli(operation, self._example(example))
                self.assertEqual(proc.returncode, 0, proc.stderr)
                result = json.loads(proc.stdout)
                self.assertEqual(result["type"], "transaction")
                self.assertEqual(len(result["entry"]), entries)

    def test_searches_from_examples(self):
        cases = [
            (
                "patient-search",
                "patient-search.json",
                "Patient?identifier=",
            ),
            (
                "encounter-search-by-patient",
                "encounter-search-by-patient.json",
                "Encounter?patient.identifier=",
            ),
            (
                "encounter-search-by-provider",
                "encounter-search-by-provider.json",
                "Encounter?service-provider.identifier=",
            ),
            (
                "condition-search",
                "condition-search.json",
                "Condition?encounter=Encounter/SYN-URG-001",
            ),
            (
                "document-search",
                "document-search.json",
                "DocumentReference?encounter=Encounter/SYN-URG-001",
            ),
        ]
        for operation, example, prefix in cases:
            with self.subTest(operation=operation):
                proc = _run_cli(operation, self._example(example))
                self.assertEqual(proc.returncode, 0, proc.stderr)
                result = json.loads(proc.stdout)
                self.assertEqual(result["method"], "GET")
                self.assertTrue(
                    result["url"].startswith(prefix), result["url"]
                )

    def test_subscription_pdf_and_identity_from_examples(self):
        proc = _run_cli("subscription", self._example("subscription.json"))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["resourceType"], "Subscription")
        self.assertEqual(result["criteria"], "Encounter?class=EMER")

        proc = _run_cli(
            "pdf-download", self._example("pdf-download.json")
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["method"], "GET")
        self.assertTrue(result["url"].endswith("SYN-URG-001.pdf"))
        self.assertEqual(
            result["headers"]["Authorization"],
            "Bearer token-sintetico",
        )

        proc = _run_cli(
            "resolve-identity", self._example("resolve-identity.json")
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), "resolved")

    def test_unknown_operation_fails(self):
        proc = _run_cli("no-existe", self._example("patient-search.json"))
        self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
