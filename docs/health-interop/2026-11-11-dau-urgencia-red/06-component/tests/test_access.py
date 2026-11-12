"""Tests for dau.access (PI-3 PDF download) — Task 19, RED first."""

import unittest

from dau.access import build_pdf_download

# DocumentReference sintéticos con las mismas attachment.url que los
# goldens de la guía (DocumentReference-ejemplo-documento-alta.json y
# ...-abandono.json).
DOC_ALTA = {
    "resourceType": "DocumentReference",
    "status": "current",
    "content": [{"attachment": {"url": "https://his.ejemplo.cl/dau/SYN-URG-001.pdf"}}],
}

DOC_ABANDONO = {
    "resourceType": "DocumentReference",
    "status": "current",
    "content": [{"attachment": {"url": "https://his.ejemplo.cl/dau/SYN-URG-002.pdf"}}],
}


class TestBuildPdfDownload(unittest.TestCase):
    def test_discharge_document(self):
        self.assertEqual(
            build_pdf_download(DOC_ALTA, "token-sintetico"),
            {
                "method": "GET",
                "url": "https://his.ejemplo.cl/dau/SYN-URG-001.pdf",
                "headers": {"Authorization": "Bearer token-sintetico"},
            },
        )

    def test_abandonment_document(self):
        self.assertEqual(
            build_pdf_download(DOC_ABANDONO, "token-sintetico"),
            {
                "method": "GET",
                "url": "https://his.ejemplo.cl/dau/SYN-URG-002.pdf",
                "headers": {"Authorization": "Bearer token-sintetico"},
            },
        )

    def test_missing_attachment_url_raises(self):
        no_url = {"resourceType": "DocumentReference", "content": [{"attachment": {}}]}
        with self.assertRaises(ValueError):
            build_pdf_download(no_url, "token-sintetico")
        no_content = {"resourceType": "DocumentReference", "content": []}
        with self.assertRaises(ValueError):
            build_pdf_download(no_content, "token-sintetico")
        no_content_key = {"resourceType": "DocumentReference"}
        with self.assertRaises(ValueError):
            build_pdf_download(no_content_key, "token-sintetico")

    def test_missing_token_raises(self):
        with self.assertRaises(ValueError):
            build_pdf_download(DOC_ALTA, "")
        with self.assertRaises(ValueError):
            build_pdf_download(DOC_ALTA, None)


if __name__ == "__main__":
    unittest.main()
