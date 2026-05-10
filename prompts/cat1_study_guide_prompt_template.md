# Study Guide Generator Prompt Template 

Use this prompt when asking an AI agent to create comprehensive study materials from course content. The output is standard markdown optimized for Notion import.

---

## THE PROMPT

```
I have an exam coming up for [SUBJECT NAME]. I am attaching my course material as [PDF/PPT/DOCX/images]. I also have past exam papers as images in the `past-papers/` directory.

Create a comprehensive, exam-focused study guide following this structured approach. Analyze the past papers to identify question patterns, frequently tested topics, and exam style, then use those insights to prioritize and tailor the study notes. All output must be standard markdown compatible with Notion import.

---

## PHASE 0: Setup (Mandatory)

1. Create an implementation plan (`implementation_plan.md`) detailing:
   - Source materials to process
   - Past papers identified in `past-papers/` and initial observations
   - Topics identified from initial scan
   - Proposed file structure with filenames
   - Verification methodology

2. Request my approval before proceeding to Phase 1.

---

## PHASE 1: Extract and Understand

1. Use the provided extraction script to exhaustively extract content from all source materials:

   ```bash
   python extract_course_material.py --input resources/ --output extracted_content/
   ```

2. Review the extraction output in `extracted_content/`:
   - `raw_text.txt` - Plain text for reference
   - `structured.md` - Formatted with headers
   - `equations.json` - All detected equations
   - `problems.json` - All worked examples
   - `figures/` - All extracted images
   - `extraction_summary.md` - Coverage report

3. If extraction is incomplete or the script is unavailable, manually read and process each source file page by page to ensure complete coverage.

4. Analyze the extracted content for:
   - Main concepts and their dependency relationships
   - Formula derivation chains (which formulas build on which)
   - Problem types and solution patterns
   - Sign conventions and edge cases
   - Figures and diagrams that must be preserved

---

## PHASE 1.5: Past Paper Analysis

This phase is critical for making the study guide exam-focused rather than just a content summary.

### 1.5.1 Read All Past Papers
- Open and carefully read every image in the `past-papers/` directory
- These are images (PNG/JPEG) of past exam papers - use vision capabilities to read them
- If any image is unclear, note which parts could not be read and describe what is visible

### 1.5.2 Extract Question Data
For each past paper, record:
- **Paper identifier** (year, semester, or filename if no date is visible)
- **Every question and sub-question**, including:
  - Full question text (transcribed from the image)
  - Marks allocated (if visible)
  - Topic/concept being tested
  - Question type: theoretical, numerical/calculation, derivation, short answer, diagram-based, comparison, or application
  - Difficulty level: straightforward, moderate, or challenging

### 1.5.3 Identify Patterns
Analyze across all past papers and create `study_guide/00_past_paper_analysis.md` containing:

1. **Frequency Table** - How often each topic appears across papers:

   | Topic | Times Appeared | Avg Marks | Question Types Seen |
   |-------|---------------|-----------|---------------------|
   | Topic A | 3/4 papers | 15 marks | Numerical, Derivation |

2. **High-Priority Topics** - Topics that appear in every or nearly every paper (these are almost guaranteed to be on the exam)

3. **Question Style Patterns** - Common structures the examiner uses:
   - Does the examiner prefer numerical problems or conceptual explanations?
   - Are derivations frequently asked?
   - Are there "define and explain" questions?
   - Are comparison questions common (e.g., "compare X and Y")?
   - Is there a pattern to mark distribution?

4. **Recurring Question Templates** - Specific question formats that repeat, e.g.:
   - "Derive the expression for..." (appears in 3/4 papers)
   - "Calculate the value of X given..." (appears in every paper)
   - "Draw and label the diagram of..." (appears in 2/4 papers)

5. **Topics Never Tested** - Topics in the course material that have never appeared in past papers (lower priority but not zero)

6. **Predicted Questions** - Based on the patterns, predict likely questions for the upcoming exam with reasoning

### 1.5.4 Feed Insights into Study Guide
The past paper analysis MUST directly influence the study guide:
- **Exam weight** in the roadmap (`00_roadmap.md`) should be based on actual past paper frequency, not guesswork
- **Topic priority order** should prioritize frequently tested topics
- Each topic file should include a section on how that topic has been examined (see Phase 2 updates below)
- Worked problems should prioritize past paper question styles
- The formula sheet should highlight formulas that appear most often in past paper calculations

---

## PHASE 2: Create Modular Study Files

Create the following files in the `study_guide/` directory.

### 2.1 Roadmap File
**File**: `00_roadmap.md`

Contents:
- A text-based concept dependency map showing which topics build on others. Use an indented list or ASCII diagram. Example:

  ```
  Foundations
  +-- Topic A
  |   +-- Topic B (depends on A)
  |   +-- Topic C (depends on A)
  +-- Topic D
      +-- Topic E (depends on B and D)
  ```

- Topic priority table (Exam Weight MUST be derived from past paper frequency analysis in Phase 1.5):

  | Priority | Topic | Complexity | Exam Weight | Past Paper Appearances | File |
  |----------|-------|------------|-------------|------------------------|------|
  | 1 | Topic Name | High | High | 4/4 papers | [01_topic.md](./01_topic.md) |

- Link to the full past paper analysis: `[Past Paper Analysis](./00_past_paper_analysis.md)`
- Suggested study order with rationale (prioritize topics that appear frequently in past papers)
- Quick-reference table linking every topic to its file

### 2.2 Topic Files
**Files**: `01_[topic].md`, `02_[topic].md`, etc.

Each topic file MUST include ALL of these sections:

1. **Learning Objectives** - Bulleted list of what you will understand after this section

2. **Ground-Up Explanation** - Assume zero prior knowledge on first mention. Build intuition before formalism. Use clear paragraph structure.

3. **Analogies** - At least one relatable real-world comparison to aid memorization

4. **Key Formulas** - Present each formula as:
   ```
   $$
   F = ma
   $$
   ```
   Immediately below each formula, define ALL variables:
   > **Where:**
   > - $F$ = force (N)
   > - $m$ = mass (kg)
   > - $a$ = acceleration (m/s^2)

   Mark critical/must-memorize equations with a blockquote callout:
   > **CRITICAL EQUATION**
   >
   > $$
   > E = mc^2
   > $$

5. **Derivations** - Show step-by-step how formulas connect (where applicable)

6. **Worked Examples** - Match every problem type from source material. Show full step-by-step solutions with unit tracking.

7. **Common Mistakes** - Bulleted list of gotchas and edge cases

8. **Self-Check Questions** - Use HTML details/summary for hidden answers:
   ```html
   <details>
   <summary>Q: What happens when X increases?</summary>

   **Answer:** Y decreases because...

   </details>
   ```

9. **Exam Focus (from Past Papers)** - Based on the Phase 1.5 analysis, include:
   - How this topic has been examined in past papers (question types, marks allocated)
   - Specific past paper questions on this topic (transcribed or paraphrased)
   - Worked solutions to those past paper questions
   - Likely variations the examiner could ask based on the pattern
   - Any examiner preferences (e.g., always asks for a specific derivation, always includes a numerical problem with certain parameters)

10. **Concept Links** - Markdown links to related topics and formula sheet sections:
   `See also: [Topic Name](./02_topic.md) | [Formula](./N_formula_sheet.md#section-anchor)`

### 2.3 Worked Problems File
**File**: `[N-1]_worked_problems.md`

- Solve EVERY problem from the source material
- **Additionally, transcribe and solve EVERY question from the past papers** - these go in a dedicated `## Past Paper Questions` section at the top, grouped by paper
- Group remaining problems by topic/problem type using `## Headers`
- Each problem must have:
  - **Concepts Used**: Links to relevant topic files, e.g. `[Topic Name](./02_topic.md)`
  - **Formulas Used**: Links to formula sheet, e.g. `[Formula Name](./N_formula_sheet.md#section)`
  - **Step-by-step solution** with unit tracking at every step
  - **Final answer** highlighted in a blockquote:
    > **Answer:** $V_{out} = 3.5\text{ V}$
  - **Verification** where applicable (substitute back, dimensional analysis, sanity check)

### 2.4 Formula Sheet
**File**: `[N]_formula_sheet.md`

- Organized by topic with markdown headers (these become anchor links)
- Sections:
  - Physical constants with values and units (in a table)
  - Unit conversion reference table
  - Formulas grouped by topic, each with all variables defined
  - **Frequently Examined Formulas** - A dedicated section at the top listing formulas that appear most often in past paper calculations, marked with a callout:
    > **PAST PAPER FAVOURITE** - This formula has appeared in X/Y past papers
  - Quick reference tables for commonly computed values
  - Sign conventions summary
  - Pre-submission checklist (common things to verify before submitting an exam)

---

## PHASE 3: Handle Figures and Diagrams

This phase is critical. Figures make or break study notes.

### 3.1 Extracted Figures
- All figures extracted by the script are in `extracted_content/figures/`
- Copy every figure that is referenced in the notes to `study_guide/figures/`
- Reference them using standard markdown:
  ```
  ![Description of the figure](./figures/filename.png)
  ```
- ALWAYS include a descriptive alt-text (the text inside the square brackets)

### 3.2 When You Cannot Extract a Figure
If a figure cannot be extracted programmatically:
1. Describe it in detail using a blockquote:
   > **Figure: [Title]**
   > Description of the diagram including all labeled components, axes, values, and relationships shown.
2. If it is a graph, include a text-based data table capturing the key data points
3. If it is a circuit or structure diagram, use ASCII art where feasible

### 3.3 Diagrams You Create
For concept flow diagrams, decision trees, or other structural diagrams:
- Use text-based representations (indented lists, ASCII art, or tables)
- Do NOT use Mermaid syntax (Notion does not render Mermaid)
- If the diagram is complex, create it as an image and save to `study_guide/figures/`

### 3.4 Figure Naming Convention

| Content Type | Naming Pattern | Example |
|--------------|----------------|---------|
| Circuit diagram | `[topic]_circuit.png` | `cs_stage_resistive_load_circuit.png` |
| Cross-section | `[device]_cross_section.png` | `nmos_cross_section.png` |
| Graph/plot | `[relationship]_graph.png` | `id_vs_vds_characteristics.png` |
| Comparison | `[items]_comparison.png` | `nmos_pmos_comparison.png` |
| Extracted figure | `[source]_fig[num].png` | `module1_fig_2_3.png` |
| Generated diagram | `[topic]_diagram.png` | `feedback_loop_diagram.png` |

---

## PHASE 4: Quality Verification

After creating all files, verify:

1. **Page Coverage**: Every page/slide of source material is represented somewhere in the notes
2. **Problem Coverage**: Every worked example from the source has a matching solution
3. **Past Paper Coverage**: Every question from every past paper has been transcribed, solved, and its topic linked
4. **Formula Coverage**: Every equation from the source is in the formula sheet
5. **Figure Coverage**: Every important figure is either embedded or described in detail
6. **Link Integrity**: All `[text](./file.md#anchor)` links point to valid targets
7. **Consistency**: Notation (variable names, sign conventions) is uniform across all files
8. **Exam Alignment**: Topic priorities and exam weights reflect actual past paper frequency data

Create a verification report as `verification_checklist.md` with a checkbox for each item:

```markdown
## Verification Checklist

### Page Coverage
- [x] Module1.pdf pages 1-15 covered in 01_topic.md
- [x] Module1.pdf pages 16-30 covered in 02_topic.md
...

### Problem Coverage
- [x] Example 1.1 solved in worked_problems.md
...

### Past Paper Coverage
- [x] image.png fully transcribed and all questions solved
- [x] image copy.png fully transcribed and all questions solved
- [x] WhatsApp Image ... (1) fully transcribed and all questions solved
- [x] WhatsApp Image ... (2) fully transcribed and all questions solved
- [x] Pattern analysis completed in 00_past_paper_analysis.md
- [x] Exam weights in roadmap reflect past paper frequency
...

### Figure Coverage
- [x] Figure 2.3 embedded as ./figures/module1_fig_2_3.png
- [ ] Figure 3.1 described in text (could not extract)
...
```

---

## FORMAT REQUIREMENTS (Notion-Compatible Markdown)

### Math/LaTeX
- Notion uses KaTeX for math rendering
- Block equations: Use `$$` on separate lines:
  ```
  $$
  E = mc^2
  $$
  ```
- Inline equations: Use single `$`, e.g. `$F = ma$`
- Supported KaTeX functions: https://katex.org/docs/supported
- Do NOT use `\boxed{}` (inconsistent rendering in Notion). Instead, use blockquote callouts to highlight critical equations.

### Images
- Use standard markdown: `![alt text](./figures/filename.png)`
- NEVER use Obsidian wiki-links (`![[image.png]]`)
- Always include descriptive alt text

### Tables
- Use standard pipe tables:
  ```
  | Header 1 | Header 2 |
  |----------|----------|
  | Cell 1   | Cell 2   |
  ```

### Callouts / Highlights
- Use blockquotes for callouts:
  ```
  > **Warning:** This is a common mistake...

  > **Key Insight:** The relationship between X and Y...

  > **CRITICAL EQUATION**
  > $$
  > V = IR
  > $$
  ```

### Hidden/Toggle Content
- Use HTML `<details>` blocks for self-check answers:
  ```html
  <details>
  <summary>Click to reveal answer</summary>

  Answer content here...

  </details>
  ```

### General Formatting Rules
- NO emojis in any files
- Use `---` for horizontal dividers between major sections
- Use `**bold**` for key terms on first introduction
- Use `inline code` for variable names, file paths, and commands
- Use numbered lists for sequential steps, bulleted lists for unordered items
- Every heading must be meaningful and descriptive (not just "Section 1")

---

## CONTENT REQUIREMENTS

- **First Mention**: Full explanation with context, motivation, and intuition
- **Subsequent Mentions**: Concise bullet points as reinforcement, with a link back to the first explanation
- **Repetition**: Intentionally repeat key concepts across relevant sections (spaced repetition principle)
- **Practical Focus**: Every explanation should ultimately help answer exam questions
- **Edge Cases**: Always note boundary conditions, special cases, and where formulas break down
- **Units**: Always track and specify units in formulas, examples, and answers

---

## MY KNOWLEDGE LEVEL

[Choose one or customize]
- Assume I know nothing - explain from absolute basics
- Assume basic familiarity - focus on application and nuance
- Assume strong foundation - focus on advanced topics and tricks

---
```

---

## DIRECTORY STRUCTURE

The working directory should look like this before starting:

```
project_root/
+-- resources/                    # Your source materials go here
|   +-- Module1.pdf
|   +-- Module2.pdf
|   +-- ...
+-- past-papers/                  # Past exam paper images
|   +-- image.png
|   +-- image copy.png
|   +-- *.jpeg / *.png            # Any exam paper images
+-- extract_course_material.py    # Extraction script
+-- study_guide_prompt_template.md # This file
```

After the agent completes all phases:

```
project_root/
+-- resources/
|   +-- Module1.pdf
|   +-- Module2.pdf
+-- extracted_content/            # Phase 1 output
|   +-- raw_text.txt
|   +-- structured.md
|   +-- equations.json
|   +-- problems.json
|   +-- figures/                  # Raw extracted images
|   +-- extraction_summary.md
+-- study_guide/                  # Phase 2-3 output (import this into Notion)
|   +-- 00_past_paper_analysis.md # Phase 1.5 output
|   +-- 00_roadmap.md
|   +-- 01_[topic].md
|   +-- 02_[topic].md
|   +-- ...
|   +-- [N-1]_worked_problems.md
|   +-- [N]_formula_sheet.md
|   +-- figures/                  # Images referenced by the notes
|   |   +-- module1_fig_2_3.png
|   |   +-- ...
|   +-- verification_checklist.md
+-- implementation_plan.md        # Phase 0 output
+-- extract_course_material.py
+-- study_guide_prompt_template.md
```

---

## IMPORTING INTO NOTION

After the agent generates all files:

1. **Individual pages**: Drag and drop each `.md` file from `study_guide/` into Notion. Notion will convert markdown to its native format.

2. **Images**: After importing a page, manually upload any referenced images from `study_guide/figures/` by:
   - Clicking on the broken image placeholder in Notion
   - Selecting "Upload" and navigating to `study_guide/figures/`
   - Or: drag the image file directly into the Notion page at the correct location

3. **Alternative - Hosted images**: If you want images to work automatically on import, upload them to an image hosting service first and replace local paths with URLs in the markdown files before importing.

4. **Math**: Notion should render `$$...$$` and `$...$` blocks automatically on import. If not, manually convert them to Notion equation blocks using `/equation`.

5. **Verify after import**:
   - Check that all math renders correctly
   - Check that all images display
   - Convert any `<details>` blocks to Notion toggle blocks if they did not convert automatically
   - Check that tables render properly

---

## EXTRACTION SCRIPT USAGE

Before starting Phase 1, install dependencies and run:

```bash
pip install PyMuPDF python-pptx python-docx pytesseract Pillow
python extract_course_material.py --input resources/ --output extracted_content/
```

The script handles: PDF, PPTX, DOCX, and images (with OCR).

If the script fails or is unavailable, the agent should read source materials directly and extract content manually.

---

## HANDLING FIGURES: FEASIBILITY REFERENCE

### What Works Well

| Source Type | Extraction Method | Quality |
|-------------|-------------------|---------|
| Embedded PDF images | PyMuPDF extracts as PNG | Excellent |
| PPT images | python-pptx exports blobs | Excellent |
| Scanned text | Tesseract OCR | Good (depends on scan quality) |
| Screenshots | Direct copy | Excellent |

### What Is Challenging

| Source Type | Challenge | Workaround |
|-------------|-----------|------------|
| Hand-drawn graphs | OCR cannot interpret | Describe in text + table of key data points |
| Complex equations in images | LaTeX conversion is error-prone | Type equations manually from the image |
| Multi-part figures | Caption association is ambiguous | Add cross-references manually |
| Low-resolution scans | OCR accuracy drops | Request better source material |

### Recommended Approach for Graphs and Plots

1. **Extract the image** from the PDF to `figures/` directory
2. **Embed it** in the notes: `![X-axis vs Y-axis for Component](./figures/filename.png)`
3. **Create a companion description** including:
   - Axes labels and units
   - Key data points or inflection points
   - Trends or relationships shown
   - Any equations that can be derived from the graph
4. This ensures the information is preserved even if the image does not import cleanly

---

## CHECKLIST BEFORE STARTING

- [ ] All source materials are in `resources/` directory
- [ ] Source PDFs are not password-protected
- [ ] Scanned documents have reasonable quality (300+ DPI preferred)
- [ ] `extract_course_material.py` is present in the project root
- [ ] Python 3.8+ is available
- [ ] You have specified your knowledge level in the prompt
- [ ] Past exam papers (images) are placed in `past-papers/` directory
- [ ] Past paper images are readable (not blurry or cut off)
