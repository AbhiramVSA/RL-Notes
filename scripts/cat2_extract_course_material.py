"""
Universal Course Material Extractor (Enhanced for Obsidian)
===========================================================
Exhaustively extracts content from PDFs, PPTX, DOCX, and images.

Usage:
    python extract_course_material.py --input <path> --output <output_dir>
    python extract_course_material.py --input "resources/" --output "extracted_content/"

Handles:
    - PDF (textbooks, notes, slides exported as PDF)
    - PPTX (PowerPoint presentations) - including grouped shapes, SmartArt text, tables
    - DOCX (Word documents)
    - Images (PNG, JPG, JPEG, BMP, TIFF) with OCR

Output:
    - raw_text.txt: Plain text content
    - structured.md: Obsidian-formatted markdown with callouts and wiki-links
    - equations.json: All detected equations
    - problems.json: All worked examples
    - tables.json: All extracted tables
    - slide_notes.md: All speaker notes (exam hints)
    - figures/: Extracted images
    - extraction_summary.md: Coverage report
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class ExtractedEquation:
    """Represents a detected equation"""
    content: str
    source_file: str
    page_or_slide: int
    context: str = ""
    is_numbered: bool = False
    equation_number: str = ""
    latex_form: str = ""  # Attempted LaTeX conversion

@dataclass
class ExtractedProblem:
    """Represents a worked example or problem"""
    title: str
    problem_text: str
    solution_text: str
    source_file: str
    page_or_slide: int
    problem_type: str = ""

@dataclass
class ExtractedFigure:
    """Represents an extracted figure/image"""
    filename: str
    source_file: str
    page_or_slide: int
    caption: str = ""
    description: str = ""
    width: int = 0
    height: int = 0

@dataclass
class ExtractedTable:
    """Represents an extracted table"""
    headers: List[str]
    rows: List[List[str]]
    source_file: str
    page_or_slide: int
    caption: str = ""

@dataclass
class SlideNote:
    """Speaker notes from a slide"""
    source_file: str
    slide_num: int
    slide_title: str
    notes_text: str

@dataclass
class PageContent:
    """Content from a single page/slide"""
    page_num: int
    source_file: str
    raw_text: str
    formatted_text: str = ""
    section_header: str = ""
    equations: List[ExtractedEquation] = field(default_factory=list)
    problems: List[ExtractedProblem] = field(default_factory=list)
    figures: List[ExtractedFigure] = field(default_factory=list)
    tables: List[ExtractedTable] = field(default_factory=list)
    notes: str = ""  # Speaker notes

@dataclass
class ExtractionResult:
    """Complete extraction result"""
    source_files: List[str]
    total_pages: int
    pages: List[PageContent]
    all_equations: List[ExtractedEquation]
    all_problems: List[ExtractedProblem]
    all_figures: List[ExtractedFigure]
    all_tables: List[ExtractedTable]
    all_notes: List[SlideNote]
    section_hierarchy: Dict[str, List[str]]
    extraction_time: str
    warnings: List[str] = field(default_factory=list)

# ============================================================================
# PATTERN DEFINITIONS (Enhanced for RL content)
# ============================================================================

EQUATION_PATTERNS = [
    # LaTeX style
    r'\$\$(.+?)\$\$',
    r'\$(.+?)\$',
    r'\\begin\{equation\}(.+?)\\end\{equation\}',
    r'\\begin\{align\}(.+?)\\end\{align\}',
    # RL-specific patterns
    r'(V\s*[\(\_]\s*s\s*[\)]\s*=\s*[^,\n]{3,})',  # V(s) = ...
    r'(Q\s*[\(\_]\s*s\s*,\s*a\s*[\)]\s*=\s*[^,\n]{3,})',  # Q(s,a) = ...
    r'(V\s*[\*π]\s*[\(]\s*s\s*[\)]\s*=\s*[^,\n]{3,})',  # V*(s) or Vπ(s) = ...
    r'(G\s*_?\s*t\s*=\s*[^,\n]{3,})',  # G_t = ...
    r'(π\s*[\(]\s*a\s*\|\s*s\s*[\)]\s*=?\s*[^,\n]{3,})',  # π(a|s) = ...
    r'(ρ\s*[^,\n]{3,}=\s*[^,\n]{3,})',  # ρ (importance sampling ratio)
    r'(E\s*[\[_]\s*[^,\n\]]{3,}[\]]?\s*=?\s*[^,\n]{3,})',  # E[...] = ...
    # General variable = expression
    r'([A-Za-z_][A-Za-z0-9_]*\s*=\s*[^,\n]{5,})',
    # Math expressions with operators
    r'(\d+\.?\d*\s*[+\-*/×÷=<>≤≥≈∝∞∫∑∏√]\s*[^,\n]+)',
    # Greek letters indicating equations
    r'([αβγδεζηθικλμνξοπρστυφχψωΓΔΘΛΠΣΦΨΩ][^,\n]{3,}=.+)',
    # Subscript/superscript patterns
    r'([A-Z][a-z]*(?:_\{?[a-z0-9]+\}?)?(?:\^\{?[a-z0-9+\-*]+\}?)?\s*=.+)',
    # Summation patterns (common in RL)
    r'(∑[^,\n]{5,})',
    r'(Σ[^,\n]{5,})',
    # Arrow-based update rules
    r'([A-Za-z_]+\s*[←→]\s*[^,\n]{3,})',
]

PROBLEM_PATTERNS = [
    r'(?:Example|EXAMPLE)\s*(\d+[\.\d]*)',
    r'(?:Problem|PROBLEM)\s*(\d+[\.\d]*)',
    r'(?:Exercise|EXERCISE)\s*(\d+[\.\d]*)',
    r'(?:Sample Problem|Worked Example)\s*(\d+[\.\d]*)?',
    r'(?:Solution|SOLUTION)[\s:]+',
    r'(?:Q\.|Question)\s*(\d+)',
    # RL-specific
    r'(?:Consider the (?:MDP|grid|gridworld|environment))',
    r'(?:Apply (?:policy iteration|value iteration|Monte Carlo))',
    r'(?:Calculate|Compute|Find|Determine)\s+(?:the\s+)?(?:value|V|Q|policy|return)',
]

SECTION_PATTERNS = [
    r'^(?:Chapter|CHAPTER)\s+(\d+)[:\.]?\s*(.+)$',
    r'^(\d+(?:\.\d+)*)[:\.\s]+(.+)$',
    r'^(?:Section|SECTION)\s+(\d+(?:\.\d+)*)[:\.]?\s*(.+)$',
    r'^([A-Z][A-Z\s]{2,}[A-Z])$',
    # RL-specific section patterns
    r'^(?:Module|MODULE)\s+(\d+)',
    r'^(?:Dynamic Programming|Monte Carlo|Importance Sampling|Policy|Value)',
]

# Unicode to LaTeX mapping for RL symbols
UNICODE_TO_LATEX = {
    'π': r'\pi',
    'γ': r'\gamma',
    'α': r'\alpha',
    'β': r'\beta',
    'δ': r'\delta',
    'ε': r'\epsilon',
    'θ': r'\theta',
    'λ': r'\lambda',
    'μ': r'\mu',
    'σ': r'\sigma',
    'ρ': r'\rho',
    'τ': r'\tau',
    'Σ': r'\sum',
    '∑': r'\sum',
    '∏': r'\prod',
    '∞': r'\infty',
    '∫': r'\int',
    '√': r'\sqrt',
    '≤': r'\leq',
    '≥': r'\geq',
    '≈': r'\approx',
    '≠': r'\neq',
    '←': r'\leftarrow',
    '→': r'\rightarrow',
    '∈': r'\in',
    '∀': r'\forall',
    '∃': r'\exists',
    '∝': r'\propto',
    'Δ': r'\Delta',
    '×': r'\times',
    '÷': r'\div',
    '·': r'\cdot',
    '′': "'",
}

# ============================================================================
# PDF EXTRACTION
# ============================================================================

def extract_from_pdf(filepath: str, output_dir: str) -> List[PageContent]:
    """Extract content from PDF using PyMuPDF (fitz)"""
    pages = []

    try:
        import fitz
    except ImportError:
        print("Installing PyMuPDF...")
        os.system(f"{sys.executable} -m pip install PyMuPDF")
        import fitz

    doc = fitz.open(filepath)
    filename = Path(filepath).name
    figures_dir = Path(output_dir) / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"  Processing {doc.page_count} pages from {filename}...")

    for page_num in range(doc.page_count):
        page = doc[page_num]

        text = page.get_text("text")
        blocks = page.get_text("dict")["blocks"]

        formatted_lines = []
        current_section = ""

        for block in blocks:
            if block["type"] == 0:  # Text block
                for line in block.get("lines", []):
                    line_text = ""
                    is_bold = False
                    font_size = 0

                    for span in line.get("spans", []):
                        line_text += span.get("text", "")
                        font_size = max(font_size, span.get("size", 0))
                        if "bold" in span.get("font", "").lower():
                            is_bold = True

                    line_text = line_text.strip()
                    if not line_text:
                        continue

                    if is_bold and font_size > 11:
                        formatted_lines.append(f"\n## {line_text}\n")
                        current_section = line_text
                    elif font_size > 13:
                        formatted_lines.append(f"\n# {line_text}\n")
                        current_section = line_text
                    else:
                        formatted_lines.append(line_text)

        formatted_text = "\n".join(formatted_lines)

        # Extract images
        figures = []
        image_list = page.get_images()
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)

                # Skip tiny images (icons, bullets)
                if pix.width < 20 or pix.height < 20:
                    pix = None
                    continue

                img_filename = f"{Path(filename).stem}_p{page_num+1}_img{img_index+1}.png"
                img_path = figures_dir / img_filename

                if pix.n < 5:
                    pix.save(str(img_path))
                else:
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.save(str(img_path))
                    pix1 = None

                caption = extract_figure_caption(text, img_index)

                figures.append(ExtractedFigure(
                    filename=img_filename,
                    source_file=filename,
                    page_or_slide=page_num + 1,
                    caption=caption,
                    width=pix.width,
                    height=pix.height
                ))
                pix = None
            except Exception as e:
                pass

        equations = extract_equations_from_text(text, filename, page_num + 1)
        problems = extract_problems_from_text(text, filename, page_num + 1)
        tables = extract_tables_from_page(page, filename, page_num + 1)

        page_content = PageContent(
            page_num=page_num + 1,
            source_file=filename,
            raw_text=text,
            formatted_text=formatted_text,
            section_header=current_section,
            equations=equations,
            problems=problems,
            figures=figures,
            tables=tables
        )
        pages.append(page_content)

    doc.close()
    return pages

def extract_tables_from_page(page, filename: str, page_num: int) -> List[ExtractedTable]:
    """Extract tables from a PDF page using text analysis"""
    tables = []

    try:
        import tabula
        dfs = tabula.read_pdf(page.parent.name, pages=page_num, multiple_tables=True)
        for df in dfs:
            if df is not None and not df.empty:
                tables.append(ExtractedTable(
                    headers=list(df.columns),
                    rows=[[str(cell) for cell in row] for row in df.values],
                    source_file=filename,
                    page_or_slide=page_num
                ))
    except Exception:
        # Fallback: detect table-like structures in text via line analysis
        text = page.get_text("text")
        lines = text.split('\n')
        table_lines = []
        for line in lines:
            # Heuristic: lines with multiple tab/multi-space separations are table rows
            cells = re.split(r'\s{2,}|\t', line.strip())
            if len(cells) >= 3:
                table_lines.append(cells)
            elif table_lines and len(table_lines) >= 2:
                # End of table block - save it
                max_cols = max(len(row) for row in table_lines)
                # Pad rows to same length
                padded = [row + [''] * (max_cols - len(row)) for row in table_lines]
                tables.append(ExtractedTable(
                    headers=padded[0],
                    rows=padded[1:],
                    source_file=filename,
                    page_or_slide=page_num
                ))
                table_lines = []

        if len(table_lines) >= 2:
            max_cols = max(len(row) for row in table_lines)
            padded = [row + [''] * (max_cols - len(row)) for row in table_lines]
            tables.append(ExtractedTable(
                headers=padded[0],
                rows=padded[1:],
                source_file=filename,
                page_or_slide=page_num
            ))

    return tables

# ============================================================================
# POWERPOINT EXTRACTION (Enhanced)
# ============================================================================

def _extract_text_from_shape(shape, depth=0) -> List[str]:
    """Recursively extract text from a shape, handling groups and nested shapes"""
    texts = []
    max_depth = 5  # Prevent infinite recursion

    if depth > max_depth:
        return texts

    # Handle group shapes
    if shape.shape_type is not None:
        try:
            from pptx.enum.shapes import MSO_SHAPE_TYPE
            if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
                for child_shape in shape.shapes:
                    texts.extend(_extract_text_from_shape(child_shape, depth + 1))
                return texts
        except (ImportError, AttributeError):
            pass

    # Handle text frames
    if hasattr(shape, "text_frame"):
        try:
            for para in shape.text_frame.paragraphs:
                para_text = para.text.strip()
                if para_text:
                    texts.append(para_text)
        except Exception:
            pass
    elif hasattr(shape, "text"):
        text = shape.text.strip()
        if text:
            texts.append(text)

    return texts


def _get_shape_title_status(shape) -> Tuple[bool, str]:
    """Check if a shape is a title placeholder and return its text"""
    try:
        from pptx.enum.shapes import MSO_SHAPE_TYPE
        if hasattr(shape, "placeholder_format") and shape.placeholder_format is not None:
            pf_type = shape.placeholder_format.type
            if pf_type is not None and pf_type.name in ['TITLE', 'CENTER_TITLE', 'SUBTITLE']:
                return True, shape.text.strip()
    except (AttributeError, ImportError):
        pass
    return False, ""


def extract_from_pptx(filepath: str, output_dir: str) -> List[PageContent]:
    """Extract content from PowerPoint files with enhanced shape handling"""
    pages = []

    try:
        from pptx import Presentation
    except ImportError:
        print("Installing python-pptx...")
        os.system(f"{sys.executable} -m pip install python-pptx")
        from pptx import Presentation

    prs = Presentation(filepath)
    filename = Path(filepath).name
    figures_dir = Path(output_dir) / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"  Processing {len(prs.slides)} slides from {filename}...")

    all_notes = []

    for slide_num, slide in enumerate(prs.slides, 1):
        text_content = []
        formatted_content = []
        figures = []
        tables = []
        current_section = ""

        # First pass: identify title
        for shape in slide.shapes:
            is_title, title_text = _get_shape_title_status(shape)
            if is_title and title_text:
                current_section = title_text
                formatted_content.append(f"# {title_text}")
                text_content.append(title_text)
                break

        # Second pass: extract all content
        for shape in slide.shapes:
            is_title, _ = _get_shape_title_status(shape)
            if is_title:
                continue  # Already handled

            # Extract text (handles groups, nested shapes)
            shape_texts = _extract_text_from_shape(shape)
            for t in shape_texts:
                text_content.append(t)

                # Detect if this looks like a bullet point or sub-header
                if t.isupper() and len(t.split()) <= 6:
                    formatted_content.append(f"## {t}")
                else:
                    formatted_content.append(t)

            # Extract images
            if hasattr(shape, "image"):
                try:
                    image = shape.image
                    img_bytes = image.blob
                    img_ext = image.ext or "png"
                    img_filename = f"{Path(filename).stem}_s{slide_num}_img{len(figures)+1}.{img_ext}"
                    img_path = figures_dir / img_filename

                    with open(img_path, "wb") as f:
                        f.write(img_bytes)

                    # Get image dimensions
                    w, h = 0, 0
                    try:
                        from PIL import Image as PILImage
                        with PILImage.open(img_path) as im:
                            w, h = im.size
                    except Exception:
                        pass

                    figures.append(ExtractedFigure(
                        filename=img_filename,
                        source_file=filename,
                        page_or_slide=slide_num,
                        width=w,
                        height=h
                    ))
                except Exception:
                    pass

            # Extract tables (FIXED: was TODO)
            if shape.has_table:
                try:
                    table = shape.table
                    if len(table.rows) > 0:
                        headers = [cell.text.strip() for cell in table.rows[0].cells]
                        rows = []
                        for row_idx, row in enumerate(table.rows):
                            if row_idx == 0:
                                continue
                            rows.append([cell.text.strip() for cell in row.cells])

                        tables.append(ExtractedTable(
                            headers=headers,
                            rows=rows,
                            source_file=filename,
                            page_or_slide=slide_num
                        ))
                except Exception:
                    pass

        # Extract speaker notes
        notes_text = ""
        if slide.has_notes_slide:
            try:
                notes_text = slide.notes_slide.notes_text_frame.text.strip()
                if notes_text:
                    text_content.append(f"\n[Speaker Notes]\n{notes_text}")
                    all_notes.append(SlideNote(
                        source_file=filename,
                        slide_num=slide_num,
                        slide_title=current_section,
                        notes_text=notes_text
                    ))
            except Exception:
                pass

        raw_text = "\n".join(text_content)
        formatted_text = "\n".join(formatted_content)

        equations = extract_equations_from_text(raw_text, filename, slide_num)
        problems = extract_problems_from_text(raw_text, filename, slide_num)

        page_content = PageContent(
            page_num=slide_num,
            source_file=filename,
            raw_text=raw_text,
            formatted_text=formatted_text,
            section_header=current_section,
            equations=equations,
            problems=problems,
            figures=figures,
            tables=tables,
            notes=notes_text
        )
        pages.append(page_content)

    # Store notes on the result (attached via a simple attribute hack)
    # The main function will collect these
    extract_from_pptx._last_notes = all_notes

    return pages

# ============================================================================
# WORD DOCUMENT EXTRACTION
# ============================================================================

def extract_from_docx(filepath: str, output_dir: str) -> List[PageContent]:
    """Extract content from Word documents"""
    try:
        from docx import Document
    except ImportError:
        print("Installing python-docx...")
        os.system(f"{sys.executable} -m pip install python-docx")
        from docx import Document

    doc = Document(filepath)
    filename = Path(filepath).name
    figures_dir = Path(output_dir) / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"  Processing {filename}...")

    pages = []
    current_page = None
    page_num = 0

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        is_heading = para.style.name.startswith('Heading')

        if is_heading or current_page is None:
            if current_page is not None:
                current_page.equations = extract_equations_from_text(
                    current_page.raw_text, filename, current_page.page_num
                )
                current_page.problems = extract_problems_from_text(
                    current_page.raw_text, filename, current_page.page_num
                )
                pages.append(current_page)

            page_num += 1
            current_page = PageContent(
                page_num=page_num,
                source_file=filename,
                raw_text="",
                formatted_text="",
                section_header=text if is_heading else ""
            )

        if is_heading:
            level = int(para.style.name[-1]) if para.style.name[-1].isdigit() else 1
            current_page.formatted_text += f"\n{'#' * level} {text}\n"
        else:
            current_page.formatted_text += f"{text}\n"

        current_page.raw_text += f"{text}\n"

    if current_page is not None:
        current_page.equations = extract_equations_from_text(
            current_page.raw_text, filename, current_page.page_num
        )
        current_page.problems = extract_problems_from_text(
            current_page.raw_text, filename, current_page.page_num
        )
        pages.append(current_page)

    # Extract tables
    for table_idx, table in enumerate(doc.tables):
        headers = [cell.text.strip() for cell in table.rows[0].cells]
        rows = [[cell.text.strip() for cell in row.cells] for row in table.rows[1:]]

        extracted_table = ExtractedTable(
            headers=headers,
            rows=rows,
            source_file=filename,
            page_or_slide=1
        )
        if pages:
            pages[0].tables.append(extracted_table)

    return pages

# ============================================================================
# IMAGE EXTRACTION (OCR)
# ============================================================================

def extract_from_image(filepath: str, output_dir: str) -> List[PageContent]:
    """Extract text from images using OCR with preprocessing"""
    try:
        from PIL import Image, ImageFilter, ImageEnhance
    except ImportError:
        print("Installing Pillow...")
        os.system(f"{sys.executable} -m pip install Pillow")
        from PIL import Image, ImageFilter, ImageEnhance

    has_tesseract = True
    try:
        import pytesseract
    except ImportError:
        print("Installing pytesseract...")
        os.system(f"{sys.executable} -m pip install pytesseract")
        try:
            import pytesseract
        except ImportError:
            has_tesseract = False
            print("  Warning: pytesseract installed but Tesseract binary may not be available")

    filename = Path(filepath).name
    print(f"  Processing image {filename}...")

    try:
        image = Image.open(filepath)

        # Preprocess for better OCR
        # Convert to grayscale
        if image.mode != 'L':
            gray = image.convert('L')
        else:
            gray = image

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(1.5)

        # Sharpen
        sharpened = enhanced.filter(ImageFilter.SHARPEN)

        text = ""
        if has_tesseract:
            try:
                # Try with preprocessed image first
                text = pytesseract.image_to_string(sharpened)
                # If very little text, try original
                if len(text.strip()) < 20:
                    text_orig = pytesseract.image_to_string(image)
                    if len(text_orig.strip()) > len(text.strip()):
                        text = text_orig
            except Exception as e:
                print(f"  Warning: OCR failed for {filename}: {e}")
                text = f"[OCR failed - image saved for manual review: {filename}]"
        else:
            text = f"[Tesseract not available - image saved for manual review: {filename}]"

        # Copy image to figures directory
        figures_dir = Path(output_dir) / "figures"
        figures_dir.mkdir(parents=True, exist_ok=True)

        import shutil
        dest_path = figures_dir / filename
        shutil.copy(filepath, dest_path)

        w, h = image.size

        figure = ExtractedFigure(
            filename=filename,
            source_file=filename,
            page_or_slide=1,
            description="OCR extracted from image",
            width=w,
            height=h
        )

        equations = extract_equations_from_text(text, filename, 1)
        problems = extract_problems_from_text(text, filename, 1)

        return [PageContent(
            page_num=1,
            source_file=filename,
            raw_text=text,
            formatted_text=text,
            figures=[figure],
            equations=equations,
            problems=problems
        )]
    except Exception as e:
        print(f"  Warning: Could not process image {filename}: {e}")
        return []

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def extract_figure_caption(text: str, img_index: int) -> str:
    """Try to find figure caption near image reference"""
    patterns = [
        rf'(?:Figure|Fig\.?)\s*{img_index + 1}[:\.]?\s*([^\n]+)',
        rf'(?:Figure|Fig\.?)\s*\d+[:\.]?\s*([^\n]+)',
        # RL-specific patterns
        rf'(?:Backup diagram|State diagram|Grid\s*world|MDP)[:\s]*([^\n]*)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return ""

def unicode_to_latex(text: str) -> str:
    """Convert Unicode math symbols to LaTeX equivalents"""
    result = text
    for unicode_char, latex_cmd in UNICODE_TO_LATEX.items():
        result = result.replace(unicode_char, latex_cmd)
    return result

def extract_equations_from_text(text: str, filename: str, page_num: int) -> List[ExtractedEquation]:
    """Extract equations from text content with RL-aware patterns"""
    equations = []
    seen = set()

    for pattern in EQUATION_PATTERNS:
        try:
            matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)
            for match in matches:
                eq_text = match.group(1) if match.groups() else match.group(0)
                eq_text = eq_text.strip()

                if len(eq_text) < 3 or eq_text in seen:
                    continue

                if re.match(r'^[\d\s.,]+$', eq_text):
                    continue

                # Skip common false positives
                if eq_text.lower() in ('the', 'and', 'for', 'with', 'from', 'that', 'this'):
                    continue

                seen.add(eq_text)

                # Get context
                start = max(0, match.start() - 80)
                end = min(len(text), match.end() + 80)
                context = text[start:end].replace('\n', ' ')

                # Check if numbered
                eq_num_match = re.search(r'\((\d+(?:\.\d+)?)\)', context)

                # Attempt LaTeX conversion
                latex_form = unicode_to_latex(eq_text)

                equations.append(ExtractedEquation(
                    content=eq_text,
                    source_file=filename,
                    page_or_slide=page_num,
                    context=context,
                    is_numbered=eq_num_match is not None,
                    equation_number=eq_num_match.group(1) if eq_num_match else "",
                    latex_form=latex_form
                ))
        except Exception:
            continue

    return equations

def extract_problems_from_text(text: str, filename: str, page_num: int) -> List[ExtractedProblem]:
    """Extract worked examples and problems from text"""
    problems = []

    for pattern in PROBLEM_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
            start_pos = match.start()
            problem_num = ""
            if match.groups():
                problem_num = match.group(1) if match.group(1) else ""

            remaining_text = text[start_pos:]

            end_match = re.search(
                r'\n(?:Example|Problem|Exercise|Q\.|Question)\s+\d+',
                remaining_text[100:],
                re.IGNORECASE
            )

            if end_match:
                problem_text = remaining_text[:100 + end_match.start()]
            else:
                problem_text = remaining_text[:1500]  # Increased from 1000
                double_nl = problem_text.find('\n\n\n')
                if double_nl > 100:
                    problem_text = problem_text[:double_nl]

            # Determine problem type
            match_text = match.group(0).lower()
            problem_type = "Example"
            if "problem" in match_text:
                problem_type = "Problem"
            elif "exercise" in match_text:
                problem_type = "Exercise"
            elif "question" in match_text or "q." in match_text:
                problem_type = "Question"
            elif "consider" in match_text or "apply" in match_text:
                problem_type = "Application"
            elif "calculate" in match_text or "compute" in match_text or "find" in match_text:
                problem_type = "Calculation"

            # Split problem from solution
            solution_split = re.search(r'(?:Solution|Answer|Ans|Result)[:\s]', problem_text, re.IGNORECASE)

            if solution_split:
                prob_text = problem_text[:solution_split.start()].strip()
                sol_text = problem_text[solution_split.end():].strip()
            else:
                prob_text = problem_text.strip()
                sol_text = ""

            problems.append(ExtractedProblem(
                title=f"{problem_type} {problem_num}".strip(),
                problem_text=prob_text[:800],
                solution_text=sol_text[:2000],  # Increased for longer RL solutions
                source_file=filename,
                page_or_slide=page_num,
                problem_type=problem_type
            ))

    return problems

def build_section_hierarchy(pages: List[PageContent]) -> Dict[str, List[str]]:
    """Build hierarchy of sections from extracted content"""
    hierarchy = defaultdict(list)
    current_chapter = ""

    for page in pages:
        header = page.section_header or ""

        chapter_match = re.match(r'^(?:Chapter|CHAPTER|Module|MODULE)\s+\d+', header)
        if chapter_match or (header.isupper() and len(header.split()) <= 6):
            current_chapter = header
            hierarchy[current_chapter] = []
        elif header and current_chapter:
            if header not in hierarchy[current_chapter]:
                hierarchy[current_chapter].append(header)
        elif header:
            if header not in hierarchy.get("Main", []):
                hierarchy["Main"].append(header)

    return dict(hierarchy)

# ============================================================================
# MAIN EXTRACTION FUNCTION
# ============================================================================

def extract_course_material(input_path: str, output_dir: str) -> ExtractionResult:
    """Main extraction function"""
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_pages = []
    all_notes: List[SlideNote] = []
    source_files = []
    warnings = []

    if input_path.is_file():
        files = [input_path]
    else:
        files = sorted(input_path.glob("**/*"))

    # Filter to supported types only
    supported_extensions = {'.pdf', '.pptx', '.docx', '.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
    files = [f for f in files if f.is_file() and f.suffix.lower() in supported_extensions]

    print(f"\nExtracting from {len(files)} file(s)...")
    for f in files:
        print(f"  Found: {f.name}")

    for filepath in files:
        ext = filepath.suffix.lower()
        source_files.append(str(filepath))

        try:
            # Reset notes collector
            extract_from_pptx._last_notes = []

            if ext == '.pdf':
                pages = extract_from_pdf(str(filepath), str(output_dir))
            elif ext == '.pptx':
                pages = extract_from_pptx(str(filepath), str(output_dir))
                # Collect notes from PPTX
                all_notes.extend(getattr(extract_from_pptx, '_last_notes', []))
            elif ext == '.docx':
                pages = extract_from_docx(str(filepath), str(output_dir))
            elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
                pages = extract_from_image(str(filepath), str(output_dir))
            else:
                warnings.append(f"Unsupported file type: {filepath}")
                continue

            all_pages.extend(pages)

        except Exception as e:
            warnings.append(f"Error processing {filepath}: {str(e)}")
            import traceback
            traceback.print_exc()

    # Aggregate content
    all_equations = []
    all_problems = []
    all_figures = []
    all_tables = []

    for page in all_pages:
        all_equations.extend(page.equations)
        all_problems.extend(page.problems)
        all_figures.extend(page.figures)
        all_tables.extend(page.tables)

    hierarchy = build_section_hierarchy(all_pages)

    result = ExtractionResult(
        source_files=source_files,
        total_pages=len(all_pages),
        pages=all_pages,
        all_equations=all_equations,
        all_problems=all_problems,
        all_figures=all_figures,
        all_tables=all_tables,
        all_notes=all_notes,
        section_hierarchy=hierarchy,
        extraction_time=datetime.now().isoformat(),
        warnings=warnings
    )

    return result

# Initialize the notes collector
extract_from_pptx._last_notes = []

# ============================================================================
# OUTPUT WRITERS (Enhanced for Obsidian)
# ============================================================================

def write_raw_text(result: ExtractionResult, output_dir: Path):
    """Write raw text output"""
    with open(output_dir / "raw_text.txt", "w", encoding="utf-8") as f:
        for page in result.pages:
            f.write(f"\n{'='*60}\n")
            f.write(f"[{page.source_file}] Page/Slide {page.page_num}\n")
            if page.section_header:
                f.write(f"Section: {page.section_header}\n")
            f.write(f"{'='*60}\n\n")
            f.write(page.raw_text)
            f.write("\n")

def write_structured_markdown(result: ExtractionResult, output_dir: Path):
    """Write Obsidian-formatted structured markdown"""
    with open(output_dir / "structured.md", "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("type: extraction\n")
        f.write(f"date: {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"sources: {len(result.source_files)}\n")
        f.write("tags: [rl, cat2, extracted]\n")
        f.write("---\n\n")

        f.write("# Extracted Course Content\n\n")
        f.write(f"**Source Files**: {', '.join(Path(s).name for s in result.source_files)}\n\n")
        f.write(f"**Total Pages/Slides**: {result.total_pages}\n\n")
        f.write(f"**Extraction Time**: {result.extraction_time}\n\n")

        f.write("---\n\n")

        # Table of Contents
        f.write("## Table of Contents\n\n")
        for chapter, sections in result.section_hierarchy.items():
            f.write(f"- **{chapter}**\n")
            for section in sections:
                f.write(f"  - {section}\n")
        f.write("\n---\n\n")

        # Content by page
        current_source = ""
        for page in result.pages:
            if page.source_file != current_source:
                f.write(f"\n# Source: {page.source_file}\n\n")
                current_source = page.source_file

            f.write(f"\n## Slide {page.page_num}")
            if page.section_header:
                f.write(f": {page.section_header}")
            f.write("\n\n")

            f.write(page.formatted_text or page.raw_text)
            f.write("\n")

            # Figures using Obsidian wiki-link syntax
            if page.figures:
                f.write("\n> [!figure] Figures on this slide\n")
                for fig in page.figures:
                    caption = fig.caption if fig.caption else fig.filename
                    f.write(f"> ![[{fig.filename}|{caption}]]\n")
                f.write("\n")

            # Tables
            if page.tables:
                for table in page.tables:
                    f.write("\n| " + " | ".join(table.headers) + " |\n")
                    f.write("|" + "|".join(["---"] * len(table.headers)) + "|\n")
                    for row in table.rows:
                        f.write("| " + " | ".join(row) + " |\n")
                    f.write("\n")

            # Speaker notes
            if page.notes:
                f.write(f"\n> [!tip] Speaker Notes (Slide {page.page_num})\n")
                for line in page.notes.split('\n'):
                    f.write(f"> {line}\n")
                f.write("\n")

def write_equations_json(result: ExtractionResult, output_dir: Path):
    """Write equations to JSON"""
    equations_data = [asdict(eq) for eq in result.all_equations]
    with open(output_dir / "equations.json", "w", encoding="utf-8") as f:
        json.dump(equations_data, f, indent=2, ensure_ascii=False)

def write_problems_json(result: ExtractionResult, output_dir: Path):
    """Write problems to JSON"""
    problems_data = [asdict(p) for p in result.all_problems]
    with open(output_dir / "problems.json", "w", encoding="utf-8") as f:
        json.dump(problems_data, f, indent=2, ensure_ascii=False)

def write_tables_json(result: ExtractionResult, output_dir: Path):
    """Write tables to JSON"""
    tables_data = [asdict(t) for t in result.all_tables]
    with open(output_dir / "tables.json", "w", encoding="utf-8") as f:
        json.dump(tables_data, f, indent=2, ensure_ascii=False)

def write_slide_notes(result: ExtractionResult, output_dir: Path):
    """Write all speaker notes to a dedicated file"""
    with open(output_dir / "slide_notes.md", "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("type: speaker-notes\n")
        f.write("tags: [rl, cat2, notes]\n")
        f.write("---\n\n")
        f.write("# Speaker Notes from All Slides\n\n")
        f.write("These notes often contain exam hints, emphasis points, and additional explanations.\n\n")
        f.write("---\n\n")

        if not result.all_notes:
            f.write("*No speaker notes found in any slides.*\n")
        else:
            current_source = ""
            for note in result.all_notes:
                if note.source_file != current_source:
                    f.write(f"## {note.source_file}\n\n")
                    current_source = note.source_file

                title = f" - {note.slide_title}" if note.slide_title else ""
                f.write(f"### Slide {note.slide_num}{title}\n\n")
                f.write(f"{note.notes_text}\n\n")

def write_extraction_summary(result: ExtractionResult, output_dir: Path):
    """Write extraction summary"""
    with open(output_dir / "extraction_summary.md", "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("type: summary\n")
        f.write("tags: [rl, cat2, extraction]\n")
        f.write("---\n\n")
        f.write("# Extraction Summary\n\n")

        f.write("## Overview\n\n")
        f.write("| Metric | Count |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Source Files | {len(result.source_files)} |\n")
        f.write(f"| Total Pages/Slides | {result.total_pages} |\n")
        f.write(f"| Equations Detected | {len(result.all_equations)} |\n")
        f.write(f"| Problems/Examples | {len(result.all_problems)} |\n")
        f.write(f"| Figures Extracted | {len(result.all_figures)} |\n")
        f.write(f"| Tables Extracted | {len(result.all_tables)} |\n")
        f.write(f"| Speaker Notes | {len(result.all_notes)} |\n")

        f.write("\n## Source Files\n\n")
        for src in result.source_files:
            f.write(f"- `{Path(src).name}`\n")

        f.write("\n## Slide-by-Slide Coverage\n\n")
        current_source = ""
        for page in result.pages:
            if page.source_file != current_source:
                f.write(f"\n### {page.source_file}\n\n")
                f.write("| Slide | Title | Equations | Figures | Tables | Notes |\n")
                f.write("|-------|-------|-----------|---------|--------|-------|\n")
                current_source = page.source_file
            title = page.section_header or "(no title)"
            has_notes = "Yes" if page.notes else "No"
            f.write(f"| {page.page_num} | {title} | {len(page.equations)} | {len(page.figures)} | {len(page.tables)} | {has_notes} |\n")

        f.write("\n## Section Hierarchy\n\n")
        for chapter, sections in result.section_hierarchy.items():
            f.write(f"### {chapter}\n")
            for section in sections:
                f.write(f"- {section}\n")
            f.write("\n")

        f.write("\n## Equations Found\n\n")
        for i, eq in enumerate(result.all_equations, 1):
            latex = f" → `{eq.latex_form}`" if eq.latex_form != eq.content else ""
            f.write(f"{i}. `{eq.content}`{latex} (Slide {eq.page_or_slide}, {eq.source_file})\n")

        f.write("\n## Problems/Examples Found\n\n")
        for prob in result.all_problems:
            f.write(f"- **{prob.title}** [{prob.problem_type}] (Slide {prob.page_or_slide}, {prob.source_file})\n")

        if result.warnings:
            f.write("\n## Warnings\n\n")
            f.write("> [!warning] Extraction Issues\n")
            for warning in result.warnings:
                f.write(f"> - {warning}\n")

        f.write(f"\n---\n\n*Extracted at: {result.extraction_time}*\n")

# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Extract content from course materials (PDF, PPTX, DOCX, images) for Obsidian study guides"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input file or directory path"
    )
    parser.add_argument(
        "--output", "-o",
        default="extracted_content",
        help="Output directory (default: extracted_content)"
    )
    args = parser.parse_args()

    result = extract_course_material(args.input, args.output)
    save_extraction_results(result, args.output)

    return result

def save_extraction_results(result: ExtractionResult, output_dir: str):
    """Save all extraction outputs"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("\nWriting output files...")

    write_raw_text(result, output_path)
    print("  - raw_text.txt")

    write_structured_markdown(result, output_path)
    print("  - structured.md")

    write_equations_json(result, output_path)
    print(f"  - equations.json ({len(result.all_equations)} equations)")

    write_problems_json(result, output_path)
    print(f"  - problems.json ({len(result.all_problems)} problems)")

    write_tables_json(result, output_path)
    print(f"  - tables.json ({len(result.all_tables)} tables)")

    write_slide_notes(result, output_path)
    print(f"  - slide_notes.md ({len(result.all_notes)} notes)")

    write_extraction_summary(result, output_path)
    print("  - extraction_summary.md")

    print(f"\nExtraction complete! Output saved to: {output_path}")
    print(f"\nSummary:")
    print(f"  Files processed: {len(result.source_files)}")
    print(f"  Slides/Pages: {result.total_pages}")
    print(f"  Equations: {len(result.all_equations)}")
    print(f"  Problems: {len(result.all_problems)}")
    print(f"  Figures: {len(result.all_figures)}")
    print(f"  Tables: {len(result.all_tables)}")
    print(f"  Speaker Notes: {len(result.all_notes)}")
    if result.warnings:
        print(f"  Warnings: {len(result.warnings)}")

if __name__ == "__main__":
    main()
