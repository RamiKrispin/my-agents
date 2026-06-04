#!/usr/bin/env python3
"""Emit a .drawio XML file from a flat JSON node spec.

Usage:
    python3 build_drawio.py <spec.json> <out.drawio>

Spec format (see formats/drawio-diagram.md):
    {
      "title": "RAG pipeline",                       # optional
      "layout": "horizontal" | "vertical" | "grid",  # default horizontal
      "nodes": [
        {"id": "q",   "label": "User query", "shape": "rounded"},
        {"id": "emb", "label": "Embed",      "shape": "rect"},
        ...
      ],
      "edges": [
        {"from": "q",   "to": "emb"},
        {"from": "emb", "to": "vs", "label": "k=10", "style": "dashed"},
        ...
      ]
    }

Open the output in https://app.diagrams.net or the drawio desktop app to
fine-tune visuals (colors, positions, swimlanes) before exporting to PNG/SVG.

Zero external dependencies — stdlib only.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape as _xml_escape


def escape(s: str) -> str:
    """xml.sax.saxutils.escape doesn't escape double-quotes by default, but
    every escaped value here is placed inside a double-quoted XML attribute,
    so a label like `RAG "pipeline"` would break the file. Map '"' → &quot;.
    """
    return _xml_escape(s, {'"': "&quot;"})

# Visual constants — drawio coordinates are points.
NODE_WIDTH = 160
NODE_HEIGHT = 60
H_GAP = 60   # horizontal spacing between nodes
V_GAP = 40   # vertical spacing between nodes
PAD = 40     # outer padding

# Shape → drawio style fragment.
SHAPE_STYLES = {
    "rect":     "rounded=0",
    "rounded":  "rounded=1",
    "ellipse":  "ellipse",
    "diamond":  "rhombus",
    "hexagon":  "shape=hexagon;perimeter=hexagonPerimeter2",
}

EDGE_STYLES = {
    "solid":  "endArrow=classic;html=1;rounded=0",
    "dashed": "endArrow=classic;html=1;rounded=0;dashed=1",
}


def _layout_positions(nodes, layout):
    """Return {id: (x, y)} positions for the chosen layout."""
    n = len(nodes)
    if n == 0:
        return {}

    if layout == "vertical":
        return {
            node["id"]: (PAD, PAD + i * (NODE_HEIGHT + V_GAP))
            for i, node in enumerate(nodes)
        }

    if layout == "grid":
        cols = max(1, int(math.ceil(math.sqrt(n))))
        positions = {}
        for i, node in enumerate(nodes):
            row, col = divmod(i, cols)
            x = PAD + col * (NODE_WIDTH + H_GAP)
            y = PAD + row * (NODE_HEIGHT + V_GAP)
            positions[node["id"]] = (x, y)
        return positions

    # default: horizontal
    return {
        node["id"]: (PAD + i * (NODE_WIDTH + H_GAP), PAD)
        for i, node in enumerate(nodes)
    }


def _node_xml(node, x, y):
    shape = node.get("shape", "rect")
    style_fragment = SHAPE_STYLES.get(shape, SHAPE_STYLES["rect"])
    style = (
        f"{style_fragment};whiteSpace=wrap;html=1;"
        "fillColor=#ffffff;strokeColor=#1f2937;fontColor=#111827;fontSize=14"
    )
    label = escape(node.get("label", node["id"]))
    nid = escape(node["id"])
    return (
        f'<mxCell id="{nid}" value="{label}" style="{style}" '
        f'vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{NODE_WIDTH}" '
        f'height="{NODE_HEIGHT}" as="geometry"/>'
        f'</mxCell>'
    )


def _edge_xml(edge, edge_id):
    style = EDGE_STYLES.get(edge.get("style", "solid"), EDGE_STYLES["solid"])
    label = escape(edge.get("label", ""))
    src = escape(edge["from"])
    tgt = escape(edge["to"])
    return (
        f'<mxCell id="e{edge_id}" value="{label}" style="{style}" '
        f'edge="1" parent="1" source="{src}" target="{tgt}">'
        f'<mxGeometry relative="1" as="geometry"/>'
        f'</mxCell>'
    )


def build_drawio(spec):
    """Return drawio XML for a parsed spec dict."""
    nodes = spec.get("nodes") or []
    edges = spec.get("edges") or []
    layout = spec.get("layout", "horizontal")
    title = spec.get("title", "Diagram")

    node_ids = {n["id"] for n in nodes}
    for e in edges:
        if e["from"] not in node_ids:
            raise ValueError(f"edge.from '{e['from']}' not in nodes")
        if e["to"] not in node_ids:
            raise ValueError(f"edge.to '{e['to']}' not in nodes")

    positions = _layout_positions(nodes, layout)
    node_xml = "".join(_node_xml(n, *positions[n["id"]]) for n in nodes)
    edge_xml = "".join(_edge_xml(e, i) for i, e in enumerate(edges))

    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<mxfile host="my-agents" type="device">'
        f'<diagram name="{escape(title)}" id="diagram-1">'
        '<mxGraphModel dx="800" dy="600" grid="1" gridSize="10" '
        'guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
        'page="1" pageScale="1" pageWidth="850" pageHeight="1100" '
        'math="0" shadow="0">'
        '<root>'
        '<mxCell id="0"/>'
        '<mxCell id="1" parent="0"/>'
        f'{node_xml}{edge_xml}'
        '</root>'
        '</mxGraphModel>'
        '</diagram>'
        '</mxfile>'
    )


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    spec_path = Path(argv[1])
    out_path = Path(argv[2])
    if not spec_path.exists():
        print(f"error: spec file not found: {spec_path}", file=sys.stderr)
        return 2

    try:
        spec = json.loads(spec_path.read_text())
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {spec_path}: {exc}", file=sys.stderr)
        return 2

    if not isinstance(spec, dict) or "nodes" not in spec:
        print("error: spec must be an object with a 'nodes' field",
              file=sys.stderr)
        return 2

    try:
        xml = build_drawio(spec)
    except (KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    out_path.write_text(xml)
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
