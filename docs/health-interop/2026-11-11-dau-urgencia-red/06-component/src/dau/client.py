"""Cliente FHIR del componente DAU (solo stdlib, ``urllib``).

El cliente NO construye recursos: recibe Bundles y peticiones ya
construidos por los módulos ``bundles``, ``search``, ``access`` e
``identity``, y los ejecuta contra el Bus / Repositorio FHIR.

- ``post_bundle(bundle)``: POST del Bundle transaccional al Bus.
- ``search(request)``: GET de una búsqueda construida por ``search.py``.
- ``get_pdf(request)``: GET autenticado del PDF (petición de
  ``access.py``); devuelve los bytes.
- ``post_subscription(subscription)``: POST de una Subscription FHIR.

Todos devuelven ``(status, cuerpo)``: el cuerpo es el JSON como dict
cuando la respuesta es JSON, o los bytes crudos en ``get_pdf``. Un
error HTTP (400, 412, 422, ...) NO lanza excepción: devuelve su status
y su OperationOutcome, para que ``responses.handle_bus_response`` lo
clasifique. Solo un fallo de red (sin respuesta del servidor) lanza
``URLError``.
"""

import json
import urllib.error
import urllib.request


class DauClient:
    """Cliente FHIR con autenticación Bearer opcional."""

    def __init__(self, base_url, token=None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _headers(self, content_type=None):
        headers = {"Accept": "application/fhir+json"}
        if content_type:
            headers["Content-Type"] = content_type
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        return headers

    def _request(self, method, url, body=None, content_type=None):
        request = urllib.request.Request(
            url,
            data=body,
            method=method,
            headers=self._headers(content_type),
        )
        try:
            with urllib.request.urlopen(request) as response:
                raw = response.read()
                return response.status, _parse_json(raw)
        except urllib.error.HTTPError as error:
            raw = error.read()
            return error.code, _parse_json(raw)

    def post_bundle(self, bundle):
        """POST del Bundle transaccional al Bus (base FHIR)."""
        payload = json.dumps(bundle, ensure_ascii=False).encode("utf-8")
        return self._request(
            "POST", self.base_url, payload, "application/fhir+json"
        )

    def search(self, request):
        """GET de una búsqueda (``{"method": "GET", "url": ...}``)."""
        url = "%s/%s" % (self.base_url, request["url"])
        return self._request(request.get("method", "GET"), url)

    def get_pdf(self, request):
        """GET autenticado del PDF; devuelve ``(status, bytes)``."""
        req = urllib.request.Request(
            request["url"],
            method=request.get("method", "GET"),
            headers=request.get("headers", {}),
        )
        try:
            with urllib.request.urlopen(req) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as error:
            return error.code, error.read()

    def post_subscription(self, subscription):
        """POST de una Subscription FHIR al Repositorio."""
        payload = json.dumps(
            subscription, ensure_ascii=False
        ).encode("utf-8")
        return self._request(
            "POST",
            self.base_url + "/Subscription",
            payload,
            "application/fhir+json",
        )


def _parse_json(raw):
    """JSON -> dict; si no es JSON, devuelve los bytes crudos."""
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return raw
