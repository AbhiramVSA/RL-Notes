# Study Guide Generator Prompt Template (Obsidian Edition)

Use this prompt when asking an AI agent to create comprehensive study materials from course content. The output is Obsidian-native markdown with full use of callouts, wiki-links, Mermaid diagrams, YAML frontmatter, and foldable sections.

---

## THE PROMPT

```
I have CAT-2 (second internal exam) coming up for Reinforcement Learning. I am attaching my course material as PPTX files in `resources/`. I also have past exam papers in the `past-papers/` directory (images and/or PDFs).

The material covers: Dynamic Programming (Policy Evaluation, Policy Iteration, Value Iteration), Monte Carlo Methods (First-Visit MC, Every-Visit MC, MC Prediction, MC Control), Importance Sampling (Ordinary and Weighted), and related RL concepts.

Create a comprehensive, exam-focused study guide following this structured approach. Analyze the past papers to identify question patterns, frequently tested topics, and exam style, then use those insights to prioritize and tailor the study notes. All output must be Obsidian-native markdown.

---

## PHASE 0: Setup (Mandatory)

1. Create an implementation plan (`implementation_plan.md`) with YAML frontmatter:
   ```yaml
   ---
   type: plan
   status: draft
   date: {{date}}
   subject: Reinforcement Learning CAT-2
   ---
   ```
   Contents:
   - Source materials to process (list every file in `resources/` and `past-papers/`)
   - Past papers identified and initial observations
   - Topics identified from initial scan
   - Proposed file structure with filenames
   - Verification methodology
   - Estimated number of slides/pages per source file

2. Request my approval before proceeding to Phase 1.

---

## PHASE 1: Extract and Understand

### 1.1 Automated Extraction
Run the provided extraction script to exhaustively extract content from all source materials:

```bash
python extract_course_material.py --input resources/ --output extracted_content/
```

### 1.2 Review Extraction Output
Check `extracted_content/` for:
- `raw_text.txt` - Plain text for reference
- `structured.md` - Formatted with headers
- `equations.json` - All detected equations
- `problems.json` - All worked examples
- `figures/` - All extracted images
- `tables.json` - All extracted tables
- `slide_notes.md` - All speaker notes (often contain exam hints)
- `extraction_summary.md` - Coverage report

### 1.3 Manual Verification (CRITICAL)
The extraction script is a starting point. You MUST also:
- **Read every source file directly** slide by slide / page by page using your native capabilities
- **Cross-reference** against the extraction output to catch anything the script missed
- **Pay special attention to**:
  - Equations embedded as images (script cannot parse these - you must transcribe them to LaTeX)
  - Diagrams with embedded text labels
  - Speaker notes (professors often put exam hints here)
  - Bullet points with mathematical notation using Unicode symbols
  - Tables embedded as images
  - Content in text boxes, callout shapes, or annotations

### 1.4 Content Analysis
After extraction and verification, analyze for:
- Main concepts and their dependency relationships
- Formula derivation chains (which formulas build on which)
- Problem types and solution patterns
- Algorithm pseudocode and step-by-step procedures
- Convergence proofs and their key steps
- Backup diagrams and Bellman equation trees
- Policy evaluation vs control distinctions
- On-policy vs off-policy method comparisons

---

## PHASE 1.5: Past Paper Analysis

This phase is critical for making the study guide exam-focused rather than just a content summary.

### 1.5.1 Read All Past Papers
- Open and carefully read every file in the `past-papers/` directory
- These may be images (PNG/JPEG) or PDFs - use vision capabilities for images, read PDFs directly
- For PDFs with multiple pages, process EVERY page
- If any content is unclear, note which parts could not be read and describe what is visible
- OCR any handwritten portions if present

### 1.5.2 Extract Question Data
For each past paper, record:
- **Paper identifier** (year, semester, CAT number, or filename if no date is visible)
- **Every question and sub-question**, including:
  - Full question text (transcribed verbatim from the source)
  - Marks allocated (if visible)
  - Topic/concept being tested
  - Question type: theoretical, numerical/calculation, derivation, algorithm-trace, short answer, diagram-based, comparison, proof, or pseudocode
  - Difficulty level: straightforward, moderate, or challenging
  - Whether it requires memorized definitions vs. applied problem-solving

### 1.5.3 Identify Patterns
Analyze across all past papers and create `study_guide/00_past_paper_analysis.md` containing:

1. **Frequency Table** - How often each topic appears across papers:

   | Topic | Times Appeared | Avg Marks | Question Types Seen |
   |-------|---------------|-----------|---------------------|
   | Policy Iteration | 3/4 papers | 10 marks | Algorithm trace, Numerical |
   | Monte Carlo Prediction | 2/4 papers | 15 marks | Derivation, Calculation |

2. **High-Priority Topics** - Topics that appear in every or nearly every paper (almost guaranteed to be on the exam)

3. **Question Style Patterns** - Common structures the examiner uses:
   - Does the examiner prefer algorithm traces or conceptual explanations?
   - Are Bellman equation derivations frequently asked?
   - Are there "define and explain" questions?
   - Are comparison questions common (e.g., "compare policy iteration vs value iteration")?
   - Does the examiner ask for pseudocode?
   - Are numerical grid-world/MDP problems common?
   - Is there a pattern to mark distribution?

4. **Recurring Question Templates** - Specific question formats that repeat, e.g.:
   - "Apply policy iteration to the following MDP..." (appears in X/Y papers)
   - "Derive the update rule for..." (appears in every paper)
   - "Compare and contrast X and Y methods" (appears in X/Y papers)

5. **Topics Never Tested** - Topics in the course material that have never appeared in past papers (lower priority but not zero)

6. **Predicted Questions** - Based on the patterns, predict likely questions for CAT-2 with reasoning

### 1.5.4 Feed Insights into Study Guide
The past paper analysis MUST directly influence the study guide:
- **Exam weight** in the roadmap should be based on actual past paper frequency, not guesswork
- **Topic priority order** should prioritize frequently tested topics
- Each topic file should include a section on how that topic has been examined
- Worked problems should prioritize past paper question styles
- The formula sheet should highlight formulas that appear most often in past paper calculations

---

## PHASE 2: Create Modular Study Files

Create the following files in the `study_guide/` directory. Every file MUST have YAML frontmatter.

### 2.1 Roadmap File
**File**: `00_roadmap.md`

Frontmatter:
```yaml
---
type: roadmap
subject: Reinforcement Learning CAT-2
topics: [dynamic-programming, monte-carlo, importance-sampling]
tags: [rl, cat2, roadmap]
---
```

Contents:
- A Mermaid concept dependency diagram:
  ```
  ```mermaid
  graph TD
      A[MDP Fundamentals] --> B[Policy Evaluation]
      B --> C[Policy Iteration]
      B --> D[Value Iteration]
      A --> E[Monte Carlo Prediction]
      E --> F[MC Control]
      F --> G[On-Policy MC]
      F --> H[Off-Policy MC]
      H --> I[Importance Sampling]
  ```
  ```

- Topic priority table (Exam Weight MUST be derived from past paper frequency):

  | Priority | Topic | Complexity | Exam Weight | Past Paper Appearances | File |
  |----------|-------|------------|-------------|------------------------|------|
  | 1 | Topic Name | High | High | 4/4 papers | `[[01_topic]]` |

- Link to past paper analysis: `[[00_past_paper_analysis]]`
- Suggested study order with rationale (prioritize high-frequency topics)
- Quick-reference table linking every topic to its file using wiki-links

### 2.2 Topic Files
**Files**: `01_[topic].md`, `02_[topic].md`, etc.

Each file MUST have frontmatter:
```yaml
---
type: topic
topic: [topic-name]
module: [module-number]
exam_weight: [high/medium/low]
past_paper_frequency: [X/Y papers]
prerequisites: [[prerequisite_topic]]
tags: [rl, cat2, topic-tag]
---
```

Each topic file MUST include ALL of these sections:

1. **Learning Objectives** - Bulleted list of what you will understand after this section

2. **Ground-Up Explanation** - Assume zero prior knowledge on first mention. Build intuition before formalism. Use clear paragraph structure. For RL topics specifically:
   - Start with the problem the method solves (WHY does this exist?)
   - Give a concrete small example (e.g., 4x4 grid world) before the general case
   - Walk through one complete iteration by hand before presenting the algorithm

3. **Analogies** - At least one relatable real-world comparison to aid memorization

4. **Algorithm / Procedure** - For algorithmic topics (most RL topics), present:
   - The complete pseudocode in a code block
   - A line-by-line explanation of what each step does
   - A hand-traced example showing the algorithm running on a small MDP

5. **Key Formulas** - Present each formula as:
   ```
   $$
   V(s) = \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]
   $$
   ```
   Immediately below each formula, define ALL variables using an Obsidian callout:
   ```
   > [!info] Variable Definitions
   > - $V(s)$ = state-value function for state $s$
   > - $\pi(a|s)$ = probability of taking action $a$ in state $s$ under policy $\pi$
   > - $p(s',r|s,a)$ = transition probability
   > - $\gamma$ = discount factor ($0 \leq \gamma \leq 1$)
   ```

   Mark critical/must-memorize equations with:
   ```
   > [!danger] MUST MEMORIZE
   > $$
   > V(s) = \max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V(s')]
   > $$
   ```

6. **Derivations** - Show step-by-step how formulas connect. For Bellman equations, show:
   - The expectation form
   - The summation form
   - How the recursive structure emerges
   - Connection to the backup diagram

7. **Worked Examples** - Match every problem type from source material. Show full step-by-step solutions. For RL:
   - Include grid-world examples with full state-value tables at each iteration
   - Show policy tables (arrows or action labels) at each step
   - Track convergence explicitly

8. **Common Mistakes** - Using Obsidian callout:
   ```
   > [!warning] Common Mistakes
   > - Forgetting to initialize V(terminal) = 0
   > - Confusing first-visit vs every-visit MC
   > - ...
   ```

9. **Self-Check Questions** - Using Obsidian foldable callouts:
   ```
   > [!question]- What is the difference between policy evaluation and policy iteration?
   > **Answer:** Policy evaluation computes V^π for a fixed policy π...
   ```

10. **Exam Focus (from Past Papers)** - Using a dedicated callout:
    ```
    > [!exam] Exam Focus
    > **How this topic has been examined:**
    > - Question types seen: ...
    > - Marks typically allocated: ...
    > - Specific past paper questions: ...
    > - Likely variations: ...
    ```
    Include:
    - How this topic has been examined in past papers (question types, marks allocated)
    - Specific past paper questions on this topic (transcribed or paraphrased)
    - Worked solutions to those past paper questions
    - Likely variations the examiner could ask based on the pattern
    - Any examiner preferences

11. **Concept Links** - Obsidian wiki-links to related topics:
    ```
    See also: [[02_topic]] | [[N_formula_sheet#Section Name]]
    ```

### 2.3 Worked Problems File
**File**: `[N-1]_worked_problems.md`

Frontmatter:
```yaml
---
type: problems
tags: [rl, cat2, worked-problems]
---
```

- Solve EVERY problem from the source material
- **Transcribe and solve EVERY question from the past papers** in a dedicated `## Past Paper Questions` section at the top, grouped by paper
- Group remaining problems by topic using `## Headers`
- Each problem must have:
  - **Concepts Used**: Wiki-links to relevant topic files: `[[02_topic]]`
  - **Formulas Used**: Wiki-links to formula sheet: `[[N_formula_sheet#Section]]`
  - **Step-by-step solution** with clear intermediate results
  - **Final answer** highlighted:
    ```
    > [!success] Answer
    > $V^*(s_1) = 3.5$
    ```
  - **Verification** where applicable (substitute back, check convergence, sanity check)

### 2.4 Formula Sheet
**File**: `[N]_formula_sheet.md`

Frontmatter:
```yaml
---
type: formula-sheet
tags: [rl, cat2, formulas]
---
```

- Organized by topic with markdown headers (these become Obsidian heading links)
- Sections:
  - **Frequently Examined Formulas** at the top:
    ```
    > [!danger] PAST PAPER FAVOURITE - Appeared in X/Y papers
    > $$
    > V_{k+1}(s) = \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)[r + \gamma V_k(s')]
    > $$
    ```
  - RL notation reference table (states, actions, rewards, policies, value functions)
  - Bellman equations (all four: V^π, Q^π, V*, Q*)
  - Dynamic Programming update rules
  - Monte Carlo estimation formulas
  - Importance sampling ratios and formulas
  - Convergence conditions and criteria
  - Key algorithm comparison table
  - Common MDP parameter conventions

### 2.5 Quick Review / Cheat Sheet (NEW)
**File**: `[N+1]_quick_review.md`

A single-page rapid review designed for last-minute revision:
- One-line summary of each algorithm
- All four Bellman equations side by side in a table
- DP vs MC comparison table
- On-policy vs off-policy comparison table
- Key theorems stated without proof
- "If you see X in the exam, use Y" decision guide

---

## PHASE 3: Handle Figures and Diagrams

### 3.1 Extracted Figures
- All figures extracted by the script are in `extracted_content/figures/`
- Copy every figure referenced in the notes to `study_guide/figures/`
- Reference using Obsidian wiki-links for images:
  ```
  ![[filename.png]]
  ```
- Also provide alt-text where possible:
  ```
  ![[filename.png|Description of the figure]]
  ```

### 3.2 When You Cannot Extract a Figure
If a figure cannot be extracted programmatically:
1. Describe it in detail using a callout:
   ```
   > [!figure] Title of Figure
   > Detailed description including all labeled components, axes, values, and relationships shown.
   ```
2. If it is a graph, include a text-based data table capturing the key data points
3. If it is a backup diagram or decision tree, use Mermaid:
   ```mermaid
   graph TD
       S((s)) -->|a1| S1((s'))
       S((s)) -->|a2| S2((s''))
   ```

### 3.3 Diagrams You Create
For concept flow diagrams, backup diagrams, decision trees:
- **Prefer Mermaid syntax** (Obsidian renders Mermaid natively):
  ```
  ```mermaid
  graph TD
      A[Start] --> B{Decision}
      B -->|Yes| C[Action 1]
      B -->|No| D[Action 2]
  ```
  ```
- For complex diagrams that Mermaid cannot handle, create as an image and save to `study_guide/figures/`

### 3.4 Figure Naming Convention

| Content Type | Naming Pattern | Example |
|--------------|----------------|---------|
| Backup diagram | `[method]_backup.png` | `policy_eval_backup.png` |
| Grid world | `[description]_grid.png` | `4x4_gridworld.png` |
| Algorithm flow | `[algorithm]_flow.png` | `policy_iteration_flow.png` |
| Convergence plot | `[method]_convergence.png` | `value_iteration_convergence.png` |
| Comparison | `[items]_comparison.png` | `dp_vs_mc_comparison.png` |
| Extracted figure | `[source]_s[num].png` | `module3_s12_img1.png` |

---

## PHASE 4: Quality Verification

After creating all files, verify:

1. **Slide Coverage**: Every slide of every PPTX is represented somewhere in the notes. Create a mapping:
   - For each source file, list slide numbers and where each slide's content appears in the study guide
2. **Problem Coverage**: Every worked example from the source has a matching solution
3. **Past Paper Coverage**: Every question from every past paper has been transcribed, solved, and its topic linked
4. **Formula Coverage**: Every equation from the source is in the formula sheet
5. **Figure Coverage**: Every important figure is either embedded or described
6. **Link Integrity**: All `[[wiki-links]]` point to valid files/headings
7. **Consistency**: Notation (variable names, Greek letters, subscripts) is uniform across all files
8. **Exam Alignment**: Topic priorities and exam weights reflect actual past paper frequency data
9. **Algorithm Coverage**: Every algorithm from the slides has complete pseudocode and a hand-traced example
10. **LaTeX Rendering**: All `$...$` and `$$...$$` blocks use valid LaTeX that renders in Obsidian

Create a verification report as `verification_checklist.md`:

```markdown
---
type: verification
status: complete
---

## Verification Checklist

### Slide Coverage
- [x] MODULE3 1 Dynamic Programming.pptx - slides 1-N covered in 01_topic.md, 02_topic.md
- [x] MODULE3 2 Monte Carlo, Components.pptx - slides 1-N covered in 03_topic.md
...

### Past Paper Coverage
- [x] cat2 papers.pdf - all pages transcribed, all questions solved
- [x] papers toc.pdf - all questions transcribed and solved
- [x] Pattern analysis completed in [[00_past_paper_analysis]]
- [x] Exam weights in roadmap reflect past paper frequency

### Problem Coverage
- [x] Example 1 from slide X solved in [[worked_problems]]
...

### Algorithm Coverage
- [x] Policy Evaluation pseudocode + hand trace in [[01_topic]]
- [x] Policy Iteration pseudocode + hand trace in [[02_topic]]
...

### Formula Coverage
- [x] All Bellman equations in [[formula_sheet]]
...
```

---

## FORMAT REQUIREMENTS (Obsidian-Native Markdown)

### YAML Frontmatter
Every file MUST start with YAML frontmatter:
```yaml
---
type: [topic/roadmap/problems/formula-sheet/analysis/verification]
tags: [rl, cat2, relevant-tags]
---
```

### Math/LaTeX
- Obsidian uses MathJax for math rendering
- Block equations: Use `$$` on separate lines:
  ```
  $$
  V(s) = E_\pi[G_t | S_t = s]
  $$
  ```
- Inline equations: Use single `$`, e.g. `$V(s)$`
- Common RL notation to use consistently:
  - States: $s, s'$, Actions: $a$, Rewards: $r, R_t$
  - Policy: $\pi(a|s)$, Value: $V(s)$, Action-value: $Q(s,a)$
  - Return: $G_t$, Discount: $\gamma$, Learning rate: $\alpha$
  - Transition: $p(s',r|s,a)$
- Use `\text{}` for words inside equations: $V_{\text{old}}$
- Use `\operatorname{}` for multi-letter operators

### Internal Links (Wiki-Links)
- Link to files: `[[filename]]` (without .md extension)
- Link to headings: `[[filename#Heading Name]]`
- Link with display text: `[[filename|Display Text]]`
- Embed content: `![[filename]]` or `![[filename#Heading]]`

### Images
- Obsidian wiki-link style: `![[image.png]]`
- With size: `![[image.png|500]]`
- With alt text: `![[image.png|alt text]]`
- Standard markdown also works: `![alt text](./figures/filename.png)`

### Callouts (Use These Extensively)
Obsidian has rich callout support. Use these types:

```markdown
> [!info] Title
> Information content

> [!warning] Common Mistake
> Warning content

> [!danger] MUST MEMORIZE
> Critical equation or fact

> [!example] Worked Example
> Step-by-step solution

> [!question]- Self-Check Question (foldable, collapsed by default)
> Hidden answer

> [!tip] Exam Tip
> Exam-specific advice

> [!note] Key Insight
> Important conceptual insight

> [!success] Answer
> Final answer to a problem

> [!abstract] Summary
> Section summary
```

The `-` after the callout type makes it **foldable and collapsed by default** (use for self-check answers).

### Mermaid Diagrams
Obsidian renders Mermaid natively. Use for:
- Concept dependency graphs
- Algorithm flowcharts
- Backup diagrams
- State transition diagrams
- Decision trees

### Tables
Use standard pipe tables:
```
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

### Tags
Use tags for cross-cutting categorization:
- `#rl/dynamic-programming`
- `#rl/monte-carlo`
- `#rl/importance-sampling`
- `#exam/must-memorize`
- `#exam/past-paper-favourite`

### General Formatting Rules
- NO emojis in any files
- Use `---` for horizontal dividers between major sections
- Use `**bold**` for key terms on first introduction
- Use `inline code` for variable names, file paths, and commands
- Use numbered lists for sequential steps, bulleted lists for unordered items
- Every heading must be meaningful and descriptive
- Use horizontal rules (`---`) to separate major sections within a file

---

## CONTENT REQUIREMENTS

- **First Mention**: Full explanation with context, motivation, and intuition
- **Subsequent Mentions**: Concise bullet points as reinforcement, with a wiki-link back to the first explanation
- **Repetition**: Intentionally repeat key concepts across relevant sections (spaced repetition principle)
- **Practical Focus**: Every explanation should ultimately help answer exam questions
- **Edge Cases**: Always note boundary conditions, special cases, and where formulas/algorithms break down
- **Algorithms**: Present pseudocode AND a hand-traced example for every algorithm
- **Comparisons**: Create comparison tables whenever two or more methods can be contrasted (DP vs MC, first-visit vs every-visit, on-policy vs off-policy, ordinary vs weighted importance sampling)
- **Convergence**: For every iterative method, state: what converges, to what, under what conditions, and how fast

---

## REINFORCEMENT LEARNING SPECIFIC REQUIREMENTS

Since this is an RL exam, ensure the following are covered exhaustively:

### Dynamic Programming
- Policy Evaluation (iterative): algorithm, convergence proof sketch, example
- Policy Improvement Theorem: statement, proof sketch, why it guarantees monotonic improvement
- Policy Iteration: full algorithm, example on small MDP, convergence guarantee
- Value Iteration: full algorithm, relationship to policy iteration, example
- Generalized Policy Iteration (GPI): concept and diagram
- Synchronous vs asynchronous DP
- Complexity analysis of DP methods

### Monte Carlo Methods
- First-Visit vs Every-Visit MC prediction: algorithms, difference, bias/variance
- MC estimation of action values
- MC Control: Exploring Starts
- On-policy MC Control (epsilon-soft policies)
- Off-policy MC Control
- Every-visit vs first-visit convergence properties

### Importance Sampling
- Why importance sampling is needed (off-policy learning)
- Importance sampling ratio: definition and derivation
- Ordinary importance sampling: formula, properties (unbiased but high variance)
- Weighted importance sampling: formula, properties (biased but lower variance)
- Incremental implementation
- Per-decision importance sampling (if covered)

### Cross-Cutting Concepts
- Prediction vs Control
- On-policy vs Off-policy
- Model-based (DP) vs Model-free (MC)
- Exploration vs Exploitation in the MC context
- Backup diagrams for each method

---

## MY KNOWLEDGE LEVEL

Assume basic familiarity with RL fundamentals (MDPs, Bellman equations, policies, value functions from Module 1-2). Focus on application, algorithm mechanics, derivations, and exam-ready problem solving for the CAT-2 topics.

---
```

---

## DIRECTORY STRUCTURE

The working directory should look like this before starting:

```
rl-2/
+-- resources/                          # Source PPTX files
|   +-- MODULE3 1 Dynamic Programming.pptx
|   +-- MODULE3 2 Monte Carlo, Components.pptx
|   +-- MODULE3 3 Monte Carlo Control.pptx
|   +-- Importance Sampling Example.pptx
+-- past-papers/                        # Past exam papers
|   +-- *.pdf / *.png / *.jpeg
+-- extract_course_material.py          # Extraction script
+-- study_guide_prompt_template.md      # This file
```

After the agent completes all phases:

```
rl-2/
+-- resources/
+-- past-papers/
+-- extracted_content/                  # Phase 1 output
|   +-- raw_text.txt
|   +-- structured.md
|   +-- equations.json
|   +-- problems.json
|   +-- tables.json
|   +-- slide_notes.md
|   +-- figures/
|   +-- extraction_summary.md
+-- study_guide/                        # Phase 2-3 output (open as Obsidian vault)
|   +-- 00_past_paper_analysis.md
|   +-- 00_roadmap.md
|   +-- 01_dynamic_programming.md
|   +-- 02_policy_iteration.md
|   +-- 03_value_iteration.md
|   +-- 04_monte_carlo_prediction.md
|   +-- 05_monte_carlo_control.md
|   +-- 06_importance_sampling.md
|   +-- 07_worked_problems.md
|   +-- 08_formula_sheet.md
|   +-- 09_quick_review.md
|   +-- figures/
|   +-- verification_checklist.md
+-- implementation_plan.md
+-- extract_course_material.py
+-- study_guide_prompt_template.md
```

To use: open the `study_guide/` folder as an Obsidian vault. All wiki-links, callouts, Mermaid diagrams, and LaTeX will render natively.

---

## EXTRACTION SCRIPT USAGE

Before starting Phase 1, install dependencies and run:

```bash
pip install PyMuPDF python-pptx python-docx pytesseract Pillow
python extract_course_material.py --input resources/ --output extracted_content/
```

The script handles: PDF, PPTX, DOCX, and images (with OCR).

If the script fails or is unavailable, the agent MUST read source materials directly and extract content manually, slide by slide.

**IMPORTANT**: The script is a supplement, not a replacement. Always verify extraction output against the original files. Slides with equations as images, complex diagrams, or unusual layouts will need manual processing.

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
| Equations as images | LaTeX conversion is error-prone | Transcribe equations manually to LaTeX |
| Backup diagrams | Structure is lost | Recreate using Mermaid in Obsidian |
| Multi-part figures | Caption association is ambiguous | Add cross-references manually |
| Low-resolution scans | OCR accuracy drops | Request better source material |

### Recommended Approach for Graphs and Plots

1. **Extract the image** from the source to `figures/` directory
2. **Embed it** in the notes: `![[filename.png|Description]]`
3. **Create a companion description** using a callout:
   ```
   > [!figure] Description of Figure
   > - Axes: X = ..., Y = ...
   > - Key data points: ...
   > - Trend: ...
   > - Related equation: $...$
   ```
4. This ensures the information is preserved even if the image has quality issues

---

## CHECKLIST BEFORE STARTING

- [ ] All source materials are in `resources/` directory
- [ ] Source files are not password-protected
- [ ] `extract_course_material.py` is present in the project root
- [ ] Python 3.8+ is available
- [ ] Past exam papers are placed in `past-papers/` directory
- [ ] Past paper files are readable (not blurry or cut off)
- [ ] Obsidian is installed (for viewing the output)
