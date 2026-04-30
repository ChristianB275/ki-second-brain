#!/usr/bin/env python3
"""PDF-Generierung für Fionas Visum-Dokumente"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Farbpalette ─────────────────────────────────────────────────────────────
BLUE      = colors.HexColor("#1a4f82")
LIGHTBLUE = colors.HexColor("#dce8f5")
GREEN     = colors.HexColor("#2d7a2d")
LIGHTGRAY = colors.HexColor("#f5f5f5")
DARKGRAY  = colors.HexColor("#333333")
RED       = colors.HexColor("#c0392b")
ORANGE    = colors.HexColor("#e67e22")

# ─── Styles ──────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def make_styles():
    return {
        "h1": ParagraphStyle("h1", fontSize=20, leading=26, textColor=BLUE,
                              spaceAfter=4, fontName="Helvetica-Bold"),
        "h2": ParagraphStyle("h2", fontSize=13, leading=17, textColor=BLUE,
                              spaceBefore=14, spaceAfter=4, fontName="Helvetica-Bold"),
        "h3": ParagraphStyle("h3", fontSize=11, leading=14, textColor=DARKGRAY,
                              spaceBefore=8, spaceAfter=3, fontName="Helvetica-Bold"),
        "body": ParagraphStyle("body", fontSize=10, leading=14, textColor=DARKGRAY,
                                fontName="Helvetica"),
        "small": ParagraphStyle("small", fontSize=8.5, leading=12, textColor=colors.gray,
                                  fontName="Helvetica"),
        "check": ParagraphStyle("check", fontSize=10, leading=16, textColor=DARKGRAY,
                                  leftIndent=14, fontName="Helvetica"),
        "check_done": ParagraphStyle("check_done", fontSize=10, leading=16,
                                      textColor=GREEN, leftIndent=14, fontName="Helvetica"),
        "note": ParagraphStyle("note", fontSize=9.5, leading=13, textColor=DARKGRAY,
                                 leftIndent=12, fontName="Helvetica-Oblique"),
        "sub": ParagraphStyle("sub", fontSize=9, leading=12, textColor=colors.gray,
                                leftIndent=8, fontName="Helvetica"),
        "center": ParagraphStyle("center", fontSize=10, leading=14, alignment=TA_CENTER,
                                   textColor=DARKGRAY, fontName="Helvetica"),
        "title_sub": ParagraphStyle("title_sub", fontSize=11, leading=15, textColor=BLUE,
                                     fontName="Helvetica"),
        "important": ParagraphStyle("important", fontSize=10, leading=14,
                                     textColor=RED, fontName="Helvetica-Bold"),
    }

S = make_styles()

def hr(color=BLUE, thickness=1):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=4, spaceBefore=4)

def section_header(text):
    return [
        Spacer(1, 0.2*cm),
        Table([[Paragraph(text, ParagraphStyle("sh", fontSize=12, leading=15,
                textColor=colors.white, fontName="Helvetica-Bold"))]],
              colWidths=["100%"],
              style=TableStyle([
                  ("BACKGROUND", (0,0), (-1,-1), BLUE),
                  ("TOPPADDING", (0,0), (-1,-1), 5),
                  ("BOTTOMPADDING", (0,0), (-1,-1), 5),
                  ("LEFTPADDING", (0,0), (-1,-1), 10),
              ])),
        Spacer(1, 0.15*cm),
    ]

def check_item(text, done=False):
    box = "☑" if done else "☐"
    style = S["check_done"] if done else S["check"]
    return Paragraph(f"{box}  {text}", style)

def sub_item(text):
    return Paragraph(f"      ↳  {text}", S["sub"])

def info_table(data, col_widths=None):
    if col_widths is None:
        col_widths = [5.5*cm, 11.5*cm]
    rows = [[Paragraph(k, ParagraphStyle("tk", fontSize=9.5, fontName="Helvetica-Bold",
                        textColor=BLUE)),
             Paragraph(v, ParagraphStyle("tv", fontSize=9.5, fontName="Helvetica",
                        textColor=DARKGRAY))]
            for k, v in data]
    t = Table(rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHTGRAY),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHTGRAY]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


# ═══════════════════════════════════════════════════════════════════════════════
#  PDF 1: VISUM-CHECKLISTE
# ═══════════════════════════════════════════════════════════════════════════════

def build_checklist():
    path = os.path.join(BASE_DIR, "visum-checkliste.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4,
                             leftMargin=2*cm, rightMargin=2*cm,
                             topMargin=2*cm, bottomMargin=2*cm)
    story = []

    # Titelblock
    story.append(Paragraph("J-1 Visum Fiona Brand", S["h1"]))
    story.append(Paragraph("Checkliste Visumsantrag — zum Ausdrucken", S["title_sub"]))
    story.append(hr())
    story.append(Spacer(1, 0.2*cm))

    story.append(info_table([
        ("Programm", "NorthWest Student Exchange (NWSE)"),
        ("Programm-Nr.", "P-3-05374"),
        ("SEVIS-ID", "N0037493477"),
        ("Laufzeit", "20.08.2026 – 20.06.2027"),
        ("Visumsart", "J-1 Exchange Visitor / Secondary School Student"),
    ]))
    story.append(Spacer(1, 0.4*cm))

    # ── Bereits erledigt ──────────────────────────────────────────────────────
    story += section_header("✅  Bereits erledigt")
    story.append(check_item("DS-2019 erhalten — ausgestellt 19.02.2026 (Dennis Broll, NWSE)", done=True))
    story.append(check_item("I-901 SEVIS-Gebühr bezahlt — $220 am 29.04.2026 | Bestätigung: BBB2621171160", done=True))

    # ── Schritt 1 ─────────────────────────────────────────────────────────────
    story += section_header("Schritt 1 — DS-2019 unterschreiben")
    story.append(Paragraph(
        "⚠  Fiona ist bei Programmbeginn (20.08.2026) noch 15 Jahre alt → "
        "Elternteil muss unterschreiben.", S["important"]))
    story.append(Spacer(1, 0.2*cm))
    story.append(check_item('Seite 1 unten: "Exchange Visitor Certification" → Elternteil unterschreibt für Fiona'))
    story.append(check_item('Ort (z.B. "Bad Homburg, Germany") + Datum eintragen'))
    story.append(check_item("Nur Original verwenden — keine Kopie"))

    # ── Schritt 2 ─────────────────────────────────────────────────────────────
    story += section_header("Schritt 2 — Passfoto vorbereiten")
    story.append(check_item("Digitales Passfoto: biometrisch, weißer Hintergrund, US-Vorgaben"))
    story.append(check_item("Ggf. gedrucktes Foto (Konsulat Frankfurt-Website prüfen)"))

    # ── Schritt 3 ─────────────────────────────────────────────────────────────
    story += section_header("Schritt 3 — DS-160 Online-Antrag (ceac.state.gov/genniv)")
    story.append(check_item("DS-160 vollständig ausgefüllt"))
    story.append(check_item("Application ID gesichert (nach jeder Seite speichern!)"))
    story.append(check_item("Passfoto hochgeladen"))
    story.append(check_item("Bestätigungsseite ausgedruckt"))
    story.append(Spacer(1, 0.15*cm))

    story.append(Paragraph("Wichtige Eingaben:", S["h3"]))
    story.append(info_table([
        ("Reisezweck", "Exchange Visitor (J) → Student (J1)"),
        ("Ankunftsdatum", "ca. 28.–30.07.2026 (oder gebuchtes Flugdatum)"),
        ("Aufenthaltsdauer", "10 MONTHS"),
        ("US-Adresse", "101 Derby Court, Azle, TX 76020 (Familie Schluter)"),
        ("Zahler der Reise", "SELF (= Eltern)"),
        ("Reisegefährten", "Nein"),
        ("SEVIS ID", "N0037493477"),
        ("Programmnummer", "P-3-05374"),
        ("Kurs", "Academic"),
        ("Sicherheitsfragen", "alle NEIN"),
    ]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("US-Kontaktperson (Dennis Broll / NWSE):", S["h3"]))
    story.append(info_table([
        ("Name", "Dennis Broll"),
        ("Organisation", "NORTHWEST STUDENT EXCHANGE"),
        ("Adresse", "3302 FUHRMAN AVE, SUITE 300, SEATTLE, WA 98102"),
        ("Telefon", "2065270917"),
        ("E-Mail", "nwse@nwse.com"),
    ]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("2 Kontaktpersonen in Deutschland (keine Familienmitglieder):", S["h3"]))
    story.append(info_table([
        ("Person 1", "_______________________________________"),
        ("Person 2", "_______________________________________"),
    ]))

    # ── Schritt 4 ─────────────────────────────────────────────────────────────
    story += section_header("Schritt 4 — Termin beim US-Konsulat Frankfurt buchen (ustraveldocs.com)")
    story.append(check_item("Account bei ustraveldocs.com angelegt"))
    story.append(sub_item("Nonimmigrant Visa → Students and Exchange Visitors (F,M,J) → J-1 Exchange Visitor"))
    story.append(check_item("Visumsgebühr bezahlt (ca. $185, nicht erstattbar)"))
    story.append(check_item("Zahlungsquittung ausgedruckt"))
    story.append(check_item("Interviewtermin gebucht"))
    story.append(check_item("Terminbestätigung ausgedruckt"))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph(
        "Wartezeiten prüfen: travel.state.gov → Wait Times — so früh wie möglich buchen!", S["note"]))

    # ── Schritt 5 ─────────────────────────────────────────────────────────────
    story += section_header("Schritt 5 — Unterlagen für das Interview")
    story.append(Paragraph("Pflichtdokumente (Original):", S["h3"]))
    story.append(check_item("DS-2019 — Original, von Elternteil unterschrieben"))
    story.append(check_item("DS-160 Bestätigungsseite — Ausdruck"))
    story.append(check_item("I-901 Zahlungsbestätigung — Ausdruck (BBB2621171160)"))
    story.append(check_item("Gültiger Reisepass — muss bis mind. 20.12.2027 gültig sein"))
    story.append(check_item("Terminbestätigung Konsulat — Ausdruck"))
    story.append(check_item("Visumsgebühr-Quittung — Ausdruck"))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph("Empfohlene zusätzliche Unterlagen:", S["h3"]))
    story.append(check_item("Kontoauszug Eltern (deutlich mehr als $2.500 verfügbar)"))
    story.append(check_item("Unterschriebenes Elternschreiben: Kostenübernahme bestätigen"))
    story.append(check_item("Brief: Fionas Motivation + warum sie nach Deutschland zurückkehrt"))
    story.append(check_item("Ggf. Englisch-Testergebnis (ELTiS o.ä.) falls vorhanden"))

    # ── Schritt 6 ─────────────────────────────────────────────────────────────
    story += section_header("Schritt 6 — Interview beim Konsulat Frankfurt")
    story.append(check_item("Alle Dokumente vollständig vorbereitet und sortiert"))
    story.append(check_item("Keine Handys, keine großen Taschen (laut Konsulatsregeln)"))
    story.append(check_item("Fiona auf Englisch vorbereitet: Rückkehr nach Deutschland klar kommunizieren"))
    story.append(check_item("Pass erhalten (Konsulat schickt ihn mit Visum per Post zurück)"))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph(
        "Bei Ablehnung: sofort NWSE kontaktieren — Dennis Broll, (206) 527-0917", S["important"]))

    # ── Schritt 7 ─────────────────────────────────────────────────────────────
    story += section_header("Schritt 7 — Einreise USA (nach Erhalt des Visums)")
    story.append(check_item("Flug gebucht (Ankunft DFW, frühestens 22.07.2026)"))
    story.append(check_item("Im Handgepäck: Reisepass + DS-2019 + I-901 Quittung"))
    story.append(check_item('Einreisestempel geprüft → muss "J-1" + "D/S" zeigen'))
    story.append(check_item("Nach Ankunft: NWSE kontaktiert (SEVIS-Bestätigung)"))

    # ── Notfall ───────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.3*cm))
    story.append(hr(color=RED, thickness=1.5))
    story.append(info_table([
        ("NWSE 24h Notfall", "(206) 683-3100"),
        ("J-1 Notfall-Hotline USA", "1-866-283-9090 (24/7)"),
        ("NWSE Büro", "(206) 527-0917 | nwse@nwse.com"),
    ]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("Erstellt: 29.04.2026", S["small"]))

    doc.build(story)
    print(f"✅ PDF erstellt: {path}")


# ═══════════════════════════════════════════════════════════════════════════════
#  PDF 2: FIONA-INFO
# ═══════════════════════════════════════════════════════════════════════════════

def build_fiona_info():
    path = os.path.join(BASE_DIR, "fiona-info-usa.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4,
                             leftMargin=2*cm, rightMargin=2*cm,
                             topMargin=2*cm, bottomMargin=2*cm)
    story = []

    # Titel
    story.append(Paragraph("Dein Auslandsjahr in den USA", S["h1"]))
    story.append(Paragraph("Das Wichtigste für Fiona Brand | Azle, Texas | 2026/2027", S["title_sub"]))
    story.append(hr())
    story.append(Spacer(1, 0.2*cm))

    # ── Dein Programm ─────────────────────────────────────────────────────────
    story += section_header("Dein Programm")
    story.append(Paragraph(
        "Du gehst mit <b>NorthWest Student Exchange (NWSE)</b> für ein ganzes Schuljahr "
        "in die USA. Dein Visum ist ein <b>J-1 Exchange Visitor Visa</b> — das ist kein "
        "normales Touristenvisum, sondern ein spezielles Austauschvisum.",
        S["body"]))
    story.append(Spacer(1, 0.15*cm))
    story.append(info_table([
        ("Programmdauer", "20. August 2026 – 20. Juni 2027"),
        ("Programm", "NorthWest Student Exchange (NWSE)"),
        ("Visumsart", "J-1 Exchange Visitor"),
    ]))

    # ── Gastfamilie ───────────────────────────────────────────────────────────
    story += section_header("Deine Gastfamilie — Familie Schluter")
    story.append(info_table([
        ("Adresse", "101 Derby Court, Azle, TX 76020"),
        ("Gastmutter", "Farrah Schluter (kommt aus Pennsylvania)"),
        ("Gastvater", "Karl Schluter"),
        ("Telefon", "(830) 534-1654"),
        ("E-Mail", "koenigfarrah@hotmail.com"),
        ("Kinder", "Mason (geht 2026 aufs College), Reese (15), Brooke (14)"),
        ("Haustiere", "2 Hunde, 1 Katze, 6 Hühner + 1 Hahn"),
        ("Dein Zimmer", "Du bekommst Masons Zimmer — du darfst die Farbe aussuchen!"),
    ]))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "Die Familie unternimmt gerne: Camping, Mountainbiking, Pickleball, Wandern, "
        "Frisbee Golf, Reiten, Paddleboarding.", S["body"]))
    story.append(Spacer(1, 0.1*cm))
    story.append(info_table([
        ("Weihnachten", "Pennsylvania (Farrahs Heimat) — Washington D.C. und NYC möglich"),
        ("Spring Break (März 2027)", "Colorado angedacht — oder dein Wunschziel"),
    ]))

    # ── Schule ────────────────────────────────────────────────────────────────
    story += section_header("Deine Schule")
    story.append(info_table([
        ("Schule", "Azle High School"),
        ("Adresse", "1200 Boyd Rd, Azle, TX 76020"),
        ("Klasse", "11th Grade"),
        ("Schulstart", "12. August 2026"),
        ("Schulende", "20. Mai 2027"),
        ("Schulregistrierung", "23. Juli 2026 — Kurswahl vorher an Familie Schluter schicken"),
    ]))

    # ── Sport ─────────────────────────────────────────────────────────────────
    story += section_header("Sport & Aktivitäten")
    story.append(Paragraph(
        "Für jeden Sport brauchst du ein <b>Sports Physical Form</b> — ein Arztzeugnis, "
        "das bestätigt, dass du sportlich fit bist. Der Arzttermin muss <b>nach dem 1. Juni 2026</b> sein.",
        S["body"]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("Volleyball Tryouts", S["h3"]))
    story.append(info_table([
        ("Datum", "31. Juli – 1. August 2026"),
        ("Hinweis", "Du hattest Volleyball angegeben — Familie Schluter hat extra darauf hingewiesen!"),
        ("Empfehlung", "Wenn du mitmachen willst: spätestens am 28. oder 29. Juli ankommen"),
    ]))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph("Cheerleading", S["h3"]))
    story.append(Paragraph("Du hast Interesse angegeben — frag Familie Schluter nach dem genauen Termin.", S["body"]))

    # ── Anreise ───────────────────────────────────────────────────────────────
    story += section_header("Anreise")
    story.append(info_table([
        ("Flughafen", "Dallas Fort Worth International (DFW)"),
        ("Früheste Einreise", "22. Juli 2026 (29 Tage vor Programmbeginn)"),
        ("Empfohlene Ankunft", "ca. 28.–30. Juli 2026 (für Volleyball Tryouts)"),
    ]))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph(
        "Bei Zwischenstopp in den USA: mindestens 3 Stunden Umsteigezeit einplanen "
        "(Immigration + Zoll + Gepäck).", S["note"]))

    # ── Gesundheit ────────────────────────────────────────────────────────────
    story += section_header("Gesundheit — wichtiger Hinweis")
    story.append(Paragraph(
        "⚠ <b>Mountain Cedar Allergie:</b> In Texas sind Dezember bis Februar die schlimmsten "
        "Monate für Pollenallergiker. Du hattest eine Pollenallergie in der Bewerbung angegeben — "
        "Familie Schluter hat dich extra darauf hingewiesen. <b>Pack Antihistaminika ein!</b>",
        ParagraphStyle("warn", fontSize=10, leading=14, textColor=ORANGE,
                        fontName="Helvetica-Bold")))

    # ── J-1 Regeln ────────────────────────────────────────────────────────────
    story += section_header("Dein J-1 Visum — die wichtigsten Regeln")

    story.append(Paragraph("1.  Versicherungspflicht", S["h3"]))
    story.append(Paragraph(
        "Du musst während des gesamten Aufenthalts eine Krankenversicherung haben. "
        "Ohne gültige Versicherung kann dein Programm beendet werden.", S["body"]))
    story.append(info_table([
        ("Mindestdeckung", "$100.000 pro Unfall oder Krankheit"),
        ("Rückführung", "$25.000"),
        ("Med. Evakuierung", "$50.000"),
        ("Selbstbeteiligung", "Maximal $500 pro Fall"),
    ]))

    story.append(Paragraph("2.  SEVIS — das amerikanische Erfassungssystem", S["h3"]))
    story.append(Paragraph(
        "Deine Daten sind in SEVIS gespeichert. Wenn du ankommst, musst du dich bei NWSE "
        "melden, damit deine Daten aktualisiert werden. Stimmen deine Daten nicht, "
        "kannst du nicht in den USA bleiben.", S["body"]))

    story.append(Paragraph("3.  Adressänderungen sofort melden", S["h3"]))
    story.append(Paragraph(
        "Wenn sich deine Adresse, Telefonnummer oder E-Mail ändert: sofort NWSE informieren.",
        S["body"]))

    story.append(Paragraph("4.  Wie lange du bleiben darfst", S["h3"]))
    story.append(Paragraph(
        "Bis zu <b>29 Tage nach deinem letzten Schultag</b> (Grace Period). Danach musst "
        "du die USA verlassen.", S["body"]))

    story.append(Paragraph("5.  Reisen außerhalb der USA während des Schuljahres", S["h3"]))
    story.append(Paragraph(
        "Wenn du die USA verlässt und wieder einreist, brauchst du deine DS-2019 mit "
        "Reisevalidierung (Unterschrift des NWSE-Officers). Frag NWSE rechtzeitig davor.",
        S["body"]))

    # ── Einreise ──────────────────────────────────────────────────────────────
    story += section_header("Was du beim Einreisen brauchst (im Handgepäck!)")
    story.append(Paragraph(
        "Niemals ins aufgegebene Gepäck packen:", S["body"]))
    story.append(Spacer(1, 0.1*cm))
    story.append(info_table([
        ("✈ Reisepass", "mit J-1 Visum"),
        ("✈ DS-2019", "dein Zulassungsformular"),
        ("✈ I-901 Quittung", "SEVIS-Gebühr-Bestätigung"),
    ]))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "Am Einreiseschalter: sage dem Beamten, dass du <b>J-1 Exchange Student</b> bist. "
        "Adresse: Familie Schluter, 101 Derby Court, Azle, TX 76020.", S["body"]))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph(
        'Nach der Einreise: schau sofort auf den Stempel im Pass. Er muss <b>"J-1"</b> '
        'und <b>"D/S"</b> (duration of stay) zeigen. Wenn etwas nicht stimmt: '
        'sofort den Beamten fragen oder NWSE anrufen.', S["body"]))

    # ── Notfallkontakte ───────────────────────────────────────────────────────
    story += section_header("Notfallkontakte")
    story.append(info_table([
        ("NWSE 24h Notfall", "(206) 683-3100"),
        ("Area Coordinator", "Karen Sweet | (440) 241-7385 | karen@nwse.com — sie ist in Keller, TX!"),
        ("NWSE Büro", "(206) 527-0917 | nwse@nwse.com"),
        ("J-1 Notfall-Hotline USA", "1-866-283-9090 (24/7)"),
        ("J-1 Notfall-E-Mail", "JVisas@state.gov"),
    ]))

    # ── Abschluss ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.4*cm))
    story.append(hr(color=BLUE, thickness=2))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Halte einen offenen Kopf. Amerikanische Familien und Schulen funktionieren anders "
        "als in Deutschland — das ist normal und Teil des Abenteuers. "
        "Dein Sponsor NWSE ist immer für dich da, wenn etwas nicht stimmt.",
        S["body"]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Viel Spaß, Fiona! Das wird ein Jahr, das du nie vergisst. 🇺🇸",
        ParagraphStyle("finale", fontSize=13, leading=18, textColor=BLUE,
                        fontName="Helvetica-Bold", alignment=TA_CENTER)))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Erstellt: 29.04.2026", S["small"]))

    doc.build(story)
    print(f"✅ PDF erstellt: {path}")


if __name__ == "__main__":
    build_checklist()
    build_fiona_info()
