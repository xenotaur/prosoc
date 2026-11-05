# Paper Supplement Rendering

Prosoc can render paper-specific LaTeX supplements from the normative card
corpus. The workflow is intentionally lightweight: each paper owns its source
manifest, LaTeX template, and command shim, while shared rendering behavior
lives in `prosoc.nca.utils.papers.render`.

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
CHARTER                 src/prosoc/prnc/charter/charter.md
FRONTAL_APPROACH        src/prosoc/prnc/scenarios/frontal_approach/scenario.md
NAVIGATE_POINT_TO_POINT src/prosoc/prnc/tasks/navigate_point_to_point/task.md
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
calls `prosoc.nca.utils.papers.render.main`.

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

`prosoc.nca.utils.papers.render` provides the reusable mechanics:

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

## Environment Setup

`render.py` (without `--pdf`) needs only Pandoc. `render.py --pdf` additionally
needs a TeX toolchain (`pdflatex`, `pdftotext`, `kpsewhich`) and the Frontiers
class file. **None of these are managed by this repository's conda
environment** -- `environment.yml` is Python-only by design, so install them
as system tools.

### Pandoc

Install via your platform's package manager (e.g. `brew install pandoc` on
macOS). `render.py --pdf` checks the installed version against
`PANDOC_PINNED_VERSION` (`prosoc.nca.utils.papers.render`) and fails clearly
on drift.

### TeX toolchain (pdflatex, kpsewhich)

On macOS, the standard route is a Homebrew Cask:

```bash
brew install --cask basictex   # ~100MB; or `mactex` for the full ~5GB distribution
```

This installs TeX Live under `/Library/TeX/texbin` and adds that directory to
`PATH` via `/etc/paths.d/TeX` -- that change only takes effect in a **new**
terminal/login shell. The cask's own install output gives a faster
alternative to opening one: in the *same* shell, run

```bash
eval "$(/usr/libexec/path_helper)"
```

Either way, then verify:

```bash
which pdflatex kpsewhich
```

If you work inside a conda environment (as this repo's `environment.yml`
expects) and the binaries resolve outside the environment but not inside it,
conda's own activation is shadowing the system `PATH` entry. The direct fix is
symlinking the binaries into the active environment's own `bin/`, which conda
always puts first on `PATH`:

```bash
ln -s /Library/TeX/texbin/pdflatex  "$CONDA_PREFIX/bin/pdflatex"
ln -s /Library/TeX/texbin/kpsewhich "$CONDA_PREFIX/bin/kpsewhich"
```

**This isn't limited to the tools `render.py` calls directly.** `pdflatex`
itself shells out to other `/Library/TeX/texbin` tools via `\write18` (e.g.
`repstopdf`, the restricted-shell-escape wrapper `epstopdf-pkg` uses to
convert `logo1.eps` to PDF -- see the EPS-to-PDF section below). Those
subprocess calls do their own separate `PATH` lookup, so symlinking only
`pdflatex`/`kpsewhich` is not enough; confirmed live: `which repstopdf`
inside the activated env came up empty even after the two symlinks above,
with `pdflatex` failing later with `sh: repstopdf: command not found`, and
only resolved once `repstopdf` (and `epstopdf`) were symlinked the same way.
Rather than symlinking every TeX tool one at a time as each one comes up,
the more robust fix is a conda environment [activation
hook](https://docs.conda.io/projects/conda/en/stable/dev-guide/deep-dives/activation.html)
that prepends the whole directory to `PATH` on activation:

```bash
mkdir -p "$CONDA_PREFIX/etc/conda/activate.d"
echo 'export PATH="/Library/TeX/texbin:$PATH"' > "$CONDA_PREFIX/etc/conda/activate.d/texbin.sh"
conda deactivate && conda activate ProsocialRobotics   # re-run to pick it up
which pdflatex kpsewhich repstopdf
```

Avoid `conda install -c conda-forge texlive-core` for this -- it is reported
unreliable at actually providing a working `pdflatex`.

BasicTeX's minimal scheme is missing several packages this document needs.
Confirmed end-to-end by actually compiling against a fresh BasicTeX install
(2026.0301) -- this template's own header names `datetime`, `fmtcount`, and
`etoolbox` directly (`template.tex:6`; `fmtcount` also provides
`fcprefix.sty`, the header's fourth name), `template.tex` itself also loads
`framed` (for the Pandoc "Shaded" code-block styling), and the Frontiers
class pulls in `sttools` (provides `flushend.sty`), `changepage` (provides
`chngpage.sty`), and the Adobe Helvetica font metrics (`helvetic`, used for
the title text) besides. Install all seven in one shot:

```bash
sudo /Library/TeX/texbin/tlmgr install datetime fmtcount etoolbox sttools changepage framed helvetic
```

The `helvetic` one shows up differently from the others -- not a missing
`.sty` but `! Font T1/phv/m/n/12=phvr8t at 12.0pt not loadable: Metric (TFM)
file not found`, preceded by `kpathsea: Running mktextfm phvr8t` /
`mktextfm: No such file or directory`. That's `kpathsea` failing to
auto-generate the font metric after not finding a precompiled one --
PostScript font metrics like this one ship precompiled and can't actually
be synthesized that way, so the real fix is just installing the package
that ships them (`tlmgr search --global --file phvr8t.tfm` names it).

(`sudo` is needed since the Homebrew Cask installs under the system-owned
`/Library/TeX`; plain `sudo tlmgr ...` often fails with `sudo: tlmgr: command
not found` instead, because `sudo` resets `PATH` to its own `secure_path`,
which doesn't include `/Library/TeX/texbin` even though your normal shell's
`PATH` does -- calling it by full path sidesteps that.)

If `pdflatex` still fails on a different `! LaTeX Error: File '<name>.sty'
not found.`, the package name doesn't always match the filename (as with
`sttools`/`flushend` above) -- look it up rather than guessing:

```bash
tlmgr search --global --file <name>.sty
sudo /Library/TeX/texbin/tlmgr install <package-name>
```

### pdftotext

Ships separately, as part of Poppler, not TeX Live:

```bash
brew install poppler
```

### EPS-to-PDF conversion (epstopdf, Ghostscript)

pdflatex can't embed EPS images directly -- `epstopdf-pkg` converts
`logo1.eps` to PDF on the fly via a `\write18` shell-out, which needs two
things neither BasicTeX nor this repo provides: the `epstopdf` script
itself, and Ghostscript (`gs`), which `epstopdf` depends on to actually do
the conversion. If this is missing, `pdflatex` fails with
`! Package pdftex.def Error: File './logo1-eps-converted-to.pdf' not
found: using draft setting`, usually preceded by a `command not found`
line from the shell. This is unrelated to `TEXINPUTS`/`TEXMFHOME` --
`\write18` just runs a program via the shell, not through the TeX search
path.

```bash
sudo /Library/TeX/texbin/tlmgr install epstopdf
brew install ghostscript
which epstopdf gs   # confirm both resolve before retrying --pdf
```

### Frontiers class file

`frontiers_suppmat.cls` is a publisher asset and is not committed to this
repository pending a licensing answer (see `WI-CHARTER-SUPPLEMENT-PDF-BUILD`'s
Risk Notes). Obtain your own copy (e.g. from the paper's Overleaf project) and
either point `TEXINPUTS` at the directory containing it before running
`--pdf`:

```bash
export TEXINPUTS=/path/to/your/class-file/dir:
```

(the trailing colon keeps the rest of the default TeX search path), or install
it into your personal `TEXMFHOME` so it's found automatically regardless of
working directory -- `kpsewhich -var-value TEXMFHOME` reports that location.

You'll also need `logo1.eps` (the class's front-page header image), from the
same source. Unlike the class file, `TEXINPUTS`/`TEXMFHOME` **won't** help
here: the class references it as a literal relative path (`./logo1.eps`),
which LaTeX resolves against the compiling process's actual working
directory, not the TeX search path -- and `compile_pdf()` runs `pdflatex`
with `cwd` set to `build/papers/01_charter/` (`render.py:424`), not the repo
root. Copy it there directly:

```bash
mkdir -p build/papers/01_charter
cp /path/to/your/logo1.eps build/papers/01_charter/
```

`render.py` never clears `build/` between runs (only
`build_dir.mkdir(parents=True, exist_ok=True)`), so this is a one-time step,
not something to repeat on every `--pdf` invocation.

## PDF Build

`render.py --pdf` compiles a reviewable PDF from current sources, validating
every prerequisite up front rather than letting a missing tool or version
mismatch surface as an opaque pdflatex log. See
[Environment Setup](#environment-setup) above if Pandoc, the TeX toolchain, or
the Frontiers class file aren't available yet:

```bash
papers/01_charter/render.py --pdf
```

In order, the command:

1. Checks the installed Pandoc version against the pinned version
   (`PANDOC_PINNED_VERSION` in `prosoc.nca.utils.papers.render`) and fails
   clearly on drift -- the pipeline is only reproducible against a pinned
   version; the 2026-10-26 charter supplement pipeline audit observed
   3.10.1 and 2.9.2 across two sandboxes.
2. Checks that `pdflatex` and `pdftotext` are installed and on `PATH`.
3. Checks (via `kpsewhich`) that the Frontiers `frontiers_suppmat` class
   file is on the TeX search path. **This publisher asset is not committed
   to the repository pending a licensing answer** -- supply it locally and
   add its directory to `TEXINPUTS` before running `--pdf`.
4. Runs the semantic/LaTeX regression suite
   (`tests.nca.utils.papers.render_test`,
   `tests.nca.utils.papers.paper_semantics_test`).
5. Renders `rendered.tex` as above.
6. Compiles it with `pdflatex -interaction=nonstopmode -halt-on-error`,
   which stops on a hard LaTeX error (e.g. invalid UTF-8) instead of
   silently producing a corrupted PDF.
7. Extracts the compiled PDF's text with `pdftotext -layout` and checks it
   for known glyph-loss corruption (`KNOWN_PDF_TEXT_CORRUPTIONS`) --
   `template.tex` loads `lmodern` (outline/scalable fonts) specifically so
   this extraction is reliable; the class's default bitmap Computer Modern
   fonts were confirmed to drop dashes and quotes from extracted text in
   the same audit.

On success it reports the Pandoc version, TeX engine version, PDF path, and
page count. Any missing tool, version mismatch, failing regression check, or
compile/text-extraction failure stops the command with a clear, specific
error rather than a partial or silently corrupted result.

**Expected warnings -- don't mistake these for a failure.** A successful
compile's `pdflatex` output is still full of noise:

- `Underfull \hbox`, `Overfull \hbox`, `Underfull \vbox`, `Overfull \vbox`
  -- routine line/page-break warnings. They don't affect the exit code and
  don't block `--pdf` from succeeding.
- `LaTeX Warning: Label(s) may have changed. Rerun to get cross-references
  right.` / `Package rerunfilecheck Warning: File 'rendered.out' has
  changed.` -- LaTeX's normal "compile it twice for correct cross-references
  and PDF bookmarks" convention. `render.py --pdf` only compiles once, so
  this always appears; it doesn't indicate a wrong result, only that page
  numbers in cross-references/bookmarks may be one pass stale.
- The reported page count can differ by one between pdfTeX's own `Output
  written on ... (N pages, ...)` line and `render.py`'s own `Pages: N`
  summary line (`count_pdf_pages`, which counts `\x0c` form feeds in the
  `pdftotext`-extracted text and adds one) -- a counting quirk, not a sign
  of a different or corrupted PDF.

A failed compile looks categorically different: `! LaTeX Error: ...`, `!
Emergency stop.`, `sh: <command>: command not found`, or `!  ==> Fatal error
occurred, no output PDF file produced!` -- and `--pdf` exits non-zero.

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
python -m unittest tests.nca.utils.papers.render_test
```

For repository validation, run the usual project checks:

```bash
scripts/lint
scripts/test
lrh validate
```

`scripts/format --check --diff` checks Python formatting across `src/` and
`tests/`; use the repository's pinned tooling when resolving Python formatting
drift.
