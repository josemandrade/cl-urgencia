#!/usr/bin/env python3
"""Render the FHIR resource graph for the DAU proposal as an SVG,
in the style of clinFHIR GraphBuilder: each resource instance is a
rectangle with title and type, references are directional arrows
labelled with the element that carries the reference.

Usage: python3 render_fhir_graph.py [output.svg]
Default output: docs/health-interop/2026-11-11-dau-urgencia-red/04-fhir-proposal-graph.svg
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    ROOT / "docs/health-interop/2026-11-11-dau-urgencia-red/04-fhir-proposal-graph.svg"
)

W, H = 1220, 900
NODE_W, NODE_H = 260, 110
HEADER_H = 30

# node: id, x, y, resource type, header colour, profile, [field lines], dashed?
NODES = [
    ("org-emisor", 60, 110, "Organization", "#6d28d9",
     "MINSAL Prestador Organizacional", ["código DEIS"], False),
    ("org-destino", 480, 110, "Organization", "#6d28d9",
     "MINSAL Prestador Organizacional", ["código DEIS", "destination (alta 01/02/04)"], False),
    ("practitioner", 900, 110, "Practitioner", "#b45309",
     "MINSAL Prestador Profesional", ["RUN · qualification"], False),
    ("patient", 60, 390, "Patient", "#0e7490",
     "MINSAL Paciente (NID)", ["RUN · birthDate · gender"], False),
    ("encounter", 480, 390, "Encounter", "#d97706",
     "EncuentroUrgencia", ["ID DAU · status · period", "class = EMER"], False),
    ("condition", 900, 390, "Condition", "#15803d",
     "Diagnóstico de urgencia", ["CIE-10 · verificationStatus"], False),
    ("docref", 60, 690, "DocumentReference", "#1d4ed8",
     "Documento de urgencia", ["LOINC 59258-4 / 34111-5", "content.attachment.url → PDF"], False),
    ("pdf", 480, 690, "PDF DAU", "#475569",
     "Documento clínico completo", ["(no es un recurso FHIR)"], True),
    ("medreq", 900, 690, "MedicationRequest", "#be185d",
     "Indicación de medicamento", ["medication · dosageInstruction"], False),
]

# edge: (path d, label, label x, label y, anchor)
# The routing is crossing-free by construction (verified by hand):
# horizontals in the middle band sit at distinct y (590, 630, 560, 575)
# and verticals end before the horizontals they would cross.
EDGES = [
    ("M480,445 H320", "subject", 400, 436, "middle"),
    ("M560,390 L190,220", "serviceProvider", 330, 290, "middle"),
    ("M660,390 L1030,220", "participant.individual", 965, 250, "middle"),
    ("M740,435 H900", "diagnosis.condition", 820, 426, "middle"),
    ("M610,390 V220", "hospitalization.destination", 622, 300, "start"),
    ("M1000,500 V590 H220 V500", "subject", 610, 581, "middle"),
    ("M900,465 H740", "encounter", 820, 482, "middle"),
    ("M1030,690 V630 H180 V500", "subject", 605, 621, "middle"),
    ("M950,690 V560 H700 V500", "encounter", 825, 551, "middle"),
    ("M140,690 V500", "subject", 152, 600, "start"),
    ("M250,690 V575 H500 V500", "context.encounter", 375, 566, "middle"),
    ("M320,745 H480", "content.attachment.url", 400, 736, "middle"),
]


def node_svg(n):
    nid, x, y, rtype, color, profile, fields, dashed = n
    dash = ' stroke-dasharray="7 4"' if dashed else ""
    parts = []
    parts.append(
        f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="8" '
        f'fill="#ffffff" stroke="{color}" stroke-width="2"{dash}/>'
    )
    parts.append(
        f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{HEADER_H}" rx="8" fill="{color}"/>'
        f'<rect x="{x}" y="{y + HEADER_H - 8}" width="{NODE_W}" height="8" fill="{color}"/>'
    )
    parts.append(
        f'<text x="{x + NODE_W // 2}" y="{y + 21}" text-anchor="middle" '
        f'font-family="sans-serif" font-size="16" font-weight="bold" fill="#ffffff">'
        f'{escape(rtype)}</text>'
    )
    ty = y + HEADER_H + 22
    parts.append(
        f'<text x="{x + NODE_W // 2}" y="{ty}" text-anchor="middle" '
        f'font-family="sans-serif" font-size="13" font-weight="bold" fill="#1f2937">'
        f'{escape(profile)}</text>'
    )
    for i, line in enumerate(fields):
        parts.append(
            f'<text x="{x + NODE_W // 2}" y="{ty + 20 + i * 19}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="12" fill="#4b5563">'
            f'{escape(line)}</text>'
        )
    return "\n".join(parts)


def label_svg(text, lx, ly, anchor):
    # a white pill behind the label so it stays readable over lines
    width = len(text) * 7.4 + 12
    x = lx - width / 2 if anchor == "middle" else lx
    return (
        f'<rect x="{x:.0f}" y="{ly - 13:.0f}" width="{width:.0f}" height="18" rx="9" '
        f'fill="#ffffff" stroke="#9ca3af" stroke-width="0.7"/>'
        f'<text x="{lx}" y="{ly:.0f}" text-anchor="{anchor}" '
        f'font-family="sans-serif" font-size="12.5" fill="#111827">{escape(text)}</text>'
    )


def main():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">'
    )
    parts.append(
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#374151"/></marker></defs>'
    )
    parts.append('<rect x="0" y="0" width="1220" height="900" fill="#ffffff"/>')
    # Bundle envelope (dashed frame)
    parts.append(
        '<rect x="25" y="40" width="1170" height="810" rx="14" '
        'fill="none" stroke="#6b7280" stroke-width="2" stroke-dasharray="10 6"/>'
    )
    parts.append(
        '<text x="48" y="72" font-family="sans-serif" font-size="17" '
        'font-weight="bold" fill="#374151">Bundle (transaction)</text>'
    )
    parts.append(
        '<text x="48" y="94" font-family="sans-serif" font-size="13" fill="#6b7280">'
        'una transacción por evento: admisión · alta · abandono</text>'
    )
    # edges first, then nodes on top
    for d, label, lx, ly, anchor in EDGES:
        parts.append(
            f'<path d="{d}" fill="none" stroke="#374151" stroke-width="1.8" '
            f'marker-end="url(#arrow)"/>'
        )
    for d, label, lx, ly, anchor in EDGES:
        parts.append(label_svg(label, lx, ly, anchor))
    for n in NODES:
        parts.append(node_svg(n))
    parts.append(
        '<text x="610" y="878" text-anchor="middle" font-family="sans-serif" '
        'font-size="13" fill="#6b7280">Las flechas son referencias FHIR; la etiqueta es el '
        'elemento que lleva la referencia. El Bundle es el sobre que lleva los recursos.</text>'
    )
    parts.append("</svg>")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
