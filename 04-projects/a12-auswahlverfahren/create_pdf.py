from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = "/Users/christian/Desktop/A12-Interview-Vorbereitung.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2.5*cm,
    leftMargin=2.5*cm,
    topMargin=2.5*cm,
    bottomMargin=2.5*cm,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle("title", fontSize=18, fontName="Helvetica-Bold",
    spaceAfter=6, textColor=colors.HexColor("#1a1a2e"), alignment=TA_LEFT)
subtitle_style = ParagraphStyle("subtitle", fontSize=11, fontName="Helvetica",
    spaceAfter=16, textColor=colors.HexColor("#555555"), alignment=TA_LEFT)
meta_style = ParagraphStyle("meta", fontSize=9, fontName="Helvetica",
    spaceAfter=4, textColor=colors.HexColor("#888888"))
q_number_style = ParagraphStyle("qnum", fontSize=10, fontName="Helvetica-Bold",
    spaceAfter=2, textColor=colors.HexColor("#ffffff"),
    backColor=colors.HexColor("#1a1a2e"), leftIndent=0)
q_style = ParagraphStyle("q", fontSize=13, fontName="Helvetica-Bold",
    spaceBefore=18, spaceAfter=4, textColor=colors.HexColor("#1a1a2e"))
theme_style = ParagraphStyle("theme", fontSize=9, fontName="Helvetica-Oblique",
    spaceAfter=10, textColor=colors.HexColor("#666666"))
body_style = ParagraphStyle("body", fontSize=10.5, fontName="Helvetica",
    spaceAfter=8, leading=16, alignment=TA_JUSTIFY, textColor=colors.HexColor("#222222"))
quote_style = ParagraphStyle("quote", fontSize=10.5, fontName="Helvetica",
    spaceAfter=6, leading=16, leftIndent=18, rightIndent=10,
    alignment=TA_JUSTIFY, textColor=colors.HexColor("#333333"),
    borderPad=6)
followup_label = ParagraphStyle("followup_label", fontSize=9, fontName="Helvetica-Bold",
    spaceBefore=10, spaceAfter=2, textColor=colors.HexColor("#c0392b"))
followup_style = ParagraphStyle("followup", fontSize=9.5, fontName="Helvetica-Oblique",
    spaceAfter=4, leading=14, leftIndent=14, textColor=colors.HexColor("#555555"))
section_style = ParagraphStyle("section", fontSize=13, fontName="Helvetica-Bold",
    spaceBefore=20, spaceAfter=8, textColor=colors.HexColor("#1a1a2e"))
bullet_style = ParagraphStyle("bullet", fontSize=10.5, fontName="Helvetica",
    spaceAfter=4, leading=15, leftIndent=14, textColor=colors.HexColor("#222222"))

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd"), spaceAfter=4, spaceBefore=4)

story = []

# Title page header
story.append(Paragraph("A12 Auswahlverfahren", title_style))
story.append(Paragraph("Interview-Vorbereitung", ParagraphStyle("t2", fontSize=22, fontName="Helvetica-Bold",
    spaceAfter=10, textColor=colors.HexColor("#c0392b"))))
story.append(hr())
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Christian Brand · Polizeihauptkommissar A11 · April 2026", meta_style))
story.append(Paragraph("Deadline: Montag, 20.04.2026", ParagraphStyle("deadline", fontSize=9,
    fontName="Helvetica-Bold", spaceAfter=4, textColor=colors.HexColor("#c0392b"))))
story.append(Spacer(1, 0.5*cm))

# Format info box
info_text = (
    "<b>Format:</b> 10 Fragen schriftlich ausgehändigt · 15 Min. Vorbereitungszeit mit Notizen · "
    "Notizen bleiben draußen · Strukturierte mündliche Antworten<br/><br/>"
    "<b>Was die Prüfer wollen:</b> Keine Schlagworte, sondern den Denkprozess — wie Entscheidungen reifen, "
    "wie Lösungen erarbeitet werden. Kleinteilig, nachvollziehbar.<br/><br/>"
    "<b>Methode:</b> Für jede Frage eine konkrete Geschichte. "
    "Ausgangslage → Wahrnehmung/Analyse → Abwägung → Entscheidung/Handlung → Ergebnis/Lernen."
)
story.append(Paragraph(info_text, ParagraphStyle("info", fontSize=9.5, fontName="Helvetica",
    spaceAfter=8, leading=14, leftIndent=12, rightIndent=12,
    textColor=colors.HexColor("#333333"),
    backColor=colors.HexColor("#f5f5f5"), borderPad=10)))
story.append(Spacer(1, 0.8*cm))

# Übersicht
story.append(Paragraph("Übersicht", section_style))
overview = [
    ("1", "Bedeutende Aufgabe", "Fachlehrer VKÜ / SPOC Hessen"),
    ("2", "Dienstliche Veränderung", "Wechsel zum RVD — bewusste Entscheidung"),
    ("3", "Eigene Aufgabe vermasselt", "ComVor/eAS nach Wechsel zur neuen Dienststelle"),
    ("4", "Allein mit einer Meinung", "VKÜ-Erlass vs. Kommunen"),
    ("5", "Innerdienstlicher Konflikt", "Verhandlungsgruppe K72 — Burnout — überraschende Unterstützung"),
    ("6", "Stress & Druck", "Dauerlauf seit Kindheit → Therapie → aktive Entscheidung"),
    ("7", "Persönliche Entscheidung", "Bruder aus Eigentumswohnung — Selbstschutz"),
    ("8", "OE gut und schlecht", "RVD positiv — systemische Ressourcenknappheit"),
    ("9", "Warum Führungskraft?", "C-Jugend — 36 Leute beim U19-Spiel"),
    ("10", "Aufgabe für andere", "Pflege der Mutter bis zu ihrem Tod"),
]
for num, q, theme in overview:
    story.append(Paragraph(f"<b>F{num} — {q}</b>", ParagraphStyle("ov_q", fontSize=10,
        fontName="Helvetica-Bold", spaceAfter=1, textColor=colors.HexColor("#1a1a2e"), leftIndent=0)))
    story.append(Paragraph(theme, ParagraphStyle("ov_t", fontSize=9.5, fontName="Helvetica-Oblique",
        spaceAfter=5, textColor=colors.HexColor("#666666"), leftIndent=14)))

story.append(PageBreak())

# Questions
questions = [
    {
        "num": "1",
        "question": "Schildere eine bedeutende Aufgabe.",
        "theme": "Fachlehrer VKÜ-Technik, landesweiter SPOC, Digitalisierung, Beschaffung, Multiplikatoren bundesweit",
        "answer": (
            "Als Fachlehrer für Verkehrssicherheit und Mobilität an der Hessischen Hochschule war ich landesweit der "
            "zentrale Ansprechpartner für Verkehrsüberwachungstechnik — für alle Polizei- und Hilfspolizeibeamten in "
            "Hessen sowie für kommunale Ordnungsbehörden.<br/><br/>"
            "Die Aufgabe war in mehreren Dimensionen bedeutend: Ich war verantwortlich für die Entwicklung "
            "didaktischer Konzepte und die vollständige Digitalisierung der Lehrinhalte — e-Learning, "
            "Broadcastformate, Datenbanken. Gleichzeitig war ich Bindeglied zwischen dem Landespolizeipräsidium "
            "im Innenministerium und der operativen Fläche — also der Ort, wo strategische Vorgaben und "
            "praktische Realität aufeinandertreffen.<br/><br/>"
            "Dazu kam die Akquise und Erprobung neuer Technik sowie die Begleitung landesweiter "
            "Beschaffungsmaßnahmen. Und weil das Thema keine Landesgrenzen kennt, habe ich "
            "Multiplikatorenbeschulungen in Bremen, Schleswig-Holstein und Mecklenburg-Vorpommern durchgeführt "
            "und war in Bundesfachtagungen aktiv.<br/><br/>"
            "Was ich aus dieser Aufgabe mitgenommen habe: Wenn man der einzige Ansprechpartner für ein komplexes "
            "Thema ist, muss man lernen, Prioritäten zu setzen, Wissen zu strukturieren und andere zu befähigen — "
            "nicht alles selbst zu machen. Das war meine erste echte Führungsverantwortung, auch ohne formalen Führungsauftrag."
        ),
        "followup": None,
    },
    {
        "num": "2",
        "question": "Gab es eine dienstliche Veränderung?",
        "theme": "Wechsel zum RVD Hochtaunus — bewusste Entscheidung nach Tod beider Eltern",
        "answer": (
            "Der bedeutendste Wechsel war der zum Regionalen Verkehrsdienst Hochtaunus Anfang 2026 — und er war "
            "eine bewusste Entscheidung gegen Karriere und für Haltung.<br/><br/>"
            "Ich habe zuvor eine Stelle mit landesweitem Impact gehabt, Aufstiegsperspektiven, Sichtbarkeit. "
            "Das aufzugeben war nicht selbstverständlich. Aber nach dem Tod beider Eltern innerhalb eines Jahres "
            "habe ich mich gefragt: Wo kann ich als Mensch und als Polizist am wirkungsvollsten sein?<br/><br/>"
            "Die Antwort war klar: in meiner Region. Ich kenne die Menschen, die Wege, die Strukturen im "
            "Hochtaunus seit Jahrzehnten. Diese Orts- und Personenkenntnis ist im operativen Dienst kein "
            "Nachteil — sie ist ein Vorsprung. Dazu kam der Wunsch, wieder unmittelbar als Polizei "
            "wahrgenommen zu werden — Uniform, Bürgerkontakt, echtes Team.<br/><br/>"
            "Ich weiß auch um meine Grenzen: der 12-Stunden-Wechselschichtdienst mit Nachtdiensten ist für "
            "mich auf Dauer nicht leistbar. Ich habe trotzdem das Pflichthalbjahr in der Dienstgruppe D in "
            "Usingen vollständig absolviert — und es aufrichtig genossen. Dieser Korpsgeist in einer "
            "Dienstgruppe, der gemeinsame Umgang mit dem Unvorhergesehenen — das ist Polizeiarbeit in ihrer "
            "reinsten Form.<br/><br/>"
            "Was mich diese Entscheidung gelehrt hat: Selbstkenntnis ist keine Schwäche. Wer weiß wo er am "
            "besten wirkt, kann dort am meisten leisten."
        ),
        "followup": None,
    },
    {
        "num": "3",
        "question": "Schildere eine Aufgabe, die du vermasselt hast.",
        "theme": "Erster komplexer Vorgang beim RVD — ComVor + eAS nach langer Pause",
        "answer": (
            "Direkt nach meinem Wechsel zum RVD Hochtaunus habe ich einen komplexen Verkehrsunfall aus der "
            "Schicht übernommen — mitten in der Eingewöhnungsphase an einer neuen Dienststelle.<br/><br/>"
            "Das Problem: Ich hatte jahrelang keinen Kontakt mehr mit ComVor, dem Vorgangsbearbeitungssystem, "
            "und dazu kam die Umstellung auf eAS, die elektronische Akte in Strafsachen — ein System, das mir "
            "in dieser Form neu war. Ich habe unterschätzt, wie viel Zeit es braucht, komplexe Sachverhalte "
            "in einem unvertrauten System sauber und vollständig abzuarbeiten. Mein Vorgesetzter war zu Recht "
            "unzufrieden — ich habe den Vorgang deutlich länger beschäftigt als nötig und Fehler gemacht, "
            "die vermeidbar gewesen wären.<br/><br/>"
            "Was ich daraus mitgenommen habe: Ich hätte früher und deutlicher um Unterstützung bitten sollen. "
            "Selbständig arbeiten ist eine Stärke — aber nicht auf Kosten der Qualität und nicht dann, wenn "
            "das Werkzeug neu ist. Seit diesem Erlebnis hole ich mir bei Systemfragen aktiv Hilfe, auch wenn "
            "es mich Überwindung kostet. Sechs Monate reichen nicht, um komplexe Vorgänge souverän "
            "abzuarbeiten — das war eine wichtige Lektion in Demut."
        ),
        "followup": None,
    },
    {
        "num": "4",
        "question": "Warst du schon einmal mit einer Meinung alleine?",
        "theme": "Interpretation des VKÜ-Erlasses — Gegenwind von Kommunen, Rückendeckung LPP13",
        "answer": (
            "Als landesweiter Ansprechpartner für Verkehrsüberwachungstechnik war ich das Bindeglied zwischen "
            "dem Landespolizeipräsidium und den kommunalen Ordnungsbehörden. In dieser Rolle musste ich "
            "mehrfach die Interpretation des Verkehrsüberwachungserlasses vertreten — auch wenn das nicht "
            "alle hören wollten.<br/><br/>"
            "Konkret gab es zwei Punkte im Erlass, die einzelne Kommunen anders auslegten als das LPP13 es "
            "beabsichtigt hatte. Ich hatte die Rückendeckung des Innenministeriums — aber das macht ein "
            "Gespräch nicht einfacher, wenn auf der anderen Seite Verantwortliche sitzen, die ihre Praxis "
            "jahrelang anders gelebt haben.<br/><br/>"
            "Ich bin bei meiner Einschätzung geblieben, habe sie sachlich und klar begründet — und wo nötig "
            "direkt auf das Rechtsreferat verwiesen. Nicht um mich zu entziehen, sondern weil Klarheit über "
            "die Quelle manchmal überzeugender ist als jede persönliche Argumentation. Einige Kommunen haben "
            "das akzeptiert, andere nicht sofort. Aber die Einschätzung war richtig — und ich habe sie nicht "
            "verwässert."
        ),
        "followup": None,
    },
    {
        "num": "5",
        "question": "Schildere einen innerdienstlichen Konflikt.",
        "theme": "Bewerbung Verhandlungsgruppe K72 — Konflikt mit Dienststellenleiter, Burnout, überraschende Unterstützung",
        "answer": (
            "Ende 2017 habe ich mich auf eine Interessensabfrage für die Verhandlungsgruppe K72 beworben — "
            "nicht weil mir meine damalige Dienststelle, der Verkehrsüberwachungsdienst D610 in Frankfurt, "
            "nicht gefallen hätte. Sondern weil ich überzeugt war, meine Stärken dort besonders gut einbringen "
            "zu können. Ich hatte vorher Kontakt zur Einheit aufgenommen, wurde aktiv ermutigt und habe die "
            "Bewerbung auf dem Dienstweg eingereicht.<br/><br/>"
            "Was ich unterschätzt hatte: Mein Dienststellenleiter hatte zu diesem Zeitpunkt bereits mit "
            "mehreren Umsetzungswünschen innerhalb seiner Einheit zu tun. Er sagte mir in einem persönlichen "
            "Gespräch, dass er mich als Leistungsträger schätzt und mir den Erfolg wirklich wünscht. Dann kam "
            "ein Satz, der mich kalt erwischt hat: Falls ich in der Verhandlungsgruppe scheitern sollte und "
            "zurückversetzt würde, würde er mich bitten, eine Versetzung in eine andere Dienststelle zu "
            "beantragen. Ich hätte durch die Bewerbung gezeigt, dass mein Interesse an der "
            "Verkehrsüberwachung zu gering sei, um dort noch produktiv zu sein.<br/><br/>"
            "Dieser Widerspruch hat mich schwer beschäftigt — einerseits Leistungsträger, andererseits im "
            "Fall des Scheiterns nicht mehr willkommen. Unser bis dahin gutes Verhältnis kühlte ab. Der "
            "Direktionsleiter bemerkte das und bat mich, das Gespräch noch einmal zu suchen. Das habe ich "
            "gemacht — mein Gegenüber hat seine Position aber vollständig bestätigt. Ich habe das "
            "akzeptiert, auch wenn ich es anders sah.<br/><br/>"
            "Ich habe das Auswahlverfahren bestanden, die Ausbildungsgruppe abgeschlossen und war im Kommando. "
            "Nach einigen Monaten bin ich aus der Einheit ausgeschieden — und musste zu D610 zurück, zum "
            "selben Dienststellenleiter. Er erinnerte mich an seine Aussagen. Zeitgleich begann meine "
            "schwerste berufliche Phase: Burnout, neun Monate Dienstunfähigkeit.<br/><br/>"
            "Ich habe eine bewusste Entscheidung getroffen: Ich bin offen auf meinen Dienststellenleiter "
            "zugegangen und habe ihn persönlich über meine Situation informiert. Was dann kam, hatte ich "
            "nicht erwartet. Er hat mich bei allen Maßnahmen vollständig unterstützt — die "
            "Wiedereingliederung, die Rückkehr, alles. Die Person, mit der ich den härtesten Konflikt "
            "meiner bisherigen Laufbahn hatte, wurde in meiner verletzlichsten Phase zu meinem wichtigsten "
            "Unterstützer.<br/><br/>"
            "Was ich daraus mitnehme: Brücken nicht abbrechen, auch wenn man sich ungerecht behandelt fühlt. "
            "Transparenz kann eine Beziehung reparieren, die schon verloren schien. Und: Manchmal liegen "
            "beide Seiten gleichzeitig richtig — er schützte seine Einheit, ich verfolgte meinen Weg."
        ),
        "followup": ("Was hätten Sie heute anders gemacht?",
                     "Ich hätte früher und direkt mit ihm gesprochen — bevor die Bewerbung auf dem Dienstweg lief. "
                     "Nicht um ihn zu fragen ob ich es darf, sondern um ihn abzuholen."),
    },
    {
        "num": "6",
        "question": "Wie gehst du mit Stress um? Schildere eine längere Phase.",
        "theme": "Lebenslanger Stressaufbau → Burnout 2018 → 11 Jahre Therapie → aktive Entscheidung nach Tod der Mutter",
        "answer": (
            "Stress begleitet mich, seit ich denken kann. Meine Eltern haben sich getrennt, als ich ein "
            "Teenager war — und ich bin früh in die Rolle gerutscht, zwischen beiden zu vermitteln, beiden "
            "gerecht zu werden, beiden zu erklären. Diese Art von Verantwortung, die eigentlich nicht die "
            "eines Kindes ist, hat mich geprägt.<br/><br/>"
            "Im Erwachsenenleben hat sich das nicht aufgelöst, sondern addiert: Carina und ich haben früh "
            "eine Familie aufgebaut, drei Kinder, zwei Immobilien, finanzielle Engpässe durch mein Studium. "
            "Gleichzeitig haben wir beide unsere Eltern begleitet — meine Mutter mit einer schweren "
            "Lungenerkrankung, mein Vater psychisch stark angeschlagen nach der Trennung, mein Bruder mit "
            "eigenen massiven Problemen. Dazu der Anspruch, im Beruf sichtbar und leistungsfähig zu sein. "
            "Das war kein Sprint — das war ein Dauerlauf über viele Jahre.<br/><br/>"
            "2018 war der Punkt, wo dieser Dauerlauf nicht mehr tragbar war. Ich bin ausgefallen. Neun "
            "Monate Dienstunfähigkeit. Das war keine Niederlage — das war ein Signal, das ich nicht länger "
            "ignorieren konnte.<br/><br/>"
            "Seit 2015 bin ich in psychotherapeutischer Begleitung. Das klingt lang — ist es auch. Aber "
            "genau diese Zeit hat mir etwas gegeben, das keine Fortbildung ersetzen kann: Ich kenne meine "
            "Warnsignale. Ich weiß, wann mein System übersteuert. Ich habe gelernt, früher zu reagieren, "
            "statt erst dann, wenn es zu spät ist.<br/><br/>"
            "Konkret erlebt habe ich das nach dem Tod meiner Mutter 2024. In einer Phase, in der ich alles "
            "hätte weiterlaufen lassen können wie bisher, habe ich stattdessen eine aktive Entscheidung "
            "getroffen: raus aus der Lehrtätigkeit an der Hochschule, weg von der täglichen Pendelstrecke "
            "nach Wiesbaden — hin zu einer Stelle näher an meiner Region. Das war kein bequemer Weg: der "
            "notwendige Zwischenschritt war zunächst ein Pflichthalbjahr im Wechselschichtdienst — also "
            "kurzfristig sogar mehr Belastung. Aber das war vorab abgesprochen und kalkuliert. Das Ziel "
            "war der Tagdienst im Regionalen Verkehrsdienst Hochtaunus — und das hat geklappt.<br/><br/>"
            "Ich bin Sportler durch und durch. Ich gehe über mein Limit — das gehört zu mir. Aber ich weiß "
            "jetzt, wo die Grenze ist. Und ich weiß: Noch ein Burnout braucht kein Mensch. Das ist keine "
            "Schwäche. Das ist Erfahrung."
        ),
        "followup": ("Was sind Ihre konkreten Warnsignale?",
                     "Schlafstörungen, Reizbarkeit in eigentlich harmlosen Situationen, und das Gefühl, dass mir "
                     "nichts mehr Freude macht — das sind bei mir die frühen Zeichen. Wenn zwei davon gleichzeitig "
                     "auftreten, weiß ich, dass ich reagieren muss."),
    },
    {
        "num": "7",
        "question": "Hast du eine persönliche Entscheidung getroffen, die Auswirkung auf andere hatte?",
        "theme": "Bruder aus Eigentumswohnung verwiesen — Selbstschutz vs. Verantwortung gegenüber dem Bruder",
        "answer": (
            "Mein Bruder hat über mehrere Jahre in einer meiner Eigentumswohnungen gewohnt. Über drei Jahre "
            "hinweg hat sich die Situation dort zunehmend verschlechtert — verbale und körperliche "
            "Auseinandersetzungen mit seiner damaligen Begleiterin, immer wieder verursacht durch Alkohol "
            "und Drogen. Die anderen Bewohner der Gemeinschaft waren massiv belastet, und ich als Eigentümer "
            "war der Ansprechpartner für alle.<br/><br/>"
            "Das Schwierige war: Es gab keinen einfachen Ausweg. Mein Bruder ist Bürgergeldempfänger — eine "
            "Wohnung im Hochtaunuskreis zu finden, die das Amt finanziert, ist faktisch unmöglich. Dazu kam, "
            "dass der langfristige Plan eigentlich vorsah, dass er diese Wohnung irgendwann übernehmen "
            "sollte. Das war kein spontaner Entschluss, den ich aufgegeben habe — das war ein über Jahre "
            "gewachsener Plan, der an dem Punkt nicht mehr haltbar war.<br/><br/>"
            "Ich habe ihm gesagt, dass er ausziehen muss. Das war klar, direkt und ohne Hintertür. Ich habe "
            "ihm dabei auch erklärt warum: Wir haben ihm über die Jahre wiederholt geholfen — bei Wohnungen, "
            "bei Jobs, bei Behörden. Er hat diese Chancen nicht genutzt. Irgendwann muss jemand die "
            "Verantwortung für sein eigenes Handeln übernehmen — und das kann ich nicht stellvertretend "
            "für ihn tragen.<br/><br/>"
            "Diese Entscheidung war zu seinem Nachteil. Das weiß ich. Und ich habe sie trotzdem getroffen — "
            "weil sie die einzige war, die mich, meine Familie und die anderen Bewohner schützte. Nicht alles "
            "lösen zu können, was man lösen möchte, ist eine eigene Art von Verantwortung.<br/><br/>"
            "Was ich daraus mitgenommen habe: Eine Entscheidung, die anderen schadet, kann trotzdem die "
            "richtige sein. Wichtig ist, dass man sie klar kommuniziert, die Gründe benennt — und nicht so "
            "tut, als gäbe es keine Alternative, wenn man die Alternativen längst ausgeschöpft hat."
        ),
        "followup": ("Haben Sie gezweifelt?",
                     "Ja — über Jahre. Das war auch notwendig, denn die Entscheidung musste reifen. Der Zweifel "
                     "ist nicht das Problem. Das Problem wäre gewesen, ihn weiter als Entschuldigung zu benutzen, "
                     "nichts zu tun. Es wäre schlicht schlimmer geworden."),
    },
    {
        "num": "8",
        "question": "Was macht deine OE gut — und was schlecht?",
        "theme": "RVD positiv — strukturelle Ressourcenknappheit als systemisches Problem",
        "answer": (
            "Ich bin seit Februar im RVD Hochtaunus — das sind knapp drei Monate. Eine tiefe Beurteilung "
            "wäre anmaßend. Ich kann aber sagen, was ich in dieser Zeit wahrgenommen habe — und was ich "
            "grundsätzlich für entscheidend halte.<br/><br/>"
            "Was eine Organisationseinheit gut macht, erlebe ich nicht zum ersten Mal: In den sechs Monaten "
            "Wechselschichtdienst an der Polizeistation Usingen davor habe ich erlebt, was Teamkultur in "
            "ihrer reinsten Form bedeutet. Ein Korpsgeist, der trägt, weil jeder weiß: der andere springt "
            "ein, wenn es nötig ist. Stärken werden genutzt, Schwächen ausgeglichen, ohne dass jemand "
            "darüber reden muss. Das funktioniert nicht durch Anweisung — das entsteht durch Haltung.<br/><br/>"
            "Was ich konkret beim RVD erlebe: Transparenz, klare Kommunikation der Erwartungen, eine Führung "
            "die erreichbar ist, und ein Team das füreinander da ist. Das sind keine Selbstverständlichkeiten. "
            "Ich bin aufrichtig positiv überrascht.<br/><br/>"
            "Zum Schwachen — und das gilt nicht nur für meinen RVD, sondern für fast jede "
            "Organisationseinheit im Polizeivollzug: Der Spagat zwischen Aufgabenvolumen und verfügbaren "
            "Ressourcen. Wir haben klare Aufträge, aber selten das Personal, um sie so zu erfüllen wie "
            "wir es eigentlich wollen. Das erzeugt einen strukturellen Druck, der auf Dauer an Teams zehrt — "
            "besonders an den Stellen, die Verlässlichkeit und Verbindlichkeit hochhalten. Das ist kein "
            "Versagen der OE. Das ist eine systemische Herausforderung, mit der jede Führungskraft "
            "umgehen muss."
        ),
        "followup": ("Was würden Sie als Führungskraft konkret anders machen?",
                     "Ressourcen kann ich nicht erschaffen — aber ich kann transparent kommunizieren, was realistisch "
                     "leistbar ist und was nicht. Erwartungsmanagement nach oben und unten ist eine Kernaufgabe "
                     "von Führung."),
    },
    {
        "num": "9",
        "question": "Warum willst du Führungskraft sein?",
        "theme": "C-Jugend Coaching als Beweis für Führungsphilosophie — Klima schaffen statt anweisen",
        "answer": (
            "Ich trainiere seit zwei Jahren eine C-Jugend im Fußball — die Mannschaft, in der mein eigener "
            "Sohn spielt. Und ich erlebe dort gerade etwas, das ich mit Geld nicht kaufen kann.<br/><br/>"
            "Wir haben 22 Spieler, zwei Trainer und eine Elternschaft, die alle an einem Strang ziehen. Wir "
            "stehen auf Tabellenplatz eins, sind auf dem Weg zur Meisterschaft — aber das ist nicht der "
            "Punkt. Der Punkt ist, wie dieser Tabellenplatz entstanden ist: durch eine Mannschaft, die sich "
            "gegenseitig trägt, die füreinander da ist, die mit Freude und Ehrgeiz arbeitet.<br/><br/>"
            "Ich habe neulich über den DFB vergünstigte Karten für ein U19-EM-Qualifikationsspiel der "
            "deutschen Nationalmannschaft angeboten — ich brauchte mindestens zehn Abnehmer. Ich habe in "
            "die Runde gefragt wer Interesse hat mitzufahren. Gemeldet haben sich 36 Personen. Alle "
            "22 Spieler, beide Trainer, und dazu noch Eltern als Fahrer. Freiwillig, ohne Pflicht, einfach "
            "weil das Team dieses Klima hat.<br/><br/>"
            "Das klappt nicht durch Anweisung. Das klappt, weil Menschen das Gefühl haben, dass ihre "
            "Stärken gesehen werden, dass ihnen jemand zutraut was ihnen vorher keiner zugetraut hat, und "
            "dass der Trainer sie als Menschen wahrnimmt — nicht nur als Spieler.<br/><br/>"
            "Ich will das nicht allein mir zuschreiben. Aber ich erlebe, dass diese Art zu führen wirkt. "
            "Und genau das ist meine Motivation: dieses Klima — wo Leistung entsteht, weil Menschen wollen "
            "und nicht weil sie müssen — auch beruflich zu schaffen. Nicht wegen des Titels. Sondern weil "
            "ich weiß, dass ich es kann."
        ),
        "followup": ("Wo sehen Sie den Unterschied zwischen Führung im Sport und Führung im Polizeidienst?",
                     "Im Sport ist Freiwilligkeit die Grundlage. Im Dienst gibt es Pflichten und Hierarchie — das "
                     "ist der Rahmen. Aber das Klima darin, ob Menschen gerne kommen oder ungerne, ob sie "
                     "füreinander einstehen oder nicht — das ist eine Führungsaufgabe. Und da glaube ich, dass "
                     "die Grundprinzipien dieselben sind."),
    },
    {
        "num": "10",
        "question": "Hast du eine Aufgabe übernommen, die für jemand anderen eine große Bedeutung hatte?",
        "theme": "Pflege der Mutter bis zu ihrem Tod — kein reines Opfer, sondern bewusste Entscheidung mit Gegenwert",
        "answer": (
            "Meine Mutter war viele Jahre schwer lungenkrank. Carina und ich waren ihre Hauptbezugspersonen — "
            "wir haben sie begleitet, versorgt, unterstützt, bis zu ihrem Tod im Oktober 2024.<br/><br/>"
            "Das war kein formaler Auftrag. Es war eine Entscheidung, die wir immer wieder neu getroffen "
            "haben — neben Vollzeitjob, drei Kindern, eigenem Haushalt, eigenem Leben. Und ja, es hat Kraft "
            "gekostet. Es war eine der Phasen, die in meiner Geschichte als Belastungsfaktor auftaucht.<br/><br/>"
            "Aber ich will ehrlich sein: Es war kein reines Opfer. Diese Zeit hat mir auch etwas gegeben — "
            "nämlich Zeit mit ihr. Momente, die ich nicht mehr haben kann. Das weiß man vorher nicht, aber "
            "man weiß es danach.<br/><br/>"
            "Was diese Aufgabe für meine Mutter bedeutet hat, das kann ich nicht in Worte fassen. Was ich "
            "sagen kann: Sie ist nicht allein gewesen. Sie ist nicht in ein Heim gekommen. Sie wurde "
            "begleitet — von jemandem, dem das nicht egal war.<br/><br/>"
            "Das ist vielleicht das Treffendste, was ich über meine Motivation sagen kann: Ich möchte, "
            "dass die Menschen in meiner Verantwortung wissen, dass es jemanden gibt, dem es nicht egal ist."
        ),
        "followup": None,
    },
]

for q in questions:
    story.append(Paragraph(f"Frage {q['num']} von 10", ParagraphStyle("qcount", fontSize=9,
        fontName="Helvetica", spaceAfter=2, textColor=colors.HexColor("#999999"))))
    story.append(Paragraph(f"F{q['num']} — {q['question']}", q_style))
    story.append(Paragraph(q['theme'], theme_style))
    story.append(hr())
    story.append(Spacer(1, 0.2*cm))

    for para in q['answer'].split('<br/><br/>'):
        if para.strip():
            story.append(Paragraph(para.strip(), body_style))

    if q['followup']:
        label, answer = q['followup']
        story.append(Paragraph(f'M\u00f6gliche Nachfrage: \u201e{label}\u201c', followup_label))
        story.append(Paragraph(answer, followup_style))

    story.append(Spacer(1, 0.5*cm))

    if q['num'] not in ("5", "10"):
        story.append(PageBreak())

# Kernbotschaften
story.append(PageBreak())
story.append(Paragraph("Kernbotschaften", section_style))
story.append(Paragraph(
    "Diese fünf Botschaften ziehen sich durch alle Antworten. Im Zweifel darauf zurückgreifen.",
    ParagraphStyle("kb_intro", fontSize=10, fontName="Helvetica-Oblique",
        spaceAfter=14, textColor=colors.HexColor("#555555"))))

kernbotschaften = [
    ("1", "Selbstkenntnis statt Selbstdarstellung",
     "Stärken benennen, Schwächen eingestehen — beides glaubwürdig."),
    ("2", "Entscheidungen reifen lassen, dann klar handeln",
     "Kein Zögern aus Feigheit, aber auch kein Aktionismus."),
    ("3", "Führung ist Klima, nicht Kontrolle",
     "Menschen sollen wollen, nicht müssen."),
    ("4", "Transparenz als Haltung",
     "Mit Vorgesetzten, mit Kollegen, mit sich selbst."),
    ("5", "Brücken nicht abbrechen",
     "Auch wenn man sich ungerecht behandelt fühlt."),
]
for num, title, desc in kernbotschaften:
    story.append(Paragraph(f"<b>{num}. {title}</b>", ParagraphStyle("kb_title", fontSize=11,
        fontName="Helvetica-Bold", spaceAfter=2, textColor=colors.HexColor("#1a1a2e"), leftIndent=0)))
    story.append(Paragraph(desc, ParagraphStyle("kb_desc", fontSize=10.5, fontName="Helvetica",
        spaceAfter=10, leading=15, leftIndent=14, textColor=colors.HexColor("#444444"))))

story.append(Spacer(1, 1*cm))
story.append(hr())
story.append(Paragraph(
    "Viel Erfolg am Montag, 20. April 2026.",
    ParagraphStyle("final", fontSize=12, fontName="Helvetica-Bold",
        spaceBefore=12, textColor=colors.HexColor("#1a1a2e"), alignment=TA_CENTER)))

doc.build(story)
print(f"PDF erstellt: {OUTPUT}")
