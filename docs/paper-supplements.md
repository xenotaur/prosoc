# Paper Supplement Rendering

Prosoc can render paper-specific LaTeX supplements from the normative card
corpus. The workflow is intentionally lightweight: each paper owns its source
manifest, LaTeX template, and command shim, while shared rendering behavior
lives in `prosoc.utils.papers.render`.

The first use of this pattern is the Frontiers supplementary material in
`papers/01_charter/`.

## Directory Layout

A paper supplement renderer should live under `papers/<paper-id>/`:

```text
papers/<paper-id>/
├── sources.txt
├── template.tex
├── render.py
└── golden/
    └── rendered.tex
```

Generated output is written under `build/papers/<paper-id>/`:

```text
build/papers/<paper-id>/
├── fragments/
│   ├── charter.tex
│   └── ...
└── rendered.tex
```

The `build/` output is disposable. Checked-in files under `golden/` capture a
reviewed rendering for diffing and reproducibility.

## Source Manifest

`sources.txt` lists the normative Markdown documents included in the
supplement. Each non-comment line contains a placeholder key and a repository
relative Markdown path:

```text
CHARTER                 prosoc/charter/charter.md
FRONTAL_APPROACH        prosoc/scenarios/frontal_approach/scenario.md
NAVIGATE_POINT_TO_POINT prosoc/tasks/navigate_point_to_point/task.md
```

The key must start with an uppercase letter and may then contain uppercase
letters, digits, and underscores. It maps to a `@@KEY@@` placeholder in
`template.tex` and to a fragment file named `key.lower() + ".tex"` under
`build/papers/<paper-id>/fragments/`.

## Template

`template.tex` is a paper-specific LaTeX document. It should preserve the
publisher setup, hand-authored prose, and section structure needed for the
submission, then use placeholders for generated card content:

```tex
\section{Social Navigation Scenario Cards}

@@FRONTAL_APPROACH@@
```

The template remains paper-specific. Do not generalize publisher-specific
formatting into the shared renderer until more than one paper needs the same
behavior.

## Renderer Shim

Each paper keeps a small executable command at `papers/<paper-id>/render.py`.
The shim sets the repository root, paper directory, and build directory, then
calls `prosoc.utils.papers.render.main`.

Run paper renderers from the repository root:

```bash
papers/01_charter/render.py
```

The command writes the monolithic supplement to:

```text
build/papers/01_charter/rendered.tex
```

It also writes one generated LaTeX fragment per source under:

```text
build/papers/01_charter/fragments/
```

## Shared Rendering Behavior

`prosoc.utils.papers.render` provides the reusable mechanics:

- reads and validates `sources.txt`;
- runs Pandoc once for each Markdown source;
- shifts headings down one level for non-charter cards, so they nest under
  hand-authored category sections;
- writes fixed-up fragment files under `build/papers/<paper-id>/fragments/`;
- replaces exactly one matching `@@KEY@@` placeholder per source;
- fails if any placeholders remain unresolved;
- writes the assembled `rendered.tex`.

The renderer applies deterministic publication fixups that make the generated
LaTeX match reviewed supplement formatting, including list-style code blocks
and removal of Pandoc horizontal-rule output.

## Golden Comparison

After rendering, compare the generated supplement with the reviewed golden
artifact:

```bash
diff -u papers/01_charter/golden/rendered.tex build/papers/01_charter/rendered.tex
```

If the diff is intentional, inspect it carefully before updating the golden
file. If the diff is accidental, fix the source Markdown, `template.tex`, or
renderer behavior and render again.

Historical comparison files, such as `papers/01_charter/golden/original.tex`,
should remain unchanged unless the history itself is being corrected.

## Validation

For renderer changes, run the focused unit tests:

```bash
python -m unittest tests.utils.papers.render_test
```

For repository validation, run the usual project checks:

```bash
scripts/lint
scripts/test
lrh validate
```

`scripts/format --check --diff` checks Python formatting across `prosoc/` and
`tests/`; use the repository's pinned tooling when resolving Python formatting
drift.
