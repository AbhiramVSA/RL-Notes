<p align="center">
  <img src="assets/rl-notes-logo.png" alt="Open notebook, pencil, reward loop, and decision tree icon" width="160">
</p>

<h1 align="center">Reinforcement Learning FAT Workspace</h1>

<p align="center">This repository contains RL CAT 1 (<code>rl</code>) and CAT 2 (<code>rl-2</code>) work in one Final FAT workspace.</p>

<p align="center">
  <a href="#obsidian-entry-point">Study guide</a> ·
  <a href="#extraction-scripts">Scripts</a> ·
  <a href="#example">Example</a> ·
  <a href="#layout">Layout</a>
</p>

<p align="center">
  <a href="#dependencies-and-validation">Dependencies</a> ·
  <a href="#tests">Tests</a> ·
  <a href="#license">License</a>
</p>

## Obsidian entry point

Open `rl-fat/study_guide` in Obsidian. Start with [`00_fat_rl_index.md`](study_guide/00_fat_rl_index.md).

## PDF-only setup

Run these commands from the repository root:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install PyMuPDF==1.28.2
```

PyMuPDF 1.28.2 is the version used for this PDF validation. It is a validation pin, not a project dependency pin or a supported-version range. This setup covers the PDF examples below. Other file types need additional packages or system tools.

## Extraction scripts

Each script accepts one input file or a directory. A directory scan is recursive. Each script writes to `extracted_content` by default. Each script reads PDF, PowerPoint (`.pptx`), Word (`.docx`), and image (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`) files.

Run these commands from the repository root, with the virtual environment above activated:

```sh
python3 scripts/cat1_extract_course_material.py --input ./input-files --output ./extracted_content/cat1
python3 scripts/cat2_extract_course_material.py --input ./input-files --output ./extracted_content/cat2
python3 scripts/cat1_extract_course_material.py --input ./input-files/synthetic-sample.pdf --output ./extracted_content/cat1-single
```

Replace each input path with the path to your input file or directory. The output path is optional. The default is `extracted_content`.

## Example

The runtime check used temporary paths and synthetic one-page PDFs. It included a CAT 1 directory, a CAT 2 directory, and one CAT 1 PDF file. The inputs were synthetic. They did not include course or user files. The CAT 1 directory run wrote this excerpt to `raw_text.txt`:

```text
============================================================
[synthetic-sample.pdf] Page/Slide 1
============================================================

Synthetic RL sample: 2 plus 2 equals 4.
```

## Layout

- [`study_guide/`](study_guide/) — Obsidian notes from CAT 1 and CAT 2.
- [`study_guide/figures/`](study_guide/figures/) — figures for CAT 1 and CAT 2 notes.
- [`source_material/cat1/`](source_material/cat1/) — CAT 1 source PDFs and past papers.
- [`source_material/cat2/`](source_material/cat2/) — CAT 2 source PowerPoint files and past papers when present.
- `extracted_content/cat1/` — an example output path for CAT 1.
- `extracted_content/cat2/` — an example output path for CAT 2.
- [`prompts/`](prompts/) — CAT prompts and the editable FAT prompt starter.
- [`scripts/`](scripts/) — CAT 1 and CAT 2 extraction scripts.
- [`plans/`](plans/) — reference plans.

The `rl` and `rl-2` directories stay available as a fallback.

## Dependencies and validation

The repository has no dependency manifest, lock file, or Python version pin. It gives no Python version range or install command with fixed package versions.

The scripts import PyMuPDF (`fitz`), `python-pptx`, `python-docx`, Pillow, `pytesseract`, and `tabula-py`. This review ran only the PDF path. It used Python 3.13.16 and PyMuPDF 1.28.2 in a temporary environment. These versions describe this review. They are not project requirements or a support range.

## Tests

No test directory or test command is present in the tracked files.

## License

No `LICENSE`, `COPYING`, or `NOTICE` file is present. The repository does not state license terms.
