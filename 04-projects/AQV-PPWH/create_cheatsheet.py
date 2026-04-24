from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/Users/christian/Desktop/A12-Cheatsheet.pdf"

W, H = A4

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=1.6*cm,
    leftMargin=1.6*cm,
    topMargin=1.4*cm,
    bottomMargin=1.2*cm,
)

def s(name, **kw):
    defaults = dict(fontName="Helvetica", fontSize=9, leading=12,
                    textColor=colors.HexColor("#222222"), spaceAfter=0, spaceBefore=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

title_s  = s("t",  fontSize=14, fontName="Helvetica-Bold", textColor=colors.HexColor("#1a1a2e"), spaceAfter=2)
sub_s    = s("su", fontSize=8,  textColor=colors.HexColor("#888888"), spaceAfter=6)
qhead_s  = s("qh", fontSize=8.5, fontName="Helvetica-Bold",
              textColor=colors.white, backColor=colors.HexColor("#1a1a2e"),
              leading=11, leftIndent=4)
bullet_s = s("b",  fontSize=8.2, leading=11.5, leftIndent=8,
              textColor=colors.HexColor("#1a1a2e"))
warn_s   = s("w",  fontSize=7.5, leading=10, leftIndent=8,
              textColor=colors.HexColor("#c0392b"), fontName="Helvetica-Oblique")
end_s    = s("e",  fontSize=8.2, leading=11.5, leftIndent=8,
              fontName="Helvetica-Bold", textColor=colors.HexColor("#1a1a2e"))
core_s   = s("c",  fontSize=8, leading=11, leftIndent=0, textColor=colors.HexColor("#444444"))
core_h_s = s("ch", fontSize=8, fontName="Helvetica-Bold", leading=11,
              textColor=colors.HexColor("#1a1a2e"))

def hr():
    return HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#cccccc"),
                      spaceAfter=3, spaceBefore=3)

def q_block(num, frage, bullets, schluss, warnung=None):
    """Returns a list of flowables for one question block."""
    items = []
    items.append(Paragraph(f"F{num} — {frage}", qhead_s))
    items.append(Spacer(1, 2))
    for b in bullets:
        items.append(Paragraph(f"· {b}", bullet_s))
    if warnung:
        items.append(Paragraph(f"⚠ {warnung}", warn_s))
    items.append(Paragraph(f"Schlusssatz: \"{schluss}\"", end_s))
    items.append(Spacer(1, 4))
    return items

story = []

story.append(Paragraph("Nachwuchsführungskraft — Interview-Cheatsheet", title_s))
story.append(Paragraph("Christian Brand · 20. April 2026 · Eignungsinterview für den Zugang zum AQV · Roten Faden pro Frage — kein Auswendiglernen!", sub_s))
story.append(hr())
story.append(Spacer(1, 3))

fragen = [
    ("1", "Bedeutende Aufgabe",
     ["HöMS: SPOC Hessen — Fachlehrer VKÜ-Technik für Polizei + Kommunen",
      "Didaktik, Digitalisierung (e-Learning), Beschaffungsbegleitung",
      "Bundesweit: Bremen, Schleswig-Holstein, Mecklenburg-Vorpommern",
      "Bindeglied LPP13 / operative Fläche"],
     "Das war meine erste echte Führungsverantwortung — auch ohne formalen Führungsauftrag.",
     None),

    ("2", "Dienstliche Veränderung",
     ["Tod beider Eltern → Prioritäten neu gewichten",
      "Bewusste Entscheidung gegen Karriere, für Stabilität + kurze Wege",
      "Pflichthalbjahr WSD trotzdem vollständig absolviert — mit Überzeugung",
      "Heimatkenntnis = Vorsprung, kein Nachteil",
      "Dieses Interview jetzt: aus stabiler Basis heraus — das ist der Unterschied zu damals."],
     "Wer weiß, wo er am besten wirkt, kann dort am meisten leisten. Das habe ich gelernt.",
     None),

    ("3", "Eigene Aufgabe vermasselt",
     ["Wechsel zu RVD: komplexer Vorgang übernommen (FoF, Alkohol, Drogen)",
      "ComVor + eAS jahrelang nicht genutzt → Fehler, Verzögerungen",
      "Zu lange alleine gearbeitet, Hilfe zu spät geholt"],
     "Mein Lerneffekt: früher melden, früher Hilfe holen — das ist keine Schwäche, das ist Vernunft.",
     None),

    ("4", "Alleine mit einer Meinung",
     ["SPOC: Kommunen legen VKÜ-Erlass zu ihren Gunsten aus",
      "Ich hatte Rückendeckung LPP — trotzdem kein leichtes Gespräch",
      "Sachlich geblieben, auf Rechtsreferat verwiesen (nicht ausgewichen!)"],
     "Meine Einschätzung war richtig — und ich habe sie nicht verwässert.",
     "Keine Namen nennen!"),

    ("5", "Innerdienstlicher Konflikt",
     ["K72-Bewerbung → Chef: 'Leistungsträger, aber bei Rückkehr bitte Umsetzung'",
      "Gespräch gesucht → Chef bestätigt Position → akzeptiert",
      "K72: Ausbildung bestanden, Kommando → nach 2 Monaten zurück",
      "Burnout — Chef wird in dieser Phase zum größten Unterstützer"],
     "Brücken nicht abbrechen — auch wenn man sich ungerecht behandelt fühlt. Das war meine wichtigste Lektion.",
     "Kürzer halten! Direktionsleiter-Detail weglassen."),

    ("6", "Stress & längere Belastungsphasen",
     ["Kindheit: Elterntrennung → früh Vermittlerrolle übernommen",
      "Erwachsen: Familie, Immobilien, kranke Eltern, Bruder — Dauerlauf",
      "2018: Burnout, 9 Monate Dienstunfähigkeit, stationär",
      "Seit 2015 Therapie → Frühwarnzeichen kennen (Schlaf, Reizbarkeit, Freudlosigkeit)",
      "Nach Muttertod 2024: aktive Entscheidung RVD statt Weitermachen wie bisher"],
     "Ich weiß jetzt, wo meine Grenze ist. Noch ein Burnout braucht kein Mensch — das ist Erfahrung, keine Schwäche.",
     None),

    ("7", "Persönliche Entscheidung mit Auswirkung auf andere",
     ["Bruder wohnte in meiner ETW — Jahre Alkohol, Drogen, Polizeieinsätze",
      "Langfristiger Plan (Wohnung an ihn): nicht mehr haltbar",
      "Klare Ansage: Auszug. Alle Chancen zuvor gegeben und nicht genutzt",
      "Tut weh — war trotzdem richtig"],
     "Eine Entscheidung, die anderen schadet, kann trotzdem die einzig richtige sein — wenn man die Alternativen wirklich ausgeschöpft hat.",
     None),

    ("8", "OE gut und schlecht",
     ["Erst 3 Monate → keine tiefe Beurteilung, aber ehrliche Wahrnehmung",
      "Gut: Klima, Transparenz, Führung erreichbar, Teamzusammenhalt",
      "Schlecht: Personalknappheit — aber systemisch, nicht OE-spezifisch!"],
     "Ressourcen kann ich nicht erschaffen — aber ich kann transparent machen, was leistbar ist und was nicht. Das ist Führungsaufgabe.",
     None),

    ("9", "Warum Führungskraft?",
     ["Nicht wegen des Titels — hätte auch einen einfacheren Weg gehabt",
      "C-Jugend: Meisterschaft, aber vor allem: das Klima",
      "36 Tickets für U19-Spiel — freiwillig, alle dabei",
      "Klima entsteht nicht durch Anweisung, sondern durch Haltung"],
     "Dieses Klima — wo Leistung entsteht, weil Menschen wollen und nicht müssen — das will ich auch beruflich schaffen.",
     None),

    ("10", "Aufgabe für jemand anderen",
     ["Mutter schwer lungenkrank — Carina und ich Hauptbezugspersonen bis zum Tod",
      "Keine Pflicht, immer wieder neu entschieden",
      "Kein reines Opfer: Zeit mit ihr, Momente die nicht wiederholbar sind",
      "Sie war nicht allein. Sie kam nicht ins Heim."],
     "Die Menschen in meiner Verantwortung sollen spüren: es ist nicht egal.",
     None),
]

for num, frage, bullets, schluss, warnung in fragen:
    for item in q_block(num, frage, bullets, schluss, warnung):
        story.append(item)

story.append(hr())
story.append(Spacer(1, 2))
story.append(Paragraph("Kernbotschaften — immer verfügbar:", core_h_s))
story.append(Spacer(1, 2))

kern = [
    "Selbstkenntnis statt Selbstdarstellung",
    "Entscheidungen reifen lassen — dann klar handeln",
    "Führung = Klima schaffen, nicht kontrollieren",
    "Transparenz als Haltung (nach oben, unten, sich selbst)",
    "Brücken nicht abbrechen",
]
for k in kern:
    story.append(Paragraph(f"· {k}", core_s))

story.append(Spacer(1, 4))
story.append(Paragraph("Viel Erfolg heute!", s("fin", fontSize=9, fontName="Helvetica-Bold",
    textColor=colors.HexColor("#c0392b"), alignment=TA_CENTER)))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#cccccc"), spaceAfter=4))
story.append(Paragraph(
    "Christian Brand · Polizeihauptkommissar A11 · RVD Hochtaunus",
    s("sig", fontSize=7.5, textColor=colors.HexColor("#aaaaaa"), alignment=TA_CENTER)))

doc.build(story)
print(f"PDF erstellt: {OUTPUT}")
