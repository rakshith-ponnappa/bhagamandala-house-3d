#!/usr/bin/env python3
"""
Convert Bhagamandala house plan markdown docs to WhatsApp-friendly PDFs.
Supports English, Kannada, Malayalam with proper Unicode fonts.
Optimized for low-cost Android phones.
"""

import os
import re
from fpdf import FPDF

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE, 'fonts')


class HousePlanPDF(FPDF):
    """Custom PDF with header/footer and multi-script support."""

    def __init__(self, title, subtitle, lang='en'):
        super().__init__()
        self.doc_title = title
        self.doc_subtitle = subtitle
        self.lang = lang
        self.set_auto_page_break(auto=True, margin=20)
        self._setup_fonts()

    def _setup_fonts(self):
        # Arial Unicode MS - supports Latin + Kannada + Malayalam (Regular only)
        self.add_font('ArialUni', '', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
        # Arial for bold (Latin only)
        self.add_font('Arial', '', '/System/Library/Fonts/Supplemental/Arial.ttf')
        self.add_font('Arial', 'B', '/System/Library/Fonts/Supplemental/Arial Bold.ttf')

        # Kannada font (has Bold)
        kn_regular = os.path.join(FONT_DIR, 'NotoSansKannada-Regular.ttf')
        kn_bold = os.path.join(FONT_DIR, 'NotoSansKannada-Bold.ttf')
        if os.path.exists(kn_regular):
            self.add_font('Kannada', '', kn_regular)
            self.add_font('Kannada', 'B', kn_bold)

        # Malayalam font (has Bold)
        ml_regular = os.path.join(FONT_DIR, 'MalayalamSangamMN-Regular.ttf')
        ml_bold = os.path.join(FONT_DIR, 'MalayalamSangamMN-Bold.ttf')
        if os.path.exists(ml_regular):
            self.add_font('Malayalam', '', ml_regular)
            self.add_font('Malayalam', 'B', ml_bold)

        # Set fallback fonts so Latin chars render in Indic docs
        # and Indic chars render in English docs
        self.set_fallback_fonts(['ArialUni', 'Arial'])

    def _get_font(self, bold=False):
        style = 'B' if bold else ''
        if self.lang == 'kn':
            return 'Kannada', style
        elif self.lang == 'ml':
            return 'Malayalam', style
        # English: ArialUni supports all scripts (no Bold variant)
        # Use ArialUni for regular, Arial for bold
        if bold:
            return 'Arial', 'B'
        return 'ArialUni', ''

    def header(self):
        font, style = self._get_font(bold=True)
        self.set_font(font, style, 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, self.doc_title, align='C')
        self.ln(4)
        self.set_draw_color(200, 100, 0)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('ArialUni', '', 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} | {self.doc_subtitle}', align='C')


def md_to_pdf(md_path, pdf_path, title, subtitle, lang='en'):
    """Convert a markdown file to a styled PDF."""
    pdf = HousePlanPDF(title, subtitle, lang)
    pdf.alias_nb_pages()
    pdf.add_page()

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    in_code = False
    table_rows = []
    col_count = 0

    for line in lines:
        line = line.rstrip('\n')

        # Skip empty lines
        if not line.strip():
            if in_table and table_rows:
                _render_table(pdf, table_rows, lang)
                table_rows = []
                in_table = False
                col_count = 0
            if not in_code:
                pdf.ln(2)
            continue

        # Code blocks
        if line.strip().startswith('```'):
            in_code = not in_code
            if in_code:
                pdf.ln(2)
            continue

        if in_code:
            # Use ArialUni for code blocks (supports all scripts including Kannada/Malayalam)
            pdf.set_font('ArialUni', '', 5.5)
            pdf.set_text_color(60, 60, 60)
            # Replace box-drawing chars with ASCII equivalents for PDF compatibility
            safe_line = line
            for old, new in [('═', '='), ('║', '|'), ('╔', '+'), ('╗', '+'),
                             ('╚', '+'), ('╝', '+'), ('╠', '+'), ('╣', '+'),
                             ('╦', '+'), ('╩', '+'), ('╬', '+'), ('━', '-'),
                             ('┃', '|'), ('┏', '+'), ('┓', '+'), ('┗', '+'),
                             ('┛', '+'), ('┣', '+'), ('┫', '+'), ('┳', '+'),
                             ('┻', '+'), ('╋', '+'), ('│', '|'), ('─', '-'),
                             ('┌', '+'), ('┐', '+'), ('└', '+'), ('┘', '+'),
                             ('├', '+'), ('┤', '+'), ('┬', '+'), ('┴', '+'),
                             ('·', '.'), ('→', '->'), ('↑', '^'), ('↓', 'v'),
                             ('★', '*'), ('✅', '[OK]'), ('✓', '[OK]')]:
                safe_line = safe_line.replace(old, new)
            try:
                pdf.set_x(10)  # Reset x position
                pdf.multi_cell(pdf.w - 20, 3.2, safe_line)
            except Exception:
                pass  # Skip lines that still can't render
            continue

        # Horizontal rule
        if line.strip() == '---':
            pdf.ln(3)
            pdf.set_draw_color(200, 200, 200)
            pdf.set_line_width(0.3)
            pdf.line(10, pdf.get_y(), pdf.w - 10, pdf.get_y())
            pdf.ln(3)
            continue

        # Headers
        if line.startswith('#'):
            level = len(line.split()[0])  # count #'s
            text = re.sub(r'^#+\s*', '', line)
            text = _clean_md(text)

            font, style = pdf._get_font(bold=True)
            sizes = {1: 16, 2: 13, 3: 11, 4: 10}
            size = sizes.get(level, 9)

            if level <= 2:
                pdf.ln(4)

            pdf.set_font(font, style, size)
            try:
                if level == 1:
                    pdf.set_fill_color(245, 240, 230)
                    pdf.set_text_color(30, 30, 30)
                    pdf.cell(0, 8, text, fill=True, new_x='LMARGIN', new_y='NEXT')
                elif level == 2:
                    pdf.set_text_color(140, 80, 0)
                    pdf.cell(0, 7, text, new_x='LMARGIN', new_y='NEXT')
                else:
                    pdf.set_text_color(60, 60, 60)
                    pdf.cell(0, 6, text, new_x='LMARGIN', new_y='NEXT')
            except Exception:
                # Fallback with ArialUni for mixed script headers
                if pdf.lang == 'en':
                    pdf.set_font('ArialUni', '', size)
                    pdf.cell(0, 7, text, new_x='LMARGIN', new_y='NEXT')

            pdf.ln(2)
            continue

        # Table rows
        if '|' in line and not line.strip().startswith('>'):
            cells = [c.strip() for c in line.split('|')]
            cells = [c for c in cells if c]  # remove empty from leading/trailing |

            # Skip separator rows
            if all(re.match(r'^[-:]+$', c) for c in cells):
                continue

            if not in_table:
                in_table = True
                col_count = len(cells)

            table_rows.append(cells)
            continue

        # If we were in a table and now hit non-table line
        if in_table and table_rows:
            _render_table(pdf, table_rows, lang)
            table_rows = []
            in_table = False
            col_count = 0

        # Blockquote
        if line.strip().startswith('>'):
            text = re.sub(r'^>\s*', '', line.strip())
            text = _clean_md(text)
            font, style = pdf._get_font()
            pdf.set_font(font, style, 8)
            pdf.set_text_color(100, 60, 0)
            pdf.set_x(15)
            pdf.set_draw_color(200, 150, 50)
            pdf.set_line_width(0.8)
            pdf.line(14, pdf.get_y(), 14, pdf.get_y() + 5)
            try:
                pdf.multi_cell(pdf.w - 25, 4.5, text)
            except Exception:
                pass
            pdf.set_text_color(0, 0, 0)
            pdf.ln(1)
            continue

        # List items
        if re.match(r'^(\s*[-*•]\s|\s*\d+\.\s)', line):
            text = re.sub(r'^(\s*[-*•]\s|\s*\d+\.\s)', '', line)
            text = _clean_md(text)
            indent = len(line) - len(line.lstrip())
            indent_mm = 5 + indent * 2

            font, style = pdf._get_font()
            # Check for bold prefix
            if text.startswith('**') or ':**' in line:
                bfont, bstyle = pdf._get_font(bold=True)
                pdf.set_font(bfont, bstyle, 8.5)
                pdf.set_text_color(40, 40, 40)
            else:
                pdf.set_font(font, style, 8.5)
                pdf.set_text_color(50, 50, 50)

            pdf.set_x(10 + indent_mm)
            bullet = '- ' if re.match(r'^\s*[-*•]', line) else re.match(r'^(\s*\d+\.)\s', line).group(1) + ' '
            try:
                pdf.multi_cell(pdf.w - 20 - indent_mm, 4.5, bullet + text)
            except Exception:
                pass
            continue

        # Regular paragraph
        text = _clean_md(line)
        font, style = pdf._get_font()
        if '**' in line:
            bfont, bstyle = pdf._get_font(bold=True)
            pdf.set_font(bfont, bstyle, 9)
            pdf.set_text_color(30, 30, 30)
        else:
            pdf.set_font(font, style, 9)
            pdf.set_text_color(50, 50, 50)
        try:
            pdf.set_x(10)
            pdf.multi_cell(pdf.w - 20, 4.5, text)
        except Exception:
            pass  # Skip lines that can't render

    # Flush remaining table
    if in_table and table_rows:
        _render_table(pdf, table_rows, lang)

    pdf.output(pdf_path)
    size_kb = os.path.getsize(pdf_path) / 1024
    print(f'  Saved: {os.path.basename(pdf_path)} ({size_kb:.0f} KB)')


def _clean_md(text):
    """Remove markdown formatting for plain text."""
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)       # italic
    text = re.sub(r'~~([^~]+)~~', r'\1', text)       # strikethrough
    text = re.sub(r'`([^`]+)`', r'\1', text)         # inline code
    return text.strip()


def _render_table(pdf, rows, lang='en'):
    """Render a markdown table as a PDF table."""
    if not rows:
        return

    pdf.ln(2)
    max_cols = max(len(r) for r in rows)

    # Calculate column widths based on content
    usable_w = pdf.w - 20  # margins
    col_widths = []

    for ci in range(max_cols):
        max_len = 0
        for row in rows:
            if ci < len(row):
                max_len = max(max_len, len(row[ci]))
        col_widths.append(max_len)

    total = sum(col_widths) or 1
    col_widths = [max(w / total * usable_w, 15) for w in col_widths]

    # Adjust if total exceeds page
    actual_total = sum(col_widths)
    if actual_total > usable_w:
        scale = usable_w / actual_total
        col_widths = [w * scale for w in col_widths]

    font_name = 'Kannada' if lang == 'kn' else ('Malayalam' if lang == 'ml' else 'ArialUni')

    for ri, row in enumerate(rows):
        is_header = (ri == 0)

        if is_header:
            if lang == 'en':
                pdf.set_font('Arial', 'B', 7.5)
            else:
                pdf.set_font(font_name, 'B', 7.5)
            pdf.set_fill_color(240, 235, 220)
            pdf.set_text_color(30, 30, 30)
        else:
            pdf.set_font(font_name, '', 7.5)
            pdf.set_text_color(50, 50, 50)
            if ri % 2 == 0:
                pdf.set_fill_color(250, 250, 248)
            else:
                pdf.set_fill_color(255, 255, 255)

        row_height = 5.5
        # Check if any cell needs wrapping
        for ci in range(min(len(row), max_cols)):
            text = _clean_md(row[ci]) if ci < len(row) else ''
            # Estimate lines needed
            char_width = col_widths[ci] / 3.5  # rough chars per line at 7.5pt
            if char_width > 0 and len(text) > char_width:
                lines = len(text) / char_width
                row_height = max(row_height, lines * 4)

        for ci in range(max_cols):
            text = _clean_md(row[ci]) if ci < len(row) else ''
            w = col_widths[ci] if ci < len(col_widths) else 20

            # Bold detection for cells starting with **
            if row[ci].strip().startswith('**') if ci < len(row) else False:
                if lang == 'en':
                    pdf.set_font('Arial', 'B', 7.5)
                else:
                    pdf.set_font(font_name, 'B', 7.5)

            try:
                pdf.cell(w, row_height, text[:80], border=1, fill=True)
            except Exception:
                # Fallback: try ArialUni for mixed script cells
                pdf.set_font('ArialUni', '', 7)
                try:
                    pdf.cell(w, row_height, text[:60], border=1, fill=True)
                except Exception:
                    pdf.cell(w, row_height, '...', border=1, fill=True)

            if is_header:
                if lang == 'en':
                    pdf.set_font('Arial', 'B', 7.5)
                else:
                    pdf.set_font(font_name, 'B', 7.5)
            else:
                pdf.set_font(font_name, '', 7.5)

        pdf.ln(row_height)

    pdf.ln(2)


def add_images_page(pdf, images_dir, lang='en'):
    """Add architectural plan images to the PDF."""
    image_files = [
        ('GF_Plan_v4.png', 'Ground Floor Plan'),
        ('FF_Plan_v4.png', 'First Floor Plan'),
        ('Site_Layout_v4.png', 'Site Layout'),
        ('Front_Elevation_v4.png', 'Front Elevation (East)'),
        ('Back_Elevation_v4.png', 'Back Elevation (West)'),
        ('Roof_Solar_v4.png', 'Roof + Solar Layout'),
    ]

    for fname, label in image_files:
        fpath = os.path.join(images_dir, fname)
        if not os.path.exists(fpath):
            continue

        pdf.add_page('L')  # Landscape for images
        font, _ = pdf._get_font(bold=True)
        pdf.set_font(font, 'B', 12)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 8, label, align='C', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(2)

        # Fit image to page
        max_w = pdf.w - 20
        max_h = pdf.h - 45
        pdf.image(fpath, x=10, y=pdf.get_y(), w=max_w, h=0, keep_aspect_ratio=True)


def generate_all_pdfs():
    """Generate all WhatsApp-friendly PDFs."""
    print('Generating WhatsApp-friendly PDFs...\n')

    # 1. English PDF (with images)
    print('[1/4] English Construction Plan + Images')
    en_md = os.path.join(BASE, 'Bhagamandala_House_Construction_Plan_v4.md')
    en_pdf = os.path.join(BASE, 'Bhagamandala_House_Plan_EN_v4.pdf')
    md_to_pdf(en_md, en_pdf,
              'BHAGAMANDALA HOUSE - CONSTRUCTION PLAN (v4)',
              'Bhagamandala-Talakaveri Road, Kodagu | April 2026',
              lang='en')

    # 2. Kannada PDF
    print('[2/4] Kannada Construction Plan')
    kn_md = os.path.join(BASE, 'Bhagamandala_Mane_Kannada_v4.md')
    kn_pdf = os.path.join(BASE, 'Bhagamandala_Mane_Kannada_v4.pdf')
    md_to_pdf(kn_md, kn_pdf,
              'ಭಾಗಮಂಡಲ ಮನೆ — ನಿರ್ಮಾಣ ಯೋಜನೆ v4',
              'ಭಾಗಮಂಡಲ-ತಲಕಾವೇರಿ ರಸ್ತೆ, ಕೊಡಗು | ಏಪ್ರಿಲ್ 2026',
              lang='kn')

    # 3. Malayalam PDF
    print('[3/4] Malayalam Construction Plan')
    ml_md = os.path.join(BASE, 'Bhagamandala_Veedu_Malayalam_v4.md')
    ml_pdf = os.path.join(BASE, 'Bhagamandala_Veedu_Malayalam_v4.pdf')
    md_to_pdf(ml_md, ml_pdf,
              'ഭാഗമണ്ഡല വീട് — നിർമ്മാണ പദ്ധതി v4',
              'ഭാഗമണ്ഡല-തലക്കാവേരി റോഡ്, കൊടഗ് | ഏപ്രിൽ 2026',
              lang='ml')

    # 4. Private Cost PDF
    print('[4/4] Private Cost Estimate')
    cost_md = os.path.join(BASE, 'Bhagamandala_Cost_Estimate_PRIVATE_v4.md')
    cost_pdf = os.path.join(BASE, 'Bhagamandala_Cost_PRIVATE_v4.pdf')
    md_to_pdf(cost_md, cost_pdf,
              'COST ESTIMATE v4 (PRIVATE)',
              'DO NOT SHARE | April 2026',
              lang='en')

    # 5. Images-only PDF (standalone, for sharing images via WhatsApp)
    print('[5/4] Architectural Plans (Images Only)')
    img_pdf = HousePlanPDF(
        'BHAGAMANDALA HOUSE - ARCHITECTURAL PLANS (v4)',
        'All dimensions in feet | v4 Optimized Layout',
        lang='en'
    )
    img_pdf.alias_nb_pages()
    add_images_page(img_pdf, BASE)
    img_pdf_path = os.path.join(BASE, 'Bhagamandala_Plans_Images_v4.pdf')
    img_pdf.output(img_pdf_path)
    size_kb = os.path.getsize(img_pdf_path) / 1024
    print(f'  Saved: Bhagamandala_Plans_Images.pdf ({size_kb:.0f} KB)')

    print(f'\n{"="*50}')
    print('ALL PDFs GENERATED!')
    print(f'{"="*50}')
    print(f'\nFiles ready for WhatsApp sharing:')
    print(f'  📄 Bhagamandala_House_Plan_EN.pdf      (English - shareable)')
    print(f'  📄 Bhagamandala_Mane_Kannada.pdf        (Kannada - shareable)')
    print(f'  📄 Bhagamandala_Veedu_Malayalam.pdf      (Malayalam - shareable)')
    print(f'  📄 Bhagamandala_Plans_Images.pdf         (Images only - shareable)')
    print(f'  🔒 Bhagamandala_Cost_PRIVATE.pdf         (PRIVATE - do NOT share)')
    print(f'\nAll in: {BASE}')


if __name__ == '__main__':
    generate_all_pdfs()
