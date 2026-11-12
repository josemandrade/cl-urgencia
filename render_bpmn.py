#!/usr/bin/env python3
"""Render a BPMN 2.0 file (semantic + DI) to a plain SVG.

Usage: python3 render_bpmn.py <input.bpmn> <output.svg>

Draws pools and lanes, tasks (wrapped labels), gateways (diamonds),
start/end/message events (circles; boundary events as double circles),
data objects (dog-eared), sequence flows (solid) and message flows
(dashed), with flow names on the longest segment.

Readability rules (learned the hard way — a diagram nobody can read is
worse than no diagram):
- Pool and lane names are drawn HORIZONTALLY in a label column on the
  left, never as long rotated text inside a short lane. A rotated label
  longer than its lane spills into the neighbouring lanes and the
  labels pile up into an unreadable wall. The label column is wide
  enough for the full name (wrapped to at most 2-3 lines).
- Flow labels are short (the parenthetical detail is dropped for
  message flows — the full definition lives in the model's PI table)
  and sit on the longest segment, not on the centroid of all
  waypoints (a centroid lands in the middle of the diagram, where
  several labels pile up).
- NO label may overlap another label. All names drawn outside their
  shape (gateway/event/data-object names, flow labels) are collected,
  de-collided as one set — a label that would land on another is
  nudged until it clears — and flow labels get a white background so
  they stay readable where they cross a line. A flow label that lands
  on an event name is just as unreadable as two flow labels on each
  other, so they are de-collided together, not separately.
- Render the PNG at 2x the SVG size so the text stays crisp when the
  reader zooms in.
- After rendering, LOOK at the PNG before shipping the diagram. If
  any label is clipped, overlapped or illegible, fix the renderer or
  the layout — do not ship it.
"""
import re
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

BPMN = '{http://www.omg.org/spec/BPMN/20100524/MODEL}'
DI = '{http://www.omg.org/spec/BPMN/20100524/DI}'
DC = '{http://www.omg.org/spec/DD/20100524/DC}'
DDI = '{http://www.omg.org/spec/DD/20100524/DI}'  # waypoints: lowercase, DD/DI

LABEL_W = 240          # left label column for pool/lane names (horizontal)
MARGIN = 40            # margin around the diagram
POOL_FONT = 10         # pool name (muted, at the top of its label column)
LANE_FONT = 12         # lane name (bold, centred on its lane)
FLOW_FONT = 11         # flow label
NODE_FONT = 11         # name drawn outside a gateway/event/data object


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


def short_flow_name(name, is_msg):
    """Short display name for a flow: message flows drop the parenthetical
    detail (the full definition lives in the model's PI table)."""
    if is_msg:
        name = re.sub(r'\s*\([^)]*\)\s*$', '', name).strip()
    return name


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

    # Shift the whole diagram right by the label column.
    shapes = [(eid, x + LABEL_W, y, w, h) for eid, x, y, w, h in shapes]
    edges = [(eid, [(x + LABEL_W, y) for x, y in wps])
             for eid, wps in edges]

    max_x = max(x + w for _, x, _, w, _ in shapes) + MARGIN
    max_y = max(y + h for _, _, y, _, h in shapes) + MARGIN

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

    def text_block(x, y, lines, anchor='middle', size=12, weight='',
                   color='#111'):
        s = ''
        for i, ln in enumerate(lines):
            s += (f'<text x="{x}" y="{y + i * 13}" text-anchor="{anchor}" '
                  f'font-size="{size}"'
                  + (f' font-weight="{weight}"' if weight else '')
                  + (f' fill="{color}"' if color != '#111' else '')
                  + f'>{escape(ln)}</text>')
        return s

    # pools and lanes first (background). Names go in the left label
    # column, horizontal: the pool name (small, muted) at the top of
    # the pool, each lane name (bold) centred on its lane. No rotated
    # text — a rotated name longer than its lane is unreadable.
    for eid, x, y, w, h in shapes:
        t = tag_of(eid)
        if t not in ('participant', 'lane'):
            continue
        fill = '#f5f5f5' if t == 'participant' else 'none'
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                   f'fill="{fill}" stroke="#333" stroke-width="1.5"/>')
        nm = name_of(eid)
        if not nm:
            continue
        if t == 'participant':
            lines = wrap(nm, 34)[:3]
            out.append(text_block(8, y + 14, lines, anchor='start',
                                  size=POOL_FONT, color='#555'))
        else:
            lines = wrap(nm, 30)[:2]
            ty = y + h / 2 - (len(lines) - 1) * 13 / 2 + 4
            out.append(text_block(8, ty, lines, anchor='start',
                                  size=LANE_FONT, weight='bold'))
    out.append(f'<line x1="{LABEL_W}" y1="0" x2="{LABEL_W}" y2="{max_y}" '
               f'stroke="#ccc" stroke-width="1"/>')

    # edges (lines only). Flow labels are collected and drawn later,
    # de-collided together with the node names.
    flow_labels = []  # (lines, cx, cy, width_px)
    for eid, wps in edges:
        el = sem.get(eid)
        is_msg = el is not None and el.tag == BPMN + 'messageFlow'
        pts = ' '.join(f'{x},{y}' for x, y in wps)
        dash = ' stroke-dasharray="6,4"' if is_msg else ''
        out.append(f'<polyline points="{pts}" fill="none" stroke="#333" '
                   f'stroke-width="1.5"{dash} marker-end="url(#arrow)"/>')
        nm = short_flow_name(name_of(eid), is_msg)
        if nm and len(wps) >= 2:
            best, best_len = None, -1.0
            for i in range(len(wps) - 1):
                ax, ay = wps[i]
                bx, by = wps[i + 1]
                ln = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
                if ln > best_len:
                    best_len, best = ln, ((ax + bx) / 2, (ay + by) / 2)
            mx, my = best
            lines = wrap(nm, 30 if is_msg else 22)[:2]
            width = max(len(ln) for ln in lines) * 7
            flow_labels.append((lines, mx, my - 6, width))

    # nodes (shapes only). Task names sit inside their boxes. Gateway,
    # event and data-object names sit outside their shape, so they are
    # collected with the flow labels and de-collided as one set.
    ext_labels = []  # (lines, cx, cy, width_px, is_flow)
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
                lines = wrap(nm, 16)
                ext_labels.append((lines, cx, y + h + 14,
                                   max(len(ln) for ln in lines) * 6, False,
                                   NODE_FONT))
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
                lines = wrap(nm, 18)
                ext_labels.append((lines, cx, y + h + 14,
                                   max(len(ln) for ln in lines) * 6, False,
                                   NODE_FONT))
        elif t == 'boundaryEvent':
            r = w / 2
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" '
                       f'stroke="#333" stroke-width="1.5"/>')
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 4}" fill="none" '
                       f'stroke="#333" stroke-width="1"/>')
            if nm:
                # one line, small: a boundary event hangs off the bottom
                # of its task and the next task is only ~15 px below, so
                # a two-line label would land on that task's box.
                lines = wrap(nm, 28)[:1]
                ext_labels.append((lines, cx, y + h + 12,
                                   max(len(ln) for ln in lines) * 5.5, False,
                                   10))
        elif t == 'dataObjectReference':
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                       f'fill="white" stroke="#333" stroke-width="1.5"/>')
            out.append(f'<path d="M{x + w - 10},{y} L{x + w},{y + 10} '
                       f'L{x + w - 10},{y + 10} Z" fill="#ddd" stroke="#333"/>')
            if nm:
                lines = wrap(nm, 18)
                ext_labels.append((lines, cx, y + h + 14,
                                   max(len(ln) for ln in lines) * 6, False,
                                   NODE_FONT))

    for lines, cx, cy, width in flow_labels:
        ext_labels.append((lines, cx, cy, width, True, FLOW_FONT))

    # ---- draw all outside labels, de-collided as one set ----
    def boxes_overlap(a, b):
        ax0, ay0, ax1, ay1 = a
        bx0, by0, bx1, by1 = b
        return ax0 < bx1 and ax1 > bx0 and ay0 < by1 and ay1 > by0

    placed = []
    for lines, cx, cy, width, is_flow, fontsize in ext_labels:
        height = len(lines) * 13
        ox, oy = 0, 0
        for dx, dy in [(0, 0), (0, 14), (0, 28), (0, -14), (0, -28),
                       (30, 0), (-30, 0), (0, 42), (0, -42), (60, 0),
                       (-60, 0)]:
            x0 = cx + dx - width / 2
            y0 = cy + dy - height + 4
            box = (x0, y0, x0 + width, y0 + height)
            if not any(boxes_overlap(box, p) for p in placed):
                ox, oy = dx, dy
                break
        else:
            x0 = cx - width / 2
            y0 = cy - height + 4
            box = (x0, y0, x0 + width, y0 + height)
        placed.append(box)
        fx, fy = cx + ox, cy + oy
        if is_flow:
            bx0, by0, bx1, by1 = box
            out.append(f'<rect x="{bx0 - 3}" y="{by0 - 2}" '
                       f'width="{bx1 - bx0 + 6}" height="{by1 - by0 + 4}" '
                       f'fill="white" fill-opacity="0.9"/>')
        # first baseline: block top + 10 (text_block adds 13 per line)
        out.append(text_block(fx, fy - height + 14, lines,
                              size=fontsize,
                              weight='bold' if is_flow else ''))

    out.append('</svg>')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'SVG written: {dst} ({max_x}x{max_y})')


if __name__ == '__main__':
    main()
