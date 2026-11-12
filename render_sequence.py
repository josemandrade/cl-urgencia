#!/usr/bin/env python3
"""Render the sequence diagrams for the DAU case as SVG (one per flow),
following the pack's sequence-diagrams skill: every message names the
operation that carries it (operation id, FHIR interaction, IHE profile
when one applies); solid arrow = synchronous, open arrow = asynchronous,
dashed arrow = return with the outcome; alt/opt fragments for the
branches; a note where a rule constrains the flow.

Usage: python3 render_sequence.py [--check]
Default: writes the 5 SVGs to the case folder and the 5 PNGs (2x) to the
guide's input/images/.
--check: verify the operation-reference rule mechanically (every message
names an operation from the proposal; every operation appears in at
least one diagram) and exit without writing files.

Flows (from the BPMN v7 paths, not invented): admission, discharge,
abandonment, network-pull, document-retrieval.

Readability rules (same hard gate as render_bpmn.py):
- Messages are horizontal, lifelines are vertical: no diagonals, ever.
- Message labels are short (operation id + interaction, at most 2
  lines); the detail lives in the operation table under the diagram
  (04-sequence-diagrams.md), not on the arrow.
- Labels get a white pill behind them so they stay readable where
  they cross a lifeline. The two lines of a label sit 19 px apart,
  so their pills (18 px tall) never overlap each other.
- A fragment tab must clear the first message's label: the tab sits
  70 px above the first arrow, and the separator guard is left-anchored
  inside the fragment, never centred on a fixed offset (a centred guard
  spills out of a narrow fragment, and a tab that overlaps a label pill
  hides the end of its own guard text).
- The cairosvg default font has no U+2192 (rightwards arrow): write
  ">" in subtitles, or the arrows render as empty boxes.
- Render the PNG at 2x the SVG size and LOOK at it at display size,
  by zones, before shipping. A diagram nobody can read is worse than
  no diagram.
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import cairosvg

ROOT = Path(__file__).resolve().parent
CASE = ROOT / "docs/health-interop/2026-11-11-dau-urgencia-red"
PNG_DIR = CASE / "05-implementation-guide/input/images"

MARGIN = 40
ROW_H = 72
TOP_TITLE = 30
PART_Y = 84
PART_H = 56
FONT = "sans-serif"

# Operation inventory: the 11 operations of the proposal/guide
# (operations.md). Every message names one of these; every one of these
# appears in at least one diagram. The Bus -> Repository "apply" message
# is the application half of the PI-1 operation that triggered it, so it
# carries that operation's id.
OPERATIONS = [
    "PI-0 Resolver identidad",
    "PI-1 Admisión",
    "PI-1 Alta",
    "PI-1 Abandono",
    "PI-1 Corrección",
    "PI-2 Buscar paciente",
    "PI-2 Buscar episodios",
    "PI-2 Buscar diagnósticos",
    "PI-2 Buscar documento",
    "PI-2 Suscribirse",
    "PI-3 Acceso al PDF",
]

# Arrow: (kind, from_idx, to_idx, label_lines, op)
# kind: "sync" (solid + filled head), "async" (solid + open head),
# "return" (dashed + open head, label below the arrow). op is None for
# returns: a return is the outcome of the message above it.
# Fragment: {"type": "alt"|"opt", "first": arrow idx, "last": arrow idx,
# "guards": [guard per operand], "sep_after": arrow idx (alt only)}.
# Activation: (participant idx, first arrow idx, last arrow idx).

DIAGRAMS = {
    "admission": {
        "title": "Admisión — publicar el evento de admisión (PI-0 / PI-1)",
        "subtitle": (
            "BPMN v7: Persona llega > ¿Emergencia vital? > Admisión > "
            "Crear episodio DAU en el HIS > Publicar evento de admisión "
            "(PI-0) > Bus recibe y aplica"
        ),
        "participants": [
            ("HIS / RCE", ""),
            ("Bus de Interoperabilidad", "MINSAL"),
            ("MPI", ""),
            ("Repositorio FHIR", ""),
        ],
        "arrows": [
            ("sync", 0, 1, ["PI-1 Admisión", "POST /Bundle (admisión)"],
             "PI-1 Admisión"),
            ("sync", 1, 2, ["PI-0 Resolver identidad",
                            "PIXm ITI-83 · consulta MPI"],
             "PI-0 Resolver identidad"),
            ("return", 2, 1, ["identidad resuelta / no resuelta"], None),
            ("sync", 1, 3, ["PI-1 Aplicar transacción",
                            "PUT condicionales · POST + ifNoneExist"],
             "PI-1 Admisión"),
            ("return", 3, 1, ["aplicado"], None),
            ("return", 1, 0, ["200 aplicado / 400–422 / 412 / 422"], None),
        ],
        "fragments": [],
        "activations": [(1, 0, 5), (2, 1, 2), (3, 3, 4)],
        "notes": [
            "C1 (vía rápida): la admisión administrativa corre en paralelo "
            "con la atención clínica (puerta AND del BPMN); el aviso se "
            "publica cuando el episodio existe en el HIS.",
            "400–422: el HIS corrige y reenvía. 412: identificador "
            "condicional ambiguo. 422: la identidad no se resolvió en el "
            "MPI; el HIS corrige y reenvía. Sin respuesta, se puede "
            "reenviar la misma transacción (las operaciones condicionales "
            "evitan duplicados).",
            "Nunca se envía la admisión de un episodio ya cerrado: el PUT "
            "lo reabriría.",
        ],
    },
    "discharge": {
        "title": "Alta — publicar el evento de alta (PI-1)",
        "subtitle": (
            "BPMN v7: Puerta de desenlace > Alta > Indicar medicamentos "
            "> Cerrar DAU y generar PDF > Publicar aviso de alta (PI-1) "
            "> Bus recibe y aplica"
        ),
        "participants": [
            ("HIS / RCE", ""),
            ("Bus de Interoperabilidad", "MINSAL"),
            ("MPI", ""),
            ("Repositorio FHIR", ""),
        ],
        "arrows": [
            ("sync", 0, 1, ["PI-1 Alta", "POST /Bundle (alta)"],
             "PI-1 Alta"),
            ("sync", 0, 1, ["PI-1 Alta", "POST /Bundle (alta, destino 03)"],
             "PI-1 Alta"),
            ("sync", 1, 2, ["PI-0 Resolver identidad",
                            "PIXm ITI-83 · consulta MPI"],
             "PI-0 Resolver identidad"),
            ("return", 2, 1, ["identidad resuelta / no resuelta"], None),
            ("sync", 1, 3, ["PI-1 Aplicar transacción",
                            "PUT condicionales · POST + ifNoneExist"],
             "PI-1 Alta"),
            ("return", 3, 1, ["aplicado"], None),
            ("return", 1, 0, ["200 aplicado / 400–422 / 412 / 422"], None),
            ("sync", 0, 1, ["PI-1 Corrección",
                            "POST /Bundle (entered-in-error)"],
             "PI-1 Corrección"),
            ("return", 1, 0, ["200 aplicado"], None),
        ],
        "fragments": [
            {"type": "alt", "first": 0, "last": 1,
             "guards": ["alta — destino 01, 02, 04, 05 o 06",
                        "fallecimiento — destino 03"],
             "sep_after": 0},
            {"type": "opt", "first": 7, "last": 8,
             "guards": ["si el aviso se envió por error"], "sep_after": None},
        ],
        "activations": [(1, 0, 6), (1, 7, 8), (2, 2, 3), (3, 4, 5)],
        "notes": [
            "El fallecimiento es un alta con destino 03 Fallecido: causa "
            "de muerte en CIE-10 con use = DD, resumen de alta (LOINC "
            "59258-4) si existe; sin medicamentos ni establecimiento de "
            "destino.",
            "Corrección: para anular un aviso enviado por error se reenvía "
            "el Encounter con status = entered-in-error; nunca se envía la "
            "admisión de un episodio ya cerrado.",
        ],
    },
    "abandonment": {
        "title": "Abandono — publicar el evento de abandono (PI-1)",
        "subtitle": (
            "BPMN v7: NEA (después de la admisión, esperando categorización "
            "o atención) o fuga (durante la atención) > Constatar abandono "
            "> Puerta de desenlace (rama abandono) > Cerrar DAU y generar "
            "PDF > Publicar aviso de abandono (PI-1) > Bus recibe y aplica"
        ),
        "participants": [
            ("HIS / RCE", ""),
            ("Bus de Interoperabilidad", "MINSAL"),
            ("MPI", ""),
            ("Repositorio FHIR", ""),
        ],
        "arrows": [
            ("sync", 0, 1, ["PI-1 Abandono", "POST /Bundle (abandono, NEA)"],
             "PI-1 Abandono"),
            ("sync", 0, 1, ["PI-1 Abandono", "POST /Bundle (abandono, fuga)"],
             "PI-1 Abandono"),
            ("sync", 1, 2, ["PI-0 Resolver identidad",
                            "PIXm ITI-83 · consulta MPI"],
             "PI-0 Resolver identidad"),
            ("return", 2, 1, ["identidad resuelta / no resuelta"], None),
            ("sync", 1, 3, ["PI-1 Aplicar transacción",
                            "PUT condicionales · POST + ifNoneExist"],
             "PI-1 Abandono"),
            ("return", 3, 1, ["aplicado"], None),
            ("return", 1, 0, ["200 aplicado / 400–422 / 412 / 422"], None),
        ],
        "fragments": [
            {"type": "alt", "first": 0, "last": 1,
             "guards": ["NEA — tipo 1", "fuga — tipo 2"],
             "sep_after": 0},
        ],
        "activations": [(1, 0, 6), (2, 2, 3), (3, 4, 5)],
        "notes": [
            "NEA: el paciente nunca fue atendido — sin hipótesis ni "
            "medicamentos; el PDF puede no existir. Fuga: hipótesis "
            "provisional (sin use) y nota de urgencia (LOINC 34111-5).",
            "El aviso de abandono repite todos los datos de la admisión: "
            "el PUT reemplaza el Encounter completo; un dato omitido se "
            "borra del repositorio.",
        ],
    },
    "network-pull": {
        "title": "Consulta de la red — pull del Repositorio y suscripción (PI-2)",
        "subtitle": (
            "BPMN v7: Punto de la red > Consultar episodios en el "
            "repositorio (o suscribirse) > ¿Necesita el detalle clínico?"
        ),
        "participants": [
            ("Punto de la red", "APS · Especialidad · Otro hospital · SAMU"),
            ("Repositorio FHIR", ""),
        ],
        "arrows": [
            ("sync", 0, 1, ["PI-2 Buscar paciente — PDQm ITI-78",
                            "GET /Patient?identifier=<sistema RUN>|<RUN>"],
             "PI-2 Buscar paciente"),
            ("return", 1, 0, ["Patient"], None),
            ("sync", 0, 1, ["PI-2 Buscar episodios — QEDm PCC-44",
                            "GET /Encounter?patient.identifier=<RUN>&class=EMER"],
             "PI-2 Buscar episodios"),
            ("return", 1, 0, ["Bundle de Encounter"], None),
            ("sync", 0, 1, ["PI-2 Buscar diagnósticos — QEDm PCC-44",
                            "GET /Condition?encounter=Encounter/[id]"],
             "PI-2 Buscar diagnósticos"),
            ("return", 1, 0, ["Condition(s)"], None),
            ("sync", 0, 1, ["PI-2 Buscar documento — MHD ITI-67",
                            "GET /DocumentReference?encounter=Encounter/[id]"],
             "PI-2 Buscar documento"),
            ("return", 1, 0, ["DocumentReference"], None),
            ("sync", 0, 1, ["PI-2 Suscribirse",
                            "POST Subscription (Encounter class=EMER)"],
             "PI-2 Suscribirse"),
            ("return", 1, 0, ["201 Created"], None),
            ("async", 1, 0, ["PI-2 Notificación",
                             "Subscription: Encounter creado / actualizado"],
             "PI-2 Suscribirse"),
        ],
        "fragments": [
            {"type": "alt", "first": 0, "last": 10,
             "guards": ["consulta puntual", "suscripción"],
             "sep_after": 7},
        ],
        "activations": [(1, 0, 7), (1, 8, 9), (1, 10, 10)],
        "notes": [
            "Buscar episodios también por establecimiento: GET "
            "/Encounter?service-provider.identifier=<sistema DEIS>|<código>"
            "&class=EMER&status=arrived.",
            "DSUB no encaja: la suscripción es una Subscription FHIR sobre "
            "Encounter class=EMER, no una suscripción DSUB a metadatos de "
            "un registro XDS. El canal de notificación (por ejemplo, "
            "REST-hook) es un detalle de implementación.",
        ],
    },
    "document-retrieval": {
        "title": "Recuperación del DAU en PDF (PI-3)",
        "subtitle": (
            "BPMN v7: Punto de la red > ¿Necesita el detalle clínico? "
            "(sí) > Solicitar y recibir DAU en PDF (PI-3) > Seguimiento"
        ),
        "participants": [
            ("Punto de la red", "APS · Especialidad · Otro hospital · SAMU"),
            ("Repositorio FHIR", ""),
            ("HIS / RCE", ""),
        ],
        "arrows": [
            ("sync", 0, 1, ["PI-2 Buscar documento — MHD ITI-67",
                            "GET /DocumentReference?encounter=Encounter/[id]"],
             "PI-2 Buscar documento"),
            ("return", 1, 0, ["DocumentReference (attachment.url)"], None),
            ("sync", 0, 2, ["PI-3 Acceso al PDF — MHD ITI-68",
                            "GET <attachment.url> (autenticado)"],
             "PI-3 Acceso al PDF"),
            ("return", 2, 0, ["PDF del DAU"], None),
        ],
        "fragments": [],
        "activations": [(1, 0, 1), (2, 2, 3)],
        "notes": [
            "El PDF se descarga con un GET autenticado directo a "
            "DocumentReference.content.attachment.url; no es una "
            "transacción ITI-68. Si el HIS no está disponible, el PDF no "
            "se puede descargar: el Repositorio guarda la referencia, no "
            "el documento.",
        ],
    },
}


def wrap(text, max_len):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_len:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def text_w(s, px):
    return len(s) * px * 0.58


def pill(s, x, y, size=12.5, fill="#ffffff", stroke="#9ca3af"):
    w = text_w(s, size) + 12
    return (
        f'<rect x="{x - w / 2:.0f}" y="{y - 13:.0f}" width="{w:.0f}" '
        f'height="18" rx="9" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="0.7"/>'
        f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{size}" fill="#111827">'
        f'{escape(s)}</text>'
    )


def check():
    """Mechanical check of the operation-reference rule."""
    used = {}
    msgs_without_op = []
    for name, d in DIAGRAMS.items():
        for i, (kind, _f, _t, _lines, op) in enumerate(d["arrows"]):
            if kind == "return":
                continue
            if op is None:
                msgs_without_op.append(f"{name} arrow {i}")
            elif op not in OPERATIONS:
                msgs_without_op.append(f"{name} arrow {i} (unknown op {op!r})")
            else:
                used.setdefault(op, []).append(name)
    missing = [op for op in OPERATIONS if op not in used]
    n_msgs = sum(
        1 for d in DIAGRAMS.values()
        for a in d["arrows"] if a[0] != "return"
    )
    n_returns = sum(
        1 for d in DIAGRAMS.values()
        for a in d["arrows"] if a[0] == "return"
    )
    print(f"diagrams: {len(DIAGRAMS)}")
    print(f"operations in inventory: {len(OPERATIONS)}")
    print(f"send messages: {n_msgs} (returns: {n_returns})")
    print(f"messages without a known operation: {len(msgs_without_op)}")
    for m in msgs_without_op:
        print(f"  MISSING OP: {m}")
    print(f"operations without a diagram: {len(missing)}")
    for op in missing:
        print(f"  NO DIAGRAM: {op}")
    for op in OPERATIONS:
        print(f"  {op}: {', '.join(used.get(op, []))}")
    ok = not msgs_without_op and not missing
    print("CHECK " + ("OK" if ok else "FAILED"))
    return ok


def render(name, d):
    parts = d["participants"]
    n = len(parts)
    col_w = 480 if n == 2 else 300
    w = 2 * MARGIN + n * col_w
    col_x = [MARGIN + col_w / 2 + i * col_w for i in range(n)]

    # --- vertical layout: one row per arrow, extra room at fragment edges
    frag_first = {f["first"] for f in d["fragments"]}
    frag_last = {f["last"] for f in d["fragments"]}
    y = PART_Y + PART_H + 46
    ys = []
    for i in range(len(d["arrows"])):
        if i in frag_first:
            y += 30
        ys.append(y)
        y += ROW_H
        if i in frag_last:
            y += 20
    last_y = ys[-1]
    notes_top = last_y + 52

    # --- notes (wrapped) and total height
    note_lines = []
    max_note = int((w - 2 * MARGIN - 32) / 7.0)
    for note in d["notes"]:
        note_lines.append(wrap(note, max_note))
    notes_h = sum(len(lines) * 18 + 20 for lines in note_lines) + 8 * (
        len(note_lines) - 1
    )
    h = notes_top + notes_h + 52

    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">'
    )
    out.append(
        '<defs>'
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#374151"/></marker>'
        '<marker id="arrow-open" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10" fill="none" stroke="#374151" '
        'stroke-width="1.6"/></marker>'
        '<marker id="arrow-ret" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10" fill="none" stroke="#6b7280" '
        'stroke-width="1.5"/></marker>'
        '</defs>'
    )
    out.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>')

    # title + subtitle
    out.append(
        f'<text x="{MARGIN}" y="{TOP_TITLE}" font-family="{FONT}" '
        f'font-size="18" font-weight="bold" fill="#111827">'
        f'{escape(d["title"])}</text>'
    )
    sub = wrap(d["subtitle"], int((w - 2 * MARGIN) / 7.0))
    for i, line in enumerate(sub):
        out.append(
            f'<text x="{MARGIN}" y="{TOP_TITLE + 22 + i * 17}" '
            f'font-family="{FONT}" font-size="13" fill="#6b7280">'
            f'{escape(line)}</text>'
        )

    # --- fragments (behind the arrows)
    for f in d["fragments"]:
        first, last = f["first"], f["last"]
        involved = set()
        for i in range(first, last + 1):
            involved.add(d["arrows"][i][1])
            involved.add(d["arrows"][i][2])
        lo = min(involved)
        hi = max(involved)
        fx0 = col_x[lo] - (col_w / 2 - 14)
        fx1 = col_x[hi] + (col_w / 2 - 14)
        fy0 = ys[first] - 70
        fy1 = ys[last] + 36
        out.append(
            f'<rect x="{fx0:.0f}" y="{fy0:.0f}" width="{fx1 - fx0:.0f}" '
            f'height="{fy1 - fy0:.0f}" fill="#f9fafb" stroke="#6b7280" '
            f'stroke-width="1.5"/>'
        )
        tab = f'{f["type"]} [{f["guards"][0]}]'
        tw = text_w(tab, 12) + 16
        out.append(
            f'<rect x="{fx0:.0f}" y="{fy0:.0f}" width="{tw:.0f}" height="22" '
            f'fill="#ffffff" stroke="#6b7280" stroke-width="1.5"/>'
            f'<text x="{fx0 + 8:.0f}" y="{fy0 + 15:.0f}" '
            f'font-family="{FONT}" font-size="12" font-weight="bold" '
            f'fill="#111827">{escape(tab)}</text>'
        )
        if f["sep_after"] is not None:
            sep_y = (ys[f["sep_after"]] + ys[f["sep_after"] + 1]) / 2
            out.append(
                f'<line x1="{fx0:.0f}" y1="{sep_y:.0f}" x2="{fx1:.0f}" '
                f'y2="{sep_y:.0f}" stroke="#6b7280" stroke-width="1.2" '
                f'stroke-dasharray="6 4"/>'
            )
            g2 = f'[{f["guards"][1]}]'
            gw = text_w(g2, 12) + 12
            out.append(pill(g2, fx0 + 10 + gw / 2, sep_y - 6))

    # --- lifelines
    life_bottom = last_y + 36
    for x in col_x:
        out.append(
            f'<line x1="{x:.0f}" y1="{PART_Y + PART_H}" x2="{x:.0f}" '
            f'y2="{life_bottom}" stroke="#9ca3af" stroke-width="1.2" '
            f'stroke-dasharray="5 4"/>'
        )

    # --- activation bars
    def active_at(p, i):
        return any(a[0] == p and a[1] <= i <= a[2] for a in d["activations"])

    for (p, first, last) in d["activations"]:
        x = col_x[p]
        out.append(
            f'<rect x="{x - 6:.0f}" y="{ys[first] - 8:.0f}" width="12" '
            f'height="{ys[last] - ys[first] + 16:.0f}" fill="#ffffff" '
            f'stroke="#374151" stroke-width="1.2"/>'
        )

    # --- arrows + labels
    for i, (kind, f, t, lines, _op) in enumerate(d["arrows"]):
        y0 = ys[i]
        x1, x2 = col_x[f], col_x[t]
        ltr = x2 > x1
        # arrows attach to the activation bar edge when the endpoint is
        # active on this row, else to the lifeline centre
        if active_at(f, i):
            x1 += -6 if ltr else 6
        if active_at(t, i):
            x2 += -6 if ltr else 6
        if kind == "sync":
            out.append(
                f'<line x1="{x1:.0f}" y1="{y0}" x2="{x2:.0f}" y2="{y0}" '
                f'stroke="#374151" stroke-width="1.8" '
                f'marker-end="url(#arrow)"/>'
            )
        elif kind == "async":
            out.append(
                f'<line x1="{x1:.0f}" y1="{y0}" x2="{x2:.0f}" y2="{y0}" '
                f'stroke="#374151" stroke-width="1.8" '
                f'marker-end="url(#arrow-open)"/>'
            )
        else:  # return: dashed, open head, label below
            out.append(
                f'<line x1="{x1:.0f}" y1="{y0}" x2="{x2:.0f}" y2="{y0}" '
                f'stroke="#6b7280" stroke-width="1.5" '
                f'stroke-dasharray="7 4" marker-end="url(#arrow-ret)"/>'
            )
        mid = (x1 + x2) / 2
        if kind == "return":
            out.append(pill(lines[0], mid, y0 + 20, size=12, fill="#f3f4f6",
                            stroke="#d1d5db"))
        else:
            for j, line in enumerate(lines):
                out.append(pill(line, mid, y0 - 10 - (len(lines) - 1 - j) * 19))

    # --- participant boxes (on top of the lifelines)
    for (name, sub), x in zip(parts, col_x):
        bw = col_w - 30
        out.append(
            f'<rect x="{x - bw / 2:.0f}" y="{PART_Y}" width="{bw:.0f}" '
            f'height="{PART_H}" rx="8" fill="#ffffff" stroke="#374151" '
            f'stroke-width="1.8"/>'
        )
        name_lines = wrap(name, int((bw - 16) / 7.8))[:2]
        total = len(name_lines) * 17 + (17 if sub else 0)
        ty = PART_Y + (PART_H - total) / 2 + 13
        for line in name_lines:
            out.append(
                f'<text x="{x:.0f}" y="{ty:.0f}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="13" font-weight="bold" '
                f'fill="#111827">{escape(line)}</text>'
            )
            ty += 17
        if sub:
            out.append(
                f'<text x="{x:.0f}" y="{ty:.0f}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="11" fill="#6b7280">'
                f'{escape(sub)}</text>'
            )

    # --- notes
    ny = notes_top
    for lines in note_lines:
        bh = len(lines) * 18 + 20
        out.append(
            f'<rect x="{MARGIN}" y="{ny}" width="{w - 2 * MARGIN}" '
            f'height="{bh}" rx="8" fill="#fef9c3" stroke="#d97706" '
            f'stroke-width="1"/>'
        )
        for j, line in enumerate(lines):
            out.append(
                f'<text x="{MARGIN + 14}" y="{ny + 22 + j * 18}" '
                f'font-family="{FONT}" font-size="12.5" fill="#451a03">'
                f'{escape(line)}</text>'
            )
        ny += bh + 8

    out.append(
        f'<text x="{w // 2}" y="{h - 18}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="12" fill="#6b7280">'
        'Cada mensaje nombra la operación que lo lleva; el detalle '
        '(entradas, ejemplo, resultado esperado) está en la tabla de '
        'operaciones de 04-sequence-diagrams.md.</text>'
    )
    out.append("</svg>")
    return "\n".join(out), w, h


def main():
    if "--check" in sys.argv:
        sys.exit(0 if check() else 1)
    for name, d in DIAGRAMS.items():
        svg, w, h = render(name, d)
        svg_path = CASE / f"04-sequence-{name}.svg"
        svg_path.write_text(svg, encoding="utf-8")
        png_path = PNG_DIR / f"04-sequence-{name}.png"
        cairosvg.svg2png(
            bytestring=svg.encode("utf-8"),
            write_to=str(png_path),
            output_width=2 * w,
            output_height=2 * h,
        )
        print(
            f"wrote {svg_path} ({svg_path.stat().st_size} bytes, "
            f"{w}x{h}) and {png_path} ({png_path.stat().st_size} bytes, "
            f"{2 * w}x{2 * h})"
        )


if __name__ == "__main__":
    main()
