#!/usr/bin/env python3
"""W85 Projektplan — PDF Generator"""

import os
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase.pdfmetrics import stringWidth

# ─── LAYOUT ─────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN  = 2.5 * cm
AVAIL   = PAGE_W - 2 * MARGIN   # ≈ 452 pt

# ─── COLOURS ────────────────────────────────────────────────────────────────
COVER_BG    = HexColor('#5c2010')
COVER_BOX   = HexColor('#4a1808')
COVER_ACCENT= HexColor('#f5cfc0')
NAVY        = HexColor('#1a3a5c')
BLUE        = HexColor('#2d6a9f')
BLUE_L      = HexColor('#d6e4f0')
BLUE_M      = HexColor('#4a8ab5')
GREEN       = HexColor('#1a7a40')
GREEN_L     = HexColor('#d5f5e3')
ORANGE      = HexColor('#c0560a')
ORANGE_L    = HexColor('#fdebd0')
RED         = HexColor('#b03020')
RED_L       = HexColor('#fadbd8')
YELLOW      = HexColor('#8a6010')
YELLOW_L    = HexColor('#fef9e7')
TEAL        = HexColor('#0e7060')
TEAL_L      = HexColor('#d1f2eb')
PURPLE      = HexColor('#5b2c8e')
GRAY_L      = HexColor('#f4f6f8')
GRAY_M      = HexColor('#cdd3d9')
GRAY_D      = HexColor('#5d6d7e')
TEXT        = HexColor('#1c2833')
WHITE       = white

# ─── STYLES ─────────────────────────────────────────────────────────────────
def S(name, **kw):
    kw.setdefault('fontName', 'Helvetica')
    kw.setdefault('fontSize', 9)
    kw.setdefault('leading', 13)
    kw.setdefault('textColor', TEXT)
    return ParagraphStyle(name, **kw)

ST = {
    'title':  S('ti', fontName='Helvetica-Bold', fontSize=24, leading=30, textColor=NAVY),
    'sub':    S('su', fontSize=10, leading=15, textColor=GRAY_D, spaceAfter=2),
    'meta':   S('me', fontSize=8.5, leading=12, textColor=GRAY_D),
    'h2':     S('h2', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=NAVY,
                spaceBefore=8, spaceAfter=5),
    'h3':     S('h3', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=BLUE,
                spaceBefore=6, spaceAfter=3),
    'body':   S('bo', fontSize=9, leading=13.5, alignment=TA_JUSTIFY, spaceAfter=4),
    'body_l': S('bl', fontSize=9, leading=13.5),
    'small':  S('sm', fontSize=7.5, leading=11, textColor=GRAY_D),
    'cell':   S('ce', fontSize=8.5, leading=12),
    'cell_c': S('cc', fontSize=8.5, leading=12, alignment=TA_CENTER),
    'cell_b': S('cb', fontName='Helvetica-Bold', fontSize=8.5, leading=12),
    'cell_bc':S('cbc',fontName='Helvetica-Bold', fontSize=8.5, leading=12, alignment=TA_CENTER),
    'cell_r': S('cr', fontSize=8.5, leading=12, textColor=GRAY_D),
    'th':     S('th', fontName='Helvetica-Bold', fontSize=8.5, leading=12,
                textColor=WHITE, alignment=TA_CENTER),
    'th_l':   S('tl', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=WHITE),
    'foot':   S('fo', fontSize=7.5, leading=10, textColor=GRAY_D, alignment=TA_CENTER),
}

# ─── TABLE STYLE HELPER ──────────────────────────────────────────────────────
def tbl(n_rows, hdr=NAVY, stripe=GRAY_L, col_aligns=None):
    ts = [
        ('BACKGROUND',    (0, 0), (-1, 0), hdr),
        ('TEXTCOLOR',     (0, 0), (-1, 0), WHITE),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0), 8.5),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 1), (-1, -1), 8.5),
        ('ALIGN',         (0, 0), (-1,  0), 'CENTER'),
        ('ALIGN',         (0, 1), (-1, -1), 'LEFT'),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID',          (0, 0), (-1, -1), 0.4, GRAY_M),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]
    for i in range(1, n_rows):
        bg = stripe if i % 2 == 0 else WHITE
        ts.append(('BACKGROUND', (0, i), (-1, i), bg))
    if col_aligns:
        for col, align in col_aligns.items():
            ts.append(('ALIGN', (col, 1), (col, -1), align))
    return TableStyle(ts)

# ─── CUSTOM FLOWABLES ────────────────────────────────────────────────────────

class SectionHeader(Flowable):
    def __init__(self, number, title, color=NAVY, w=AVAIL, h=30):
        super().__init__()
        self.number = number
        self.title  = title
        self.color  = color
        self._w     = w
        self._h     = h

    def wrap(self, *args):
        return self._w, self._h + 10

    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.roundRect(0, 6, self._w, self._h, 4, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1, alpha=0.18)
        c.circle(19, 6 + self._h / 2, 11, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 11)
        c.drawCentredString(19, 6 + self._h / 2 - 4, str(self.number))
        c.setFont('Helvetica-Bold', 13)
        c.drawString(38, 6 + self._h / 2 - 5, self.title)


class InfoBox(Flowable):
    def __init__(self, title, lines, color=BLUE, bg=None, w=AVAIL):
        super().__init__()
        self.title    = title
        self.lines    = lines
        self.color    = color
        self.bg       = bg or HexColor('#eaf3fb')
        self._w       = w
        self._h       = None
        self._display = None

    def _rewrap(self, inner_w):
        result = []
        for raw in self.lines:
            words = raw.split()
            cur   = ''
            for word in words:
                test = (cur + ' ' + word).strip() if cur else word
                if stringWidth(test, 'Helvetica', 8.5) <= inner_w:
                    cur = test
                else:
                    if cur:
                        result.append(cur)
                    cur = word
            if cur:
                result.append(cur)
        return result or ['']

    def wrap(self, availW, availH):
        inner_w       = self._w - 24
        self._display = self._rewrap(inner_w)
        title_h       = 16 if self.title else 0
        body_h        = len(self._display) * 13
        self._h       = max(36, 10 + title_h + body_h + 8)
        return self._w, self._h

    def draw(self):
        c = self.canv
        h = self._h or 48
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self._w, h, 3, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.roundRect(0, 0, 4, h, 2, fill=1, stroke=0)
        y = h - 14
        if self.title:
            c.setFillColor(self.color)
            c.setFont('Helvetica-Bold', 9)
            c.drawString(11, y, self.title)
            y -= 16
        c.setFillColor(TEXT)
        c.setFont('Helvetica', 8.5)
        for line in (self._display or []):
            if y > 4:
                c.drawString(11, y, line)
                y -= 13


class CoverBlock(Flowable):
    def __init__(self, w=AVAIL):
        super().__init__()
        self._w = w
        self._h = 100

    def wrap(self, *args):
        return self._w, self._h

    def draw(self):
        c = self.canv
        c.setFillColor(COVER_BG)
        c.roundRect(0, 0, self._w, self._h, 6, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 20)
        c.drawString(16, self._h - 30, 'Sanierung W85 — Projektplan')
        c.setFont('Helvetica', 10)
        c.setFillColor(COVER_ACCENT)
        c.drawString(16, self._h - 46, 'Weilburger Str. 85, 61250 Usingen')
        metrics = [
            ('Vermietungsstart', '01.07.2026'),
            ('Gesamtbudget',     '180.000 EUR'),
            ('KV beauftragt',    '181.134 EUR'),
            ('Stand',            '29.04.2026'),
        ]
        box_w = (self._w - 32) / len(metrics)
        for i, (label, value) in enumerate(metrics):
            bx = 16 + i * box_w
            by = 8
            c.setFillColor(COVER_BOX)
            c.roundRect(bx, by, box_w - 6, 30, 3, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont('Helvetica-Bold', 10)
            c.drawCentredString(bx + (box_w - 6) / 2, by + 17, value)
            c.setFillColor(COVER_ACCENT)
            c.setFont('Helvetica', 7)
            c.drawCentredString(bx + (box_w - 6) / 2, by + 5, label)


class GanttChart(Flowable):
    T0    = date(2026, 4,  1)
    T1    = date(2026, 7,  1)
    TODAY = date(2026, 4, 29)
    DAYS  = 91

    TASKS = [
        ('Innenausbau (Unsinnbau)',       date(2026,4, 1), date(2026,6,15), BLUE,   date(2026,4,29)),
        ('Sanit\xe4r & Heizung (Nagell)', date(2026,4, 1), date(2026,6,20), NAVY,   date(2026,4,29)),
        ('Dach / Jung (BAFA bewilligt)',  date(2026,5,15), date(2026,6,30), ORANGE, None),
        ('Elektro (Ott)',                 date(2026,4, 1), date(2026,6,25), GREEN,  date(2026,4,29)),
        ('Fenster & Haust\xfcr (ML)',     date(2026,4,15), date(2026,5,15), PURPLE, date(2026,4,29)),
        ('Eigenleistung',                 date(2026,5, 1), date(2026,6,15), YELLOW, None),
        ('Au\xdfenbereich (KVs offen)',   date(2026,5,15), date(2026,6,30), TEAL,   None),
        ('\xdcbergabe',                   date(2026,6,25), date(2026,7, 1), RED,    None),
    ]

    MILESTONES = [
        ('IKEA Lieferung',   date(2026,6, 8), NAVY),
        ('Vermietungsstart', date(2026,7, 1), RED),
    ]

    MONTHS = [
        (date(2026,4,1), date(2026,5,1), 'April'),
        (date(2026,5,1), date(2026,6,1), 'Mai'),
        (date(2026,6,1), date(2026,7,1), 'Juni / Juli'),
    ]

    def __init__(self, w=AVAIL):
        super().__init__()
        self._w      = w
        self.label_w = 152
        self.chart_w = w - self.label_w
        self.row_h   = 19
        self.hdr_h   = 20
        self.ms_h    = 22
        self._h      = self.hdr_h + len(self.TASKS) * self.row_h + self.ms_h + 4

    def _x(self, d):
        days = max(0, min(self.DAYS, (d - self.T0).days))
        return self.label_w + (days / self.DAYS) * self.chart_w

    def wrap(self, *args):
        return self._w, self._h

    def draw(self):
        c   = self.canv
        lw  = self.label_w
        rh  = self.row_h
        hh  = self.hdr_h
        ms  = self.ms_h
        n   = len(self.TASKS)
        chart_body_h = n * rh
        chart_body_y = ms

        band_colors = [HexColor('#f0f4f8'), HexColor('#e8edf2')]
        for i, (m_start, m_end, _) in enumerate(self.MONTHS):
            x1 = self._x(m_start)
            x2 = self._x(m_end)
            c.setFillColor(band_colors[i % 2])
            c.rect(x1, chart_body_y, x2 - x1, chart_body_h, fill=1, stroke=0)

        hdr_y = ms + chart_body_h
        c.setFillColor(NAVY)
        c.rect(lw, hdr_y, self._w - lw, hh, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 7)
        c.drawString(3, hdr_y + hh / 2 - 4, 'Gewerk')
        for m_start, m_end, m_name in self.MONTHS:
            x1 = self._x(m_start)
            x2 = self._x(m_end)
            c.drawCentredString((x1 + x2) / 2, hdr_y + hh / 2 - 4, m_name)

        c.setStrokeColor(GRAY_M)
        c.setLineWidth(0.4)
        for m_start, _, _ in self.MONTHS:
            mx = self._x(m_start)
            c.line(mx, chart_body_y, mx, hdr_y)

        tx = self._x(self.TODAY)
        c.setStrokeColor(RED)
        c.setLineWidth(1.2)
        c.setDash([3, 3])
        c.line(tx, chart_body_y, tx, hdr_y)
        c.setDash()
        c.setFillColor(RED)
        c.setFont('Helvetica-Bold', 6.5)
        c.drawCentredString(tx, chart_body_y - 8, 'Heute')

        for i, (label, t_start, t_end, color, done_until) in enumerate(self.TASKS):
            row_y = ms + (n - 1 - i) * rh
            bg = HexColor('#f8fafc') if i % 2 == 0 else WHITE
            c.setFillColor(bg)
            c.rect(0, row_y, lw - 2, rh, fill=1, stroke=0)
            c.setFillColor(TEXT)
            c.setFont('Helvetica', 7.5)
            c.drawString(3, row_y + rh / 2 - 4, label)

            x1 = self._x(t_start)
            x2 = self._x(t_end)
            bw = max(3, x2 - x1)
            bh = rh - 6
            by = row_y + 3

            if done_until:
                dx2    = min(self._x(done_until), x2)
                done_w = max(0, dx2 - x1)
                if done_w > 0:
                    c.setFillColor(GRAY_D)
                    c.roundRect(x1, by, done_w, bh, 2, fill=1, stroke=0)
                remain_w = bw - done_w
                if remain_w > 1:
                    c.setFillColor(color)
                    c.roundRect(x1 + done_w, by, remain_w, bh, 2, fill=1, stroke=0)
            else:
                c.setFillColor(color)
                c.roundRect(x1, by, bw, bh, 2, fill=1, stroke=0)

            if 'BAFA' in label:
                badge_x = x1 - 14
                c.setFillColor(GREEN)
                c.roundRect(badge_x, by, 12, bh, 2, fill=1, stroke=0)
                c.setFillColor(WHITE)
                c.setFont('Helvetica-Bold', 7)
                c.drawCentredString(badge_x + 6, by + bh / 2 - 3, 'ok')

            c.setStrokeColor(GRAY_M)
            c.setLineWidth(0.3)
            c.line(0, row_y, self._w, row_y)

        c.setFillColor(GRAY_L)
        c.rect(0, 0, self._w, ms, fill=1, stroke=0)
        c.setFillColor(GRAY_D)
        c.setFont('Helvetica-Bold', 7)
        c.drawString(3, ms / 2 - 4, 'Meilensteine')
        for m_label, m_date, m_color in self.MILESTONES:
            mx = self._x(m_date)
            c.setFillColor(m_color)
            sz = 5
            path = c.beginPath()
            path.moveTo(mx,      ms / 2 + sz)
            path.lineTo(mx + sz, ms / 2)
            path.lineTo(mx,      ms / 2 - sz)
            path.lineTo(mx - sz, ms / 2)
            path.close()
            c.drawPath(path, fill=1, stroke=0)
            c.setFont('Helvetica-Bold', 6.5)
            c.drawCentredString(mx, 2, m_label)

        c.setStrokeColor(GRAY_M)
        c.setLineWidth(0.6)
        c.rect(0, 0, self._w, self._h, fill=0, stroke=1)


class BudgetAmpel(Flowable):
    def __init__(self, current, w=AVAIL):
        super().__init__()
        self.current = current
        self._w = w
        self._h = 70

    def wrap(self, *args):
        return self._w, self._h

    def draw(self):
        c      = self.canv
        levels = [
            (183000, GREEN,  'GR\xdcN',  'bis 183.000 EUR',      'Im Rahmen'),
            (190000, YELLOW, 'GELB',     '183.001–190.000', 'Beobachten'),
            (999999, RED,    'ROT',      '\xfcber 190.000 EUR',   'Sofort priorisieren'),
        ]
        bw = (self._w - 20) / 3
        for i, (threshold, color, label, range_str, action) in enumerate(levels):
            bx     = 10 + i * bw
            active = (i == 0 and self.current <= 183000) or \
                     (i == 1 and 183000 < self.current <= 190000) or \
                     (i == 2 and self.current > 190000)
            c.setStrokeColor(color if active else GRAY_M)
            c.setFillColor(color if active else GRAY_L)
            c.setLineWidth(2.5 if active else 0.4)
            c.roundRect(bx, 4, bw - 8, self._h - 8, 4, fill=1, stroke=1)
            tc = WHITE if active else GRAY_D
            c.setFillColor(tc)
            c.setFont('Helvetica-Bold', 10)
            c.drawCentredString(bx + (bw - 8) / 2, self._h - 24, label)
            c.setFont('Helvetica', 7)
            c.drawCentredString(bx + (bw - 8) / 2, self._h - 36, range_str)
            c.setFont('Helvetica', 6.5)
            c.drawCentredString(bx + (bw - 8) / 2, self._h - 48, action)
            if active:
                c.setFillColor(WHITE)
                c.setFont('Helvetica-Bold', 7)
                val = f'Aktuell: {int(self.current):,} EUR'.replace(',', '.')
                c.drawCentredString(bx + (bw - 8) / 2, 10, val)


# ─── PAGE FOOTER ─────────────────────────────────────────────────────────────

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(GRAY_D)
    canvas.drawString(MARGIN, 1.2 * cm,
                      'Sanierung W85 — Projektplan | Stand 29.04.2026 | Vertraulich')
    canvas.drawRightString(PAGE_W - MARGIN, 1.2 * cm, f'Seite {doc.page}')
    canvas.restoreState()

# ─── CONTENT HELPERS ─────────────────────────────────────────────────────────

def P(text, style='body'):
    return Paragraph(text, ST[style])

def sp(n=6):
    return Spacer(1, n)

def hr(color=GRAY_M, thickness=0.5):
    return HRFlowable(width=AVAIL, thickness=thickness, color=color,
                      spaceAfter=5, spaceBefore=5)

# ─── SECTION 0: COVER ────────────────────────────────────────────────────────

def build_cover():
    return [CoverBlock(AVAIL), sp(10), hr(COVER_BG, 1.5)]

# ─── SECTION 1: FEHLENDE KVs ─────────────────────────────────────────────────

def build_section1():
    elems = []
    elems.append(SectionHeader(1, 'Fehlende Kostenvoranschl\xe4ge', NAVY))
    elems.append(sp(5))
    elems.append(P(
        'F\xfcnf Gewerke sind geplant, aber noch ohne Kostenvoranschlag. '
        'Diese Positionen sind im aktuellen Budget von 180.000 EUR nicht enthalten. '
        'Alle Gewerke sollen vor Vermietungsbeginn am 01.07.2026 abgeschlossen sein.',
        'body'
    ))
    elems.append(sp(5))

    cols   = [22, 82, 120, 62, 166]
    header = [P('#','th'), P('Gewerk','th'), P('Beschreibung','th'),
              P('Priorit\xe4t','th'), P('N\xe4chster Schritt','th')]
    rows_data = [
        ('1', 'Terrassenbelag',    'Erneuerung Terrassenbelag',                           'Hoch',   'KV anfordern – ggf. Unsinnbau'),
        ('2', 'Podest Haust\xfcr', 'Erneuerung Podest Hauseingangsbereich',               'Hoch',   'KV anfordern – ggf. Unsinnbau'),
        ('3', 'Garagentor',        'Erneuerung Garagentor',                               'Mittel', 'KV anfordern – Fachbetrieb Tore'),
        ('4', 'Zaun Altk\xf6nigstr.','Doppelstabmatte 8m + T\xfcr 1m, 180cm, anthrazit', 'Mittel', 'KV anfordern – Zaunbauer'),
        ('5', 'Verkleidung',       'Eingang + Gartenschuppen – Rauspund',            'Mittel', 'KV anfordern – ggf. Unsinnbau'),
    ]
    prio_col = {'Hoch': RED_L, 'Mittel': YELLOW_L}
    prio_txt = {'Hoch': RED,   'Mittel': YELLOW}
    data = [header]
    for nr, gw, desc, prio, step in rows_data:
        data.append([P(nr,'cell_c'), P(f'<b>{gw}</b>','cell'),
                     P(desc,'cell'), P(prio,'cell_c'), P(step,'cell')])
    t = Table(data, colWidths=cols, repeatRows=1)
    ts = tbl(len(data))
    for i, (_, _, _, prio, _) in enumerate(rows_data):
        ts.add('BACKGROUND', (3,i+1), (3,i+1), prio_col[prio])
        ts.add('TEXTCOLOR',  (3,i+1), (3,i+1), prio_txt[prio])
        ts.add('FONTNAME',   (3,i+1), (3,i+1), 'Helvetica-Bold')
    t.setStyle(ts)
    elems.append(t)
    elems.append(sp(8))

    card_w  = AVAIL / 2 - 5
    details = [
        ('1 \xb7 Terrassenbelag', BLUE,
         ['Terrassenbelag erneuern.',
          'Handwerker: offen – Unsinnbau anfragen.']),
        ('2 \xb7 Podest Haust\xfcr', BLUE,
         ['Eingangsbereich / Podest vor Haust\xfcr erneuern.',
          'Handwerker: offen – Unsinnbau anfragen.']),
        ('3 \xb7 Garagentor', BLUE,
         ['Bestehendes Garagentor ersetzen.',
          'Handwerker: offen – Fachbetrieb Tore / Antriebe.']),
        ('4 \xb7 Zaun Altk\xf6nigstra\xdfe', BLUE,
         ['Doppelstabmatte 8 m + T\xfcr 1 m,',
          '180 cm H\xf6he, anthrazit.',
          'Handwerker: offen – Zaunbauer / Metallbau.']),
        ('5 \xb7 Verkleidung Eingang + Schuppen', BLUE,
         ['Rauspund-Verkleidung Eingangsbereich',
          'und Gartenschuppen.',
          'Handwerker: offen – Unsinnbau oder Zimmermann.']),
    ]

    all_cards = [P('Details pro Gewerk', 'h2')]
    for i in range(0, len(details), 2):
        pair = details[i:i+2]
        row  = []
        for title, color, lines in pair:
            row.append(InfoBox(title, lines, color=color, w=card_w))
        if len(row) == 1:
            row.append(Spacer(1, 1))
        t2 = Table([row], colWidths=[card_w, card_w])
        t2.setStyle(TableStyle([
            ('VALIGN',        (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('BOX',           (0,0), (-1,-1), 0, WHITE),
            ('INNERGRID',     (0,0), (-1,-1), 0, WHITE),
        ]))
        all_cards.append(t2)

    all_cards.append(sp(4))
    all_cards.append(InfoBox(
        'Hinweis',
        ['Terrassenbelag und Podest Haust\xfcr haben h\xf6chste Priorit\xe4t vor Vermietungsbeginn.',
         'Alle \xfcbrigen Gewerke (Garagentor, Zaun, Verkleidung) ebenfalls bis 01.07.2026 einplanen.'],
        color=ORANGE, bg=ORANGE_L
    ))
    elems.append(KeepTogether(all_cards))
    return elems

# ─── SECTION 2: ZEITPLAN ─────────────────────────────────────────────────────

def build_section2():
    elems = []
    elems.append(PageBreak())
    elems.append(SectionHeader(2, 'Zeitplan bis Vermietungsstart', BLUE))
    elems.append(sp(6))

    elems.append(P('Meilensteine', 'h2'))
    cols = [82, 230, 140]
    ms_header = [P('Datum','th'), P('Meilenstein','th'), P('Status','th')]
    ms_data = [
        ('29.04.2026', 'Budget-Dashboard + Projektplan erstellt',             'Erledigt',   GREEN_L),
        ('29.04.2026', 'NASPA KfW-Anfrage gesendet',                          'Erledigt',   GREEN_L),
        ('29.04.2026', 'Budget-Check-Anfrage an Unsinnbau',                   'Erledigt',   GREEN_L),
        ('Laufend',    'Elektro Ott – Kabel verlegt',                    'Teilweise',  TEAL_L),
        ('Ab Mitte Mai','Dachdecker Jung – Baubeginn Dach',              'In Planung', BLUE_L),
        ('Mai / Juni', 'KVs fehlende Gewerke einholen + beauftragen',         'Offen',      YELLOW_L),
        ('Mai / Juni', 'Eigenleistung: Studio, Dachboden, Bodenplatten',      'Offen',      YELLOW_L),
        ('08.06.2026', 'IKEA K\xfcche – Lieferung',                      'Best\xe4tigt', TEAL_L),
        ('Juni 2026',  'Elektro Ott – Anschl\xfcsse + Sicherungskasten', 'Offen',      YELLOW_L),
        ('Juni 2026',  'Abschluss aller Gewerke',                             'Ziel',       RED_L),
        ('25.–30.06.2026', '\xdcbergabe-Begehung + Schl\xfcssel\xfcbergabe', 'Ziel',  RED_L),
        ('01.07.2026', 'Vermietungsstart',                                    'Zieldatum',  RED_L),
    ]
    ms_table_data = [ms_header]
    for datum, text, status, _ in ms_data:
        ms_table_data.append([P(datum,'cell_c'), P(text,'cell'), P(status,'cell_c')])
    t = Table(ms_table_data, colWidths=cols, repeatRows=1)
    ts = tbl(len(ms_table_data))
    for i, (_, _, _, bg) in enumerate(ms_data):
        ts.add('BACKGROUND', (2, i+1), (2, i+1), bg)
    last = len(ms_table_data) - 1
    ts.add('BACKGROUND', (0, last), (-1, last), RED_L)
    ts.add('FONTNAME',   (0, last), (-1, last), 'Helvetica-Bold')
    t.setStyle(ts)
    elems.append(KeepTogether([t]))
    elems.append(sp(12))

    elems.append(P('Sanierungsfahrplan', 'h2'))
    elems.append(sp(4))
    elems.append(GanttChart(AVAIL))
    elems.append(sp(4))
    elems.append(P(
        'Grau: bereits erledigte Anteile.  |  Gestrichelte Linie: Stand 29.04.2026.  |  '
        'Gr\xfcnes Badge „ok“: BAFA bewilligt.  |  Rauten: Meilensteine.',
        'small'
    ))

    elems.append(PageBreak())
    elems.append(P('Kritischer Pfad & Risiken', 'h2'))
    kp_cols = [115, 165, 172]
    kp_data = [
        [P('Schritt','th_l'), P('Abh\xe4ngigkeit','th_l'), P('Risiko','th_l')],
        [P('Dach (Jung) ab Mitte Mai','cell_b'),
         P('BAFA bewilligt (Bescheid liegt vor)','cell'),
         P('Verz\xf6gerung durch Wetter oder Material – gr\xf6\xdftes Einzelrisiko','cell')],
        [P('Elektro Abschluss (Ott)','cell_b'),
         P('Alle anderen Gewerke m\xfcssen stromfrei sein','cell'),
         P('Letzte Ma\xdfnahme vor \xdcbergabe – fr\xfchzeitig koordinieren','cell')],
        [P('Fehlende KVs<br/>(5 Gewerke)','cell_b'),
         P('KVs m\xfcssen zeitnah eingeholt werden','cell'),
         P('Je sp\xe4ter beauftragt, desto enger der Zeitplan','cell')],
        [P('\xdcbergabe 25.–30.06.','cell_b'),
         P('Alle Gewerke abgeschlossen','cell'),
         P('Puffer nur 1–2 Wochen bis Vermietungsstart','cell')],
    ]
    kt = Table(kp_data, colWidths=kp_cols, repeatRows=1)
    kt.setStyle(tbl(len(kp_data), hdr=HexColor('#2c4f6e')))
    elems.append(kt)
    elems.append(sp(12))

    elems.append(P('Eigenleistung', 'h2'))
    el_cols = [180, 148, 124]
    el_data = [
        [P('Arbeit','th'), P('Zeitraum','th'), P('Abh\xe4ngigkeit','th')],
        [P('Studio: Bodenfliesen entfernen','cell'),
         P('Mai 2026','cell_c'),
         P('Vor Neuverlegung Bodenbelag','cell')],
        [P('Dachboden d\xe4mmen','cell'),
         P('Mai / Juni 2026','cell_c'),
         P('Unabh\xe4ngig durchf\xfchrbar','cell')],
        [P('Restliche Bodenplatten verlegen','cell'),
         P('Mai / Juni 2026','cell_c'),
         P('Nach Fliesenentfernung Studio','cell')],
    ]
    et = Table(el_data, colWidths=el_cols, repeatRows=1)
    et.setStyle(tbl(len(el_data), hdr=BLUE))
    elems.append(et)
    return elems

# ─── SECTION 3: BUDGET-CONTROLLING ───────────────────────────────────────────

def build_section3():
    elems = []
    elems.append(PageBreak())
    elems.append(SectionHeader(3, 'Budget-Controlling', HexColor('#1e5c30')))
    elems.append(sp(6))

    elems.append(InfoBox(
        'Grundsatz',
        ['Alle Nachtr\xe4ge und Zusatzleistungen werden sofort im Budget-Dashboard erfasst.',
         'Schwellenwert f\xfcr sofortige Eskalation: einzelner Nachtrag > 2.000 EUR.'],
        color=GREEN, bg=GREEN_L
    ))
    elems.append(sp(10))

    elems.append(P('Nachtrag-Prozess', 'h2'))
    proc_rows = [
        [P('<b>1. Meldung</b>  —  Handwerker meldet Mehrkosten m\xfcndlich oder schriftlich', 'cell')],
        [P('<b>2. Pr\xfcfung</b>  —  Ist der Nachtrag technisch notwendig? Wenn nein: ablehnen', 'cell')],
        [P('<b>3. Best\xe4tigung</b>  —  Schriftliche Best\xe4tigung anfordern (WhatsApp gen\xfcgt)', 'cell')],
        [P('<b>4. Erfassung</b>  —  Betrag sofort in budget-dashboard.md eintragen', 'cell')],
        [P('<b>5. Eskalation</b>  —  Nachtrag > 2.000 EUR: Gesamtbudget neu rechnen', 'cell')],
    ]
    step_colors = [BLUE_L, GRAY_L, BLUE_L, GRAY_L, YELLOW_L]
    proc_ts = TableStyle([
        ('FONTNAME',      (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE',      (0,0), (-1,-1), 8.5),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('GRID',          (0,0), (-1,-1), 0.4, GRAY_M),
    ])
    for i, col in enumerate(step_colors):
        proc_ts.add('BACKGROUND', (0,i), (-1,i), col)
    pt = Table(proc_rows, colWidths=[AVAIL])
    pt.setStyle(proc_ts)
    elems.append(pt)
    elems.append(sp(12))

    elems.append(P('Laufende Kontrolle', 'h2'))
    ctrl_data = [
        [P('Wann','th'), P('Aktion','th')],
        [P('Bei jeder Rechnung','cell_b'),
         P('Betrag sofort in budget-dashboard.md eintragen (Spalte Gezahlt)','cell')],
        [P('W\xf6chentlich (Mo)','cell_b'),
         P('Restbudget pr\xfcfen – Gesamtkosten bekannt unter 185.000 EUR?','cell')],
        [P('Nachtrag > 2.000 EUR','cell_b'),
         P('Sofort Gesamtplanung neu rechnen, ggf. Gewerke priorisieren','cell')],
        [P('Nach Abschluss Gewerk','cell_b'),
         P('Endabrechnung mit KV vergleichen und Differenz dokumentieren','cell')],
    ]
    ct = Table(ctrl_data, colWidths=[130, 322], repeatRows=1)
    ct.setStyle(tbl(len(ctrl_data), hdr=HexColor('#1e5c30')))
    elems.append(ct)
    elems.append(sp(12))

    elems.append(P('Budget-Ampel', 'h2'))
    elems.append(BudgetAmpel(181134, AVAIL))
    elems.append(sp(4))
    elems.append(P(
        'Aktueller Stand: 181.134 EUR (KV beauftragt + bekannte Nachtr\xe4ge). '
        'Budget 180.000 EUR. Leichte \xdcberschreitung unkritisch. '
        'F\xfcnf Gewerke ohne KV noch nicht enthalten.',
        'small'
    ))

    elems.append(PageBreak())
    elems.append(P('Erwartete Nachtragsrechnungen', 'h2'))
    nr_cols = [40, 155, 205, 52]
    nr_data = [
        [P('#','th'), P('Gewerk','th'), P('Beschreibung','th'), P('Betrag','th')],
        [P('1','cell_c'), P('Unsinnbau','cell_b'),
         P('Estrich Bad OG (gebrochen, nicht im KV)','cell'),
         P('~ 800 EUR','cell_c')],
        [P('2','cell_c'), P('Ralf M\xfcller OHG','cell_b'),
         P('Fu\xdfbodenheizung Bad OG (im Zuge Estrich verlegt)','cell'),
         P('~ 1.200 EUR','cell_c')],
        [P('3','cell_c'), P('Unsinnbau','cell_b'),
         P('K\xfcchenmontage IKEA (separate Rechnung)','cell'),
         P('~ 1.000 EUR','cell_c')],
        [P('4–8','cell_c'), P('Verschiedene','cell_b'),
         P('5 Gewerke ohne KV (Terrassenbelag, Podest, Garagentor, Zaun, Verkleidung)','cell'),
         P('offen','cell_c')],
        [P('','cell'), P('<b>Gesamt erwartet (ohne offene KVs)</b>','cell'),
         P('','cell'), P('<b>~ 3.000 EUR</b>','cell_c')],
    ]
    nt = Table(nr_data, colWidths=nr_cols, repeatRows=1)
    nts = tbl(len(nr_data), hdr=HexColor('#1e5c30'))
    nts.add('BACKGROUND', (0, len(nr_data)-1), (-1, len(nr_data)-1), GREEN_L)
    nts.add('FONTNAME',   (0, len(nr_data)-1), (-1, len(nr_data)-1), 'Helvetica-Bold')
    nt.setStyle(nts)
    elems.append(nt)
    elems.append(sp(16))
    elems.append(hr(GRAY_M))
    elems.append(P(
        'Entwurf — Stand 29.04.2026 — Weilburger Str. 85, 61250 Usingen — Vertraulich',
        'foot'
    ))
    return elems

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    out = os.path.join(os.path.dirname(__file__), 'projektplan-w85.pdf')
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN,  bottomMargin=2.0 * cm,
        title='Sanierung W85 — Projektplan',
        author='Christian Brand',
        subject='Projektplan Sanierung Weilburger Str. 85',
    )
    story = (build_cover() + build_section1() +
             build_section2() + build_section3())
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f'PDF erstellt: {out}')

if __name__ == '__main__':
    main()
