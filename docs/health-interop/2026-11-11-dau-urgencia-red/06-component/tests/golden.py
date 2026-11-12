"""Comparación de recursos construidos contra los goldens de la guía.

Los goldens son copias textuales de los JSON compilados por SUSHI
(``tests/goldens/``) y NUNCA se editan. La comparación normaliza SOLO lo
documentado en las Rulings de ``state.md``:

- Se quitan ``id`` y ``meta`` del lado del golden (Ruling Task 10/11/12:
  los recursos se emiten sin ``Resource.id``; ``meta`` no se compara aquí
  — cada test la comprueba por separado contra la canónica del perfil).
- Se normaliza el RUN: 12345678-9 -> 12345678-5 y 98765432-1 -> 98765432-5
  (Ruling Task 2: los RUN de ejemplo de la guía tienen DV inválido; el DV
  calculado es 5 en ambos). La normalización recorre todos los valores de
  texto, incluidos los ``ifNoneExist`` de los Bundles.
- Para Condition, MedicationRequest y DocumentReference se añade el
  ``identifier`` local esperado (Ruling Task 7/8/9: el PUT condicional lo
  exige aunque el ejemplo de la guía no lo lleve), con el sistema de la
  guía y valor ``<DAU>-1`` (se pasa como ``local_id``).
- Para DocumentReference se añade ``contentType = application/pdf``
  (Ruling Task 9: el perfil lo fija, el ejemplo compilado lo omite).

Ninguna otra diferencia se normaliza: si el recurso construido difiere
del golden en cualquier otro campo, el test falla.
"""

import copy
import json
import os

GOLDENS_DIR = os.path.join(os.path.dirname(__file__), "goldens")

# Ruling Task 2 (state.md): RUN de ejemplo de la guía con DV inválido
# (DV calculado 5) -> RUN sintético del componente, con DV válido.
RUN_NORMALIZATIONS = {
    "12345678-9": "12345678-5",
    "98765432-1": "98765432-5",
}


def load_golden(name):
    """Carga un golden por nombre de archivo (sin editarlo)."""
    path = os.path.join(GOLDENS_DIR, name)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _walk_strings(obj, fn):
    if isinstance(obj, dict):
        return {k: _walk_strings(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_walk_strings(item, fn) for item in obj]
    if isinstance(obj, str):
        return fn(obj)
    return obj


def _normalize_run_strings(obj):
    """Ruling Task 2: sustituye los RUN de la guía por los del componente."""

    def _replace(text):
        for old, new in RUN_NORMALIZATIONS.items():
            text = text.replace(old, new)
        return text

    return _walk_strings(obj, _replace)


def _strip_id_meta(obj):
    """Quita ``id`` y ``meta`` en todos los niveles (lado del golden).

    Ruling Task 10/11/12: los recursos se emiten sin ``Resource.id`` y los
    goldens se comparan con ``id`` quitado. ``meta`` tampoco se compara:
    cada test comprueba ``meta.profile`` por separado.
    """
    if isinstance(obj, dict):
        return {
            k: _strip_id_meta(v)
            for k, v in obj.items()
            if k not in ("id", "meta")
        }
    if isinstance(obj, list):
        return [_strip_id_meta(item) for item in obj]
    return obj


def normalize_golden(resource, local_id=None, local_system=None):
    """Devuelve una copia normalizada del golden, lista para comparar.

    ``local_id``/``local_system``: identificador local que el builder añade
    (Ruling Task 7/8/9); solo se añade si el golden no lleva ``identifier``.
    """
    golden = copy.deepcopy(resource)
    golden = _strip_id_meta(golden)
    golden = _normalize_run_strings(golden)
    if local_id is not None and "identifier" not in golden:
        # Ruling Task 7/8/9: PUT condicional exige identifier local.
        golden["identifier"] = [{"system": local_system, "value": local_id}]
    if golden.get("resourceType") == "DocumentReference":
        # Ruling Task 9: el perfil fija contentType = application/pdf.
        for content in golden.get("content", []):
            attachment = content.get("attachment", {})
            attachment.setdefault("contentType", "application/pdf")
    return golden


def assert_golden_equal(testcase, built, golden_name, local_id=None,
                        local_system=None):
    """Compara el recurso construido con su golden normalizado.

    El lado del recurso construido se compara sin ``id`` (el contrato dice
    que los builders no lo emiten) y sin ``meta`` (se comprueba aparte).
    """
    golden = normalize_golden(
        load_golden(golden_name),
        local_id=local_id,
        local_system=local_system,
    )
    built_cmp = _strip_id_meta(copy.deepcopy(built))
    testcase.assertEqual(built_cmp, golden)


def _parse_local_id_from_put_url(url):
    """``<Tipo>?identifier=<sistema>|<valor>`` -> (sistema, valor)."""
    if "identifier=" not in url:
        return None
    ident = url.split("identifier=", 1)[1]
    system, _, value = ident.partition("|")
    return system, value


def normalize_bundle_golden(bundle):
    """Normaliza un golden de Bundle para compararlo con el construido.

    Reescribe las referencias lógicas (``Tipo/ejemplo-...``) a los
    ``fullUrl urn:uuid:`` de las entradas del propio Bundle (Ruling Task
    10/11/12: el ensamblador reescribe las referencias internas; las
    referencias a recursos que NO son entradas del Bundle quedan lógicas,
    como en el ejemplo compilado). Además aplica, por entrada, las
    normalizaciones de ``normalize_golden`` (RUN, ``id``/``meta``,
    identificador local del PUT condicional y ``contentType``).
    """
    golden = copy.deepcopy(bundle)
    ref_map = {}
    for entry in golden.get("entry", []):
        resource = entry.get("resource", {})
        logical = "%s/%s" % (
            resource.get("resourceType"), resource.get("id")
        )
        ref_map[logical] = entry.get("fullUrl")

    def _rewrite(obj):
        if isinstance(obj, dict):
            if set(obj.keys()) == {"reference"} \
                    and obj["reference"] in ref_map:
                return {"reference": ref_map[obj["reference"]]}
            return {k: _rewrite(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_rewrite(item) for item in obj]
        return obj

    golden = _strip_id_meta(golden)
    golden = _normalize_run_strings(golden)
    golden = _rewrite(golden)
    for entry in golden.get("entry", []):
        resource = entry.get("resource", {})
        request = entry.get("request", {})
        parsed = None
        if request.get("method") == "PUT":
            parsed = _parse_local_id_from_put_url(
                request.get("url", "")
            )
        entry["resource"] = normalize_golden(
            resource,
            local_id=parsed[1] if parsed else None,
            local_system=parsed[0] if parsed else None,
        )
    return golden


def assert_bundle_golden_equal(testcase, built, golden_name):
    """Compara el Bundle construido con su golden normalizado.

    El lado construido se compara sin ``id``/``meta`` (``meta.profile``
    del Bundle se comprueba aparte); el orden de las entradas debe
    coincidir con el del golden.
    """
    golden = normalize_bundle_golden(load_golden(golden_name))
    built_cmp = _strip_id_meta(copy.deepcopy(built))
    testcase.assertEqual(built_cmp, golden)
