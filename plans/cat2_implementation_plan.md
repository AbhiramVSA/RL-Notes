---
type: plan
status: draft
date: 2026-03-21
subject: Reinforcement Learning CAT-2
---

# Implementation Plan - RL CAT-2 Study Guide

## Source Materials

### Resources (PPTX files)

| File | Slides | Status | Key Content |
|------|--------|--------|-------------|
| `Importance Sampling Example.pptx` | 10 | OK | 2 worked examples on importance sampling (statistical + RL episode) |
| `MODULE3 1 Dynamic Programming.pptx` | 8 | OK | DP introduction, motorbike rental problem motivation |
| `MODULE3 2 Monte Carlo, Components.pptx` | 18 | OK | MC prediction, first-visit vs every-visit MC, worked examples, policy evaluation |
| `MODULE3 3 Monte Carlo Control.pptx` | ? | CORRUPT | File is a truncated zip archive (no end-of-central-directory record). Cannot be read by python-pptx or zipfile. |

### Past Papers
- **Directory is empty** - no past papers provided
- Past paper analysis phase will be skipped
- Exam weights will be based on module outline emphasis and topic coverage in slides

### Extracted Images (13 total)
- `is_s4_img1.png` - Importance weight derivation (w(x) formula steps)
- `is_s5_img2.png` - f(x) = e^(-x^2) formula
- `is_s5_img3.png` - w(x) = e^(-x+1/2) formula
- `is_s5_img4.png` - Sum f(xi)w(xi) = 3.170
- `is_s6_img5.png` - IS estimator calculation (0.634 result)
- `m3_1_s1_img1.gif` - DP title slide graphic
- `m3_2_s1_img1.gif` - MC title slide graphic
- `m3_2_s8_img2.jpg` - v_pi(s) = E_pi[G_t | S_t = s] equation
- `m3_2_s9_img3.png` - V_pi(s) = (1/N) sum G_{i,s} equation
- `m3_2_s13_img4.png` - Episode traces (states A, B with rewards)
- `m3_2_s14_img5.png` - Same episode traces (duplicate)
- `m3_2_s15_img6.png` - Same episode traces (duplicate)
- `m3_2_s16_img7.png` - Four episodes E1-E4 with 5 states (S0-S4) and rewards

## Topics Identified

From the slides and module outline (slide 2 of MODULE3 1 and MODULE3 2):

1. **Dynamic Programming** - intro, motivation, planning vs RL (from slides)
2. **Policy Evaluation** - iterative policy evaluation algorithm (mentioned in outline, not detailed in available slides)
3. **Policy Iteration** - full algorithm (mentioned in outline, not detailed in available slides)
4. **Value Iteration** - algorithm and convergence (mentioned in outline, not detailed in available slides)
5. **Monte Carlo Prediction** - first-visit and every-visit MC (well covered in slides)
6. **Monte Carlo Control** - exploring starts, on-policy, off-policy (CORRUPT FILE - content unavailable)
7. **Importance Sampling** - ordinary and weighted IS, worked examples (well covered in slides)

### Content Gap Analysis
The corrupt MODULE3 3 file likely contained:
- MC Control with Exploring Starts
- On-policy MC Control (epsilon-soft/epsilon-greedy)
- Off-policy MC Control
- GPI (Generalized Policy Iteration)
- Possibly epsilon-greedy policy improvement

The MODULE3 1 slides only cover DP motivation, not the algorithms. The detailed DP algorithms (policy evaluation, policy iteration, value iteration) were likely in additional slides or covered in class.

**Approach**: I will cover all topics from the module outline comprehensively using standard RL textbook content (Sutton & Barto), ensuring the study guide is complete for the exam despite the corrupt file.

## Proposed File Structure

```
study_guide/
  00_roadmap.md
  01_dynamic_programming.md          (DP overview, policy evaluation)
  02_policy_iteration.md             (policy improvement + iteration)
  03_value_iteration.md              (value iteration, comparison with PI)
  04_monte_carlo_prediction.md       (first-visit, every-visit MC)
  05_monte_carlo_control.md          (MC control methods)
  06_importance_sampling.md          (ordinary, weighted IS)
  07_worked_problems.md              (all worked problems)
  08_formula_sheet.md                (all formulas)
  09_quick_review.md                 (cheat sheet)
  figures/                           (all extracted + generated figures)
  verification_checklist.md
```

## Verification Methodology
1. Cross-reference every slide's content against study guide files
2. Ensure all equations from images are transcribed to LaTeX
3. Verify all worked examples are solved step-by-step
4. Check all wiki-links resolve
5. Confirm notation consistency across files

## Notes
- No past paper analysis possible (empty directory)
- MODULE3 3 content will be reconstructed from standard RL curriculum
- DP algorithm details will be supplemented beyond what's in the available slides
- All topic files will follow the full template structure from the prompt
