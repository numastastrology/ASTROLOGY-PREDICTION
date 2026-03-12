from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

# --- Color Palette ---
DARK_BG = HexColor("#121212")   # Very Dark Grey/Black
ACCENT_PURPLE = HexColor("#7B61FF") # Bright Purple
ACCENT_GOLD = HexColor("#FFD700")   # Gold
TEXT_WHITE = HexColor("#FFFFFF")
TEXT_GREY = HexColor("#B0B0B0")
TEXT_GOLD = HexColor("#FFD700")
CONTAINER_BG = HexColor("#1E1E2E") # Slightly lighter dark for boxes

def draw_background(canvas, doc):
    """Draws the dark background and decorative borders on every page"""
    canvas.saveState()
    
    # 1. Fill Background
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, 0, A4[0], A4[1], fill=True, stroke=False)
    
    # 2. Draw Outer Border (Purple)
    canvas.setStrokeColor(ACCENT_PURPLE)
    canvas.setLineWidth(2)
    margin = 20
    canvas.roundRect(margin, margin, A4[0]-2*margin, A4[1]-2*margin, 10, fill=False, stroke=True)
    
    # 3. Footer/Watermark
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(TEXT_GREY)
    canvas.drawCentredString(A4[0]/2, 30, "Premium Astrology Report • Stricktly Confidential")
    
    canvas.restoreState()

def generate_prediction_report(prediction_data, filename="premium_report.pdf"):
    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=50
    )
    
    # Create a Frame for content
    frame = Frame(
        doc.leftMargin, 
        doc.bottomMargin, 
        doc.width, 
        doc.height, 
        id='normal'
    )
    
    # Add Page Template
    template = PageTemplate(id='dark_theme', frames=frame, onPage=draw_background)
    doc.addPageTemplates([template])
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom Styles for Dark Theme
    styles.add(ParagraphStyle(
        name='PremiumMainTitle', 
        parent=styles['Title'], 
        fontSize=28, 
        textColor=ACCENT_PURPLE,
        alignment=1, # Center
        spaceAfter=10
    ))
    
    styles.add(ParagraphStyle(
        name='PremiumSubTitle', 
        parent=styles['Heading2'], 
        fontSize=18, 
        textColor=ACCENT_GOLD,
        alignment=1,
        spaceAfter=20
    ))
    
    styles.add(ParagraphStyle(
        name='PremiumSectionHeader', 
        parent=styles['Heading2'], 
        fontSize=16, 
        textColor=ACCENT_GOLD,
        spaceBefore=15, 
        spaceAfter=10,
        borderWidth=0,
    ))
    
    styles.add(ParagraphStyle(
        name='PremiumBodyText', 
        parent=styles['Normal'], 
        fontSize=11, 
        textColor=TEXT_WHITE,
        leading=16
    ))
    
    styles.add(ParagraphStyle(
        name='PremiumPointText', 
        parent=styles['Normal'], 
        fontSize=11, 
        textColor=TEXT_WHITE,
        leading=14,
        leftIndent=15
    ))

    styles.add(ParagraphStyle(
        name='PremiumRemedyTitle', 
        parent=styles['Heading3'], 
        fontSize=14, 
        textColor=ACCENT_GOLD,
        spaceBefore=10,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        name='PremiumRemedyText', 
        parent=styles['Normal'], 
        fontSize=11, 
        textColor=TEXT_WHITE,
        leading=14,
        leftIndent=20
    ))

    elements = []

    # --- Header Box (Simulating the Purple Box) ---
    # We can use a Table with a single cell to create a bordered box
    
    chart_summary = prediction_data.get('chart_summary', {})
    user_name = chart_summary.get('name', 'Native').upper()
    
    header_content = [
        [Paragraph(f"ASTROLOGY PREDICTION REPORT", styles['PremiumMainTitle'])],
        [Paragraph(f"Prepared for: {clean_text(user_name)}", styles['PremiumSubTitle'])],
        [Paragraph("Prepared by: RAJAGOPAL KANNAN", ParagraphStyle('RightSmall', parent=styles['Normal'], alignment=2, textColor=ACCENT_GOLD, fontSize=10))]
    ]
    
    header_table = Table(header_content, colWidths=[doc.width])
    header_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 2, ACCENT_PURPLE),
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),
        ('TOPPADDING', (0,0), (-1,-1), 15),
        ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ('BACKGROUND', (0,0), (-1,-1), CONTAINER_BG) # Lighter dark background for header
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 30))

    # --- Helper: Draw South Indian Chart ---
    def draw_south_indian_chart(c, x, y, size, title, positions, ascendant_sign=None):
        """Draws a South Indian Chart at (x,y) with given size."""
        c.saveState()
        c.setStrokeColor(ACCENT_GOLD)
        c.setLineWidth(1.5)
        c.setFillColor(CONTAINER_BG)
        
        # Outer Box
        c.rect(x, y, size, size, fill=True, stroke=True)
        
        # Inner Lines (Grid)
        step = size / 4
        # Horizontal lines
        c.line(x, y + step, x + size, y + step)
        c.line(x, y + 2*step, x + size, y + 2*step)
        c.line(x, y + 3*step, x + size, y + 3*step)
        # Vertical lines
        c.line(x + step, y, x + step, y + size)
        c.line(x + 2*step, y, x + 2*step, y + size)
        c.line(x + 3*step, y, x + 3*step, y + size)
        
        # Clear Center (South Indian chart has open center usually, or crossed)
        # We will leave it as grid for now, typically center 4 boxes are merged or ignored.
        # Actually in South Indian chart, the center is not used for signs.
        # Signs map:
        # Pisces, Aries, Taurus, Gemini (Top Row, L->R? No, Clockwise)
        # South Indian Config:
        # Pisces | Aries | Taurus | Gemini
        # Aquarius |      |      | Cancer
        # Capricorn|      |      | Leo
        # Sagitt |orpio | Libra  | Virgo
        
        # We need to map Sign Name -> Grid Coordinate (row, col)
        # (0,0) is bottom-left.
        # Pisces: (0, 3) (Top Left)
        # Aries: (1, 3)
        # Taurus: (2, 3)
        # Gemini: (3, 3)
        # Cancer: (3, 2)
        # Leo: (3, 1)
        # Virgo: (3, 0)
        # Libra: (2, 0)
        # Scorpio: (1, 0)
        # Sagittarius: (0, 0)
        # Capricorn: (0, 1)
        # Aquarius: (0, 2)
        
        sign_map = {
            "Pisces": (0, 3), "Aries": (1, 3), "Taurus": (2, 3), "Gemini": (3, 3),
            "Cancer": (3, 2), "Leo": (3, 1), "Virgo": (3, 0), "Libra": (2, 0),
            "Scorpio": (1, 0), "Sagittarius": (0, 0), "Capricorn": (0, 1), "Aquarius": (0, 2)
        }
        
        # Center white box for Title
        c.setFillColor(DARK_BG)
        c.rect(x + step, y + step, 2*step, 2*step, fill=True, stroke=True)
        c.setFillColor(TEXT_GOLD)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + size/2, y + size/2, title)
        
        # Place Planets
        c.setFont("Helvetica", 8)
        c.setFillColor(TEXT_WHITE)
        
        # Group planets by sign
        sign_contents = {k: [] for k in sign_map.keys()}
        
        if ascendant_sign and ascendant_sign != "Unknown":
            # Strip degrees if present: "Sign (Deg Min)" -> "Sign"
            clean_asc_sign = ascendant_sign.split('(')[0].strip()
            if clean_asc_sign in sign_contents:
                sign_contents[clean_asc_sign].append("Asc")
            
        for planet, pos_str in positions.items():
            # Extract sign name from "Sign (Deg Min)"
            p_sign = pos_str.split('(')[0].strip()
            if p_sign in sign_contents:
                abbr = planet[:2]
                if planet == "Mandhi": abbr = "Md"
                
                # Check for status suffixes (R), (C), (D)
                status = ""
                if "(R)" in pos_str: status += "R"
                if "(C)" in pos_str: status += "C"
                if "(D)" in pos_str: status += "D"
                
                display_name = f"{abbr}{status}" if status else abbr
                sign_contents[p_sign].append(display_name)
                
        # Draw text in cells
        for sign, planets in sign_contents.items():
            col, row = sign_map[sign]
            # Cell coordinates
            cx = x + col * step
            cy = y + row * step
            
            # Constrain text to cell
            text_y = cy + step - 10
            for i, p_abbr in enumerate(planets):
                c.drawString(cx + 5, text_y - (i*10), p_abbr)
        
        c.restoreState()

    # Define a custom Flowable for the Chart to put in ReportLab story
    from reportlab.platypus import Flowable
    class SouthIndianChart(Flowable):
        def __init__(self, title, positions, ascendant):
            Flowable.__init__(self)
            self.title = title
            self.positions = positions
            self.ascendant = ascendant
            self.width = 200
            self.height = 200
            
        def draw(self):
            draw_south_indian_chart(self.canv, 0, 0, 200, self.title, self.positions, self.ascendant)

    # --- Profile Box ---
    elements.append(Paragraph("Horoscope Profile", styles['PremiumSectionHeader']))
    
    profile_data = [
        [Paragraph("Name:", styles['PremiumBodyText']), Paragraph(clean_text(user_name), styles['PremiumBodyText'])],
        [Paragraph("DOB:", styles['PremiumBodyText']), Paragraph(clean_text(str(chart_summary.get('date_of_birth', ''))), styles['PremiumBodyText'])],
        [Paragraph("Time:", styles['PremiumBodyText']), Paragraph(clean_text(str(chart_summary.get('time_of_birth', ''))), styles['PremiumBodyText'])],
        [Paragraph("Place:", styles['PremiumBodyText']), Paragraph(clean_text(str(chart_summary.get('place_of_birth', ''))), styles['PremiumBodyText'])],
        [Paragraph("Star:", styles['PremiumBodyText']), Paragraph(clean_text(f"{chart_summary.get('nakshatra', '')} - Pada {chart_summary.get('pada', '')}"), styles['PremiumBodyText'])],
    ]
    
    profile_table = Table(profile_data, colWidths=[1.5*inch, 4*inch])
    profile_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, ACCENT_PURPLE),
        ('BACKGROUND', (0,0), (-1,-1), CONTAINER_BG),
        ('TEXTCOLOR', (0,0), (-1,-1), TEXT_WHITE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(profile_table)
    elements.append(Spacer(1, 20))

    # --- Charts Section (D1 & D9) ---
    elements.append(Paragraph("Divisional Charts", styles['PremiumSectionHeader']))
    
    # Create Table for Side-by-Side Charts
    # Create Table for Side-by-Side Charts
    d1_data = chart_summary.get('planetary_positions', {})
    d9_data = chart_summary.get('navamsa_positions', {})
    asc_sign = chart_summary.get('ascendant', 'Unknown')
    d9_asc_sign = chart_summary.get('navamsa_ascendant', 'Unknown')
    
    chart_row = [
        SouthIndianChart("Rasi (D1)", d1_data, asc_sign),
        SouthIndianChart("Navamsa (D9)", d9_data, d9_asc_sign) 
    ]
    
    chart_table = Table([chart_row], colWidths=[220, 220])
    chart_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(chart_table)
    elements.append(Spacer(1, 20))

    # --- Jamakkol Section ---
    jk_data = chart_summary.get('jamakkol', {})
    if jk_data:
        elements.append(Paragraph("Jamakkol Prasannam", styles['PremiumSectionHeader']))
        # 3 cols: Udayam, Arudham, Kavippu
        jk_udayam = jk_data.get('Udayam', '-')
        jk_arudham = jk_data.get('Arudham', '-')
        jk_kavippu = jk_data.get('Kavippu', '-')
        
        jk_row = [
            [Paragraph("Udayam", styles['PremiumPointText']), Paragraph(jk_udayam, styles['PremiumBodyText'])],
            [Paragraph("Arudham", styles['PremiumPointText']), Paragraph(jk_arudham, styles['PremiumBodyText'])],
            [Paragraph("Kavippu", styles['PremiumPointText']), Paragraph(jk_kavippu, styles['PremiumBodyText'])]
        ]
        
        # Make a horizontal table
        jk_table_data = [
            [Paragraph("Udayam", styles['PremiumPointText']), Paragraph("Arudham", styles['PremiumPointText']), Paragraph("Kavippu", styles['PremiumPointText'])],
            [Paragraph(clean_text(jk_udayam), styles['PremiumBodyText']), Paragraph(clean_text(jk_arudham), styles['PremiumBodyText']), Paragraph(clean_text(jk_kavippu), styles['PremiumBodyText'])]
        ]
        
        jk_table = Table(jk_table_data, colWidths=[2*inch, 2*inch, 2*inch])
        jk_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), CONTAINER_BG),
            ('TEXTCOLOR', (0,0), (-1,-1), TEXT_WHITE),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(jk_table)
        elements.append(Spacer(1, 20))

    # --- Transit Positions ---
    # --- Transit Positions ---
    elements.append(Spacer(1, 20)) # Spacer instead of PageBreak
    elements.append(Paragraph("Current Transit Positions (Gochar)", styles['PremiumSectionHeader']))
    transit_data = chart_summary.get('transit_positions', {})
    
    t_rows = []
    t_rows.append([Paragraph("Planet", styles['PremiumBodyText']), Paragraph("Current Position", styles['PremiumBodyText'])])
    
    for planet, position in transit_data.items():
        t_rows.append([Paragraph(clean_text(planet), styles['PremiumPointText']), Paragraph(clean_text(position), styles['PremiumPointText'])])

    t_table = Table(t_rows, colWidths=[2.5*inch, 2.5*inch])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), ACCENT_PURPLE),
        ('TEXTCOLOR', (0,0), (-1,-1), TEXT_WHITE),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_table)
    elements.append(Spacer(1, 30)) # Spacer instead of PageBreak

    # --- Predictions Loop ---
    # Use the order as provided in the predictions dictionary (now handled by backend)
    elements.append(PageBreak()) # Force start on new page for Predictions
    predictions = prediction_data.get('predictions', {})
    ordered_categories = list(predictions.keys())
    
    for i, category in enumerate(ordered_categories):
        content = predictions[category]
        readable_category = category.replace('_', ' ').upper()
        
        # Get Score
        score = 0
        points = []
        if isinstance(content, dict):
            score = content.get('score', 0)
            points = content.get('points', [])
            remedies = content.get('remedies', [])
        elif isinstance(content, list):
            points = content
            remedies = []
            
        elements.append(Paragraph(clean_text(readable_category), styles['PremiumSectionHeader']))
        
        # Score Display
        if isinstance(content, dict) and 'score' in content:
            score_color = colors.green if score >= 75 else (colors.orange if score >= 50 else colors.red)
            
            # Improved Score Bar Visibility (100% Border, Fill Score, Text Inside)
            bar_total_width = 5 * inch
            bar_fill_width = (score / 100.0) * bar_total_width
            if bar_fill_width < 0: bar_fill_width = 0
            bar_empty_width = bar_total_width - bar_fill_width
            
            # Text Style
            score_text = f"Score: {score}%"
            text_style_white = ParagraphStyle('ScoreTextW', parent=styles['Normal'], textColor=colors.white, fontSize=12, alignment=1) # Center
            text_style_grey = ParagraphStyle('ScoreTextG', parent=styles['Normal'], textColor=HexColor("#D3D3D3"), fontSize=12, alignment=1)
            
            # Determine where to put text
            if score >= 35:
                # Text in Filled part
                row_data = [Paragraph(score_text, text_style_white), ""]
            else:
                # Text in Empty part
                row_data = ["", Paragraph(score_text, text_style_grey)]
            
            bar = Table([row_data], colWidths=[bar_fill_width, bar_empty_width])
            bar.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 1.5, colors.white), # FULL 100% White Border
                ('BACKGROUND', (0,0), (0,0), score_color),  # Fill Score Part
                ('BACKGROUND', (1,0), (1,0), CONTAINER_BG), # Empty Part (Dark)
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            elements.append(bar)
            elements.append(Spacer(1, 25))
        
        # Points List
        for point in points:
            # We must preserve <b> tags if they exist (only escape &, <, > that are NOT tags?)
            # But clean_text escapes < and >.
            # astro_utils uses <b> tags. 
            # We need a smarter clean_text or just trust astro_utils?
            # User reported crash. Likely & in point.
            # Let's try to just escape '&' for now inside clean_text?
            # Or manually replace & here?
            sanitized_point = clean_text(point).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
            elements.append(Paragraph(f"• {sanitized_point}", styles['PremiumPointText']))
            elements.append(Spacer(1, 4))
        # Remedies
        if remedies:
            elements.append(PageBreak()) # FORCE NEW PAGE FOR REMEDIES
            elements.append(Paragraph("Remedies and Recommendations:", styles['PremiumRemedyTitle']))
            
            for r in remedies:
                sanitized_r = clean_text(r).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
                elements.append(Paragraph(f"➜ {sanitized_r}", styles['PremiumRemedyText']))
                
        # Add PageBreak unless it's the last category
        if i < len(ordered_categories) - 1:
            elements.append(PageBreak())


    # --- Disclaimer (Try to fit on same page) ---
    elements.append(Spacer(1, 25))
    elements.append(Paragraph("DISCLAIMER", styles['PremiumSectionHeader']))
    disclaimer_text = """
    This astrology report is based on ancient Vedic principles and is intended for guidance, spiritual growth, and entertainment purposes only. 
    Astrological predictions are subject to interpretation and should not be considered as absolute facts or fatalistic verdicts. 
    The information provided here does not constitute professional legal, medical, financial, or psychological advice. 
    AstroPredictor and its developers are not responsible for any decisions made based on this report.
    Users are advised to use their own discretion, critical thinking, and judgment in all matters of life.
    """
    elements.append(Paragraph(disclaimer_text, styles['PremiumBodyText']))

    doc.build(elements)
    return filename

def clean_text(text):
    """
    Sanitizes text for ReportLab Paragraph (XML).
    Escapes &, <, >.
    """
    if not isinstance(text, str):
        return str(text)
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
