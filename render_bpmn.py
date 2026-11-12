#!/usr/bin/env python3
"""Render a BPMN 2.0 file (semantic + DI) to a plain SVG.

Usage: python3 render_bpmn.py <input.bpmn> <output.svg>

Draws pools and lanes, tasks (wrapped labels), gateways (diamonds),
start/end/message events (circles; boundary events as double circles),
data objects (dog-eared), sequence flows (solid) and message flows
(dashed), with flow names at the midpoint.
"""
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

BPMN = '{http://www.omg.org/spec/BPMN/20100524/MODEL}'
DI = '{http://www.omg.org/spec/BPMN/20100524/DI}'
DC = '{http://www.omg.org/spec/DD/20100524/DC}'
DDI = '{http://www.omg.org/spec/DD/20100524/DI}'  # waypoints: lowercase, DD/DI


def wrap(text, max_len):
    if not text:
        return []
    lines, cur = [], ''
    for w in text.split():
        if cur and len(cur) + len(w) + 1 > max_len:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur:
        lines.append(cur)
    return lines


def main():
    src, dst = sys.argv[1], sys.argv[2]
    root = ET.parse(src).getroot()

    sem = {}
    for el in root.iter():
        if 'id' in el.attrib:
            sem[el.attrib['id']] = el

    shapes, edges = [], []
    for plane in root.iter(DI + 'BPMNPlane'):
        for s in plane.iter(DI + 'BPMNShape'):
            b = s.find(DC + 'Bounds')
            shapes.append((s.get('bpmnElement'),
                           int(b.get('x')), int(b.get('y')),
                           int(b.get('width')), int(b.get('height'))))
        for e in plane.iter(DI + 'BPMNEdge'):
            wps = [(int(w.get('x')), int(w.get('y')))
                   for w in e.iter(DDI + 'waypoint')]
            edges.append((e.get('bpmnElement'), wps))

    max_x = max(x + w for _, x, _, w, _ in shapes) + 40
    max_y = max(y + h for _, _, y, _, h in shapes) + 40

    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{max_x}" '
               f'height="{max_y}" viewBox="0 0 {max_x} {max_y}" '
               f'font-family="sans-serif" font-size="12" fill="#111">')
    out.append('<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
               'refX="7" refY="4" orient="auto">'
               '<path d="M0,0 L8,4 L0,8 z" fill="#333"/></marker></defs>')
    out.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')

    def tag_of(eid):
        el = sem.get(eid)
        return el.tag.replace(BPMN, '') if el is not None else ''

    def name_of(eid):
        el = sem.get(eid)
        return (el.get('name') or '') if el is not None else ''

    def text_block(x, y, lines, anchor='middle', size=12, weight=''):
        s = ''
        for i, ln in enumerate(lines):
            s += (f'<text x="{x}" y="{y + i * 13}" text-anchor="{anchor}" '
                  f'font-size="{size}"'
                  + (f' font-weight="{weight}"' if weight else '')
                  + f'>{escape(ln)}</text>')
        return s

    # pools and lanes first (background)
    for eid, x, y, w, h in shapes:
        t = tag_of(eid)
        if t in ('participant', 'lane'):
            fill = '#f5f5f5' if t == 'participant' else 'none'
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                       f'fill="{fill}" stroke="#333" stroke-width="1.5"/>')
            nm = name_of(eid)
            if nm:
                cx, cy = x + 16, y + h / 2
                out.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" '
                           f'transform="rotate(-90 {cx} {cy})" font-size="12" '
                           f'font-weight="bold">{escape(nm)}</text>')

    # edges
    for eid, wps in edges:
        el = sem.get(eid)
        is_msg = el is not None and el.tag == BPMN + 'messageFlow'
        pts = ' '.join(f'{x},{y}' for x, y in wps)
        dash = ' stroke-dasharray="6,4"' if is_msg else ''
        out.append(f'<polyline points="{pts}" fill="none" stroke="#333" '
                   f'stroke-width="1.5"{dash} marker-end="url(#arrow)"/>')
        nm = name_of(eid)
        if nm and len(wps) >= 2:
            mx = sum(p[0] for p in wps) / len(wps)
            my = sum(p[1] for p in wps) / len(wps)
            out.append(text_block(mx, my - 4, wrap(nm, 30),
                                  size=11, weight='bold'))

    # nodes
    for eid, x, y, w, h in shapes:
        t = tag_of(eid)
        nm = name_of(eid)
        cx, cy = x + w / 2, y + h / 2
        if t == 'task':
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                       f'rx="6" fill="white" stroke="#333" stroke-width="1.5"/>')
            lines = wrap(nm, 22)
            ty = cy - (len(lines) - 1) * 13 / 2 + 4
            out.append(text_block(cx, ty, lines))
        elif t == 'exclusiveGateway':
            pts = f'{cx},{y} {x + w},{cy} {cx},{y + h} {x},{cy}'
            out.append(f'<polygon points="{pts}" fill="white" stroke="#333" '
                       f'stroke-width="1.5"/>')
            out.append(f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" '
                       f'font-size="16" font-weight="bold">×</text>')
            if nm:
                out.append(text_block(cx, y + h + 14, wrap(nm, 16), size=11))
        elif t in ('startEvent', 'endEvent'):
            r = w / 2
            sw = 3 if t == 'endEvent' else 1.5
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" '
                       f'stroke="#333" stroke-width="{sw}"/>')
            el = sem.get(eid)
            if el is not None and el.find(BPMN + 'messageEventDefinition') is not None:
                out.append(f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" '
                           f'font-size="12">✉</text>')
            if nm:
                out.append(text_block(cx, y + h + 14, wrap(nm, 18), size=11))
        elif t == 'boundaryEvent':
            r = w / 2
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" '
                       f'stroke="#333" stroke-width="1.5"/>')
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 4}" fill="none" '
                       f'stroke="#333" stroke-width="1"/>')
            if nm:
                out.append(text_block(cx, y + h + 14, wrap(nm, 18), size=11))
        elif t == 'dataObjectReference':
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                       f'fill="white" stroke="#333" stroke-width="1.5"/>')
            out.append(f'<path d="M{x + w - 10},{y} L{x + w},{y + 10} '
                       f'L{x + w - 10},{y + 10} Z" fill="#ddd" stroke="#333"/>')
            if nm:
                out.append(text_block(cx, y + h + 14, wrap(nm, 18), size=11))

    out.append('</svg>')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'SVG written: {dst} ({max_x}x{max_y})')


if __name__ == '__main__':
    main()
