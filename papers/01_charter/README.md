# PRNC Frontiers Supplement

This directory contains the reproducible renderer for the Supplementary Material
for the Frontiers in Robotics paper "The Prosocial Robot Navigation Charter: A
Framework Based on Normative Cards" by Anthony Francis.

The supplement includes selected normative cards from the Prosoc repository. The
renderer uses:

- `sources.txt` to list the Markdown card sources included in the supplement;
- `template.tex` for the hand-authored Frontiers LaTeX structure and prose;
- `render.py` as the paper-specific entry point.

Run the renderer from the repository root:

```bash
papers/01_charter/render.py
```

The command writes:

```text
build/papers/01_charter/rendered.tex
```

It also writes individual LaTeX fragments under:

```text
build/papers/01_charter/fragments/
```

The generated `rendered.tex` is the monolithic LaTeX supplement used to create
the paper's Supplementary Material. Checked-in golden outputs under `golden/`
capture reviewed renderings for comparison and reproducibility.

Implementation note: `render.py` is intentionally a thin shim over
`prosoc.utils.papers.render`, preserving this paper's command path while keeping
the reusable rendering logic unit tested.

