"""PI-3: petición de descarga del PDF del DAU.

El PDF se obtiene por `DocumentReference.content.attachment.url`, con
autenticación (operations.md PI-3; MHD parcial, ITI-68 como patrón). El
mecanismo no es una transacción ITI-68: es un GET autenticado directo a
la URL del DocumentReference. Este módulo solo construye la petición;
no hace la llamada HTTP (eso es Task 21, client.py).
"""


def build_pdf_download(document_reference: dict, token: str) -> dict:
    """GET autenticado al `attachment.url` del DocumentReference.

    Devuelve ``{"method": "GET", "url": <attachment.url>, "headers":
    {"Authorization": "Bearer <token>"}}``. Sin `attachment.url` ->
    ValueError; sin token (vacío o None) -> ValueError.
    """
    if not token:
        raise ValueError("token de autenticación vacío")
    content = document_reference.get("content") or []
    url = None
    if content:
        url = (content[0].get("attachment") or {}).get("url")
    if not url:
        raise ValueError("DocumentReference sin content.attachment.url")
    return {"method": "GET", "url": url, "headers": {"Authorization": f"Bearer {token}"}}
