#!/usr/bin/env python3
"""build/build_index.py — baut index.html (Deutsch) und en.html (English) aus briefe/, quellen/ und daten/.
Aufruf im Repo: python3 build/build_index.py   (keine Abhaengigkeiten ausser Python 3)
Regel: keine Pfade der Analystenseite, kein ORF-Material, nur Worte, eigenes Material und Erzeugnisse.
Struktur (Philipp, 9.10. 15:00): das Ergebnis zuerst, jede Information genau einmal, ein Knopf je Abschnitt.
Sprachen (Philipp, 9.10. 20:30): ein Knopf Deutsch, ein Knopf English; daten/ergebnisse.json ist die Quelle,
daten/ergebnisse.en.json legt die englischen Texte je ID darueber; briefe/en/ sind Uebersetzungen, briefe/ das Original."""
import json, csv, html, os, io, copy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rd(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()

def esc(s):
    return html.escape(str(s))

def md2html(t):
    out, mode = [], None
    def close():
        nonlocal mode
        if mode: out.append('</%s>' % mode); mode = None
    for ln in t.splitlines():
        s = ln.strip()
        if s.startswith('- '):
            if mode != 'ul': close(); out.append('<ul>'); mode = 'ul'
            out.append('<li>%s</li>' % esc(s[2:])); continue
        if len(s) > 2 and s[0].isdigit() and s[1:3] == '. ':
            if mode != 'ol': close(); out.append('<ol>'); mode = 'ol'
            out.append('<li>%s</li>' % esc(s[3:])); continue
        close()
        if s.startswith('# '): out.append('<h3>%s</h3>' % esc(s[2:]))
        elif s.startswith('## '): out.append('<h4>%s</h4>' % esc(s[3:]))
        elif s: out.append('<p>%s</p>' % esc(s))
    close()
    return '\n'.join(out)

BASE = json.loads(rd('daten/ergebnisse.json'))
EN = json.loads(rd('daten/ergebnisse.en.json'))
rows = list(csv.DictReader(io.StringIO(rd('quellen/Quellenliste.csv')), delimiter=';'))

def data(lang):
    """Deutsch: die Quelle. English: dieselben Zahlen, Dateien und Status, Texte je ID aus der Overlay-Datei."""
    D = copy.deepcopy(BASE)
    if lang == 'de':
        D['beleg_pdf'] = [p for p in D.get('beleg_pdf', []) if '-DE.' in p['datei']]
        return D
    for k in ('hinweis_test', 'freigabe_hinweis', 'prompt_regeln', 'beobachtungen', 'offen', 'beleg_pdf'):
        if k in EN: D[k] = EN[k]
    for t in D['takes']:
        t.update(EN['takes'][t['id']])
    for b in D['bilder']:
        b.update(EN['bilder'][b['id']])
    for f in D['fehlversuche']:
        f.update(EN['fehlversuche'][f['id']])
    assert len(D['vorhersagen_detail']) == len(EN['vorhersagen_detail']), 'vorhersagen_detail: DE und EN ungleich lang'
    D['vorhersagen_detail'] = EN['vorhersagen_detail']
    if D.get('original_embed'):
        D['original_embed'] = D['original_embed'].replace('Original: die Einleitung', 'Original: the opening')
    return D

CSS = """
:root{--ink:#1f1f1f;--steel:#474747;--muted:#6f6f6f;--hair:#dedede;--surface:#f7f7f7;--bronze:#a06a24;--red:#8a2b2b;--good:#3f7a4c;--amber:#fff7e6;--amberline:#f0d9a0}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font-family:system-ui,-apple-system,"Helvetica Neue",Arial,sans-serif;font-size:15.5px;line-height:1.55}
.wrap{max-width:1120px;margin:0 auto;padding:28px 24px 100px}
nav{position:sticky;top:0;z-index:9;background:#fff;border-bottom:1px solid var(--hair);padding:8px 14px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
nav a{text-decoration:none;font:700 12px system-ui,sans-serif;padding:5px 9px;border-radius:7px;background:#efefef;color:var(--ink)}nav a:hover{background:#e2e2e2}
nav .lang{margin-left:auto}nav .lang+.lang{margin-left:0}nav a.on{background:#1f1f1f;color:#fff}nav a.on:hover{background:#1f1f1f}
nav .brand{margin-left:10px;font:700 11px ui-monospace,Menlo,monospace;letter-spacing:.14em;color:#7a7a7a}
.eyebrow{font:11px ui-monospace,Menlo,monospace;letter-spacing:.24em;text-transform:uppercase;color:var(--bronze);margin:0 0 12px}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:500;font-size:clamp(2rem,5vw,3rem);line-height:1.05;letter-spacing:-.01em;margin:0 0 10px}
.sub{font-style:italic;color:var(--steel);font-size:1.05rem;max-width:70ch;margin:0 0 6px}
h2{font-family:Georgia,serif;font-weight:500;font-size:1.6rem;margin:0 0 8px}h3{font-size:1.05rem;margin:18px 0 6px}
h4{font:700 12px ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--bronze);margin:16px 0 4px}
section{margin-top:52px;scroll-margin-top:60px}p{margin:0 0 12px;max-width:76ch}
.banner{background:var(--amber);border:1px solid var(--amberline);border-left:5px solid var(--red);padding:10px 14px;border-radius:8px;margin:0 0 24px;font-size:14px}
.note{background:var(--amber);border:1px solid var(--amberline);padding:8px 12px;border-radius:7px;font-size:13.5px;margin:0 0 12px}
table{border-collapse:collapse;width:100%;margin-top:10px;font-size:.9rem}th{font:700 10.5px ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);text-align:left;border-bottom:1px solid #cfcfcf;padding:6px 8px}
td{border-bottom:1px solid var(--hair);padding:6px 8px;vertical-align:top}td small,.mono{font:11.5px ui-monospace,Menlo,monospace;color:var(--muted);display:block}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin:14px 0}
.row3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:14px 0}@media(max-width:860px){.row3{grid-template-columns:1fr}}
.row4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:14px 0}@media(max-width:1100px){.row4{grid-template-columns:repeat(2,1fr)}}@media(max-width:860px){.row4{grid-template-columns:1fr}}
figure{margin:0;background:var(--surface);border:1px solid var(--hair);border-radius:10px;overflow:hidden}
figure video,figure img{display:block;width:100%;background:#000}figure img{background:#eee}
figcaption{padding:8px 10px;font-size:.82rem;color:var(--muted);line-height:1.4}figcaption b{display:block;color:var(--ink);font-size:.86rem}
.pend{display:none;padding:28px 10px;text-align:center;color:var(--muted);font-size:.85rem;background:#eee}
.missing video,.missing img{display:none}.missing .pend{display:block}
.locked{aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;text-align:center;background:#2a2a2a;color:#ddd;font-size:.9rem;padding:18px}
.locked a{color:#fff}
.tag{display:inline-block;font:9.5px ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;padding:1px 7px;border-radius:5px;margin-right:5px;color:#fff}
.t-ok{background:var(--good)}.t-rep{background:#8a8a8a}.t-ctl{background:#3a6ea5}.t-open{background:var(--bronze)}.t-orig{background:#1f1f1f}
.brief{background:var(--surface);border:1px solid var(--hair);border-radius:10px;padding:6px 18px 14px;margin:10px 0}.brief p{max-width:78ch}
details summary{cursor:pointer;font-weight:700;padding:8px 0}
.nums{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin:12px 0}.num{background:var(--surface);border:1px solid var(--hair);border-radius:10px;padding:10px 12px}.num b{display:block;font-size:1.5rem;font-family:Georgia,serif;font-weight:500}.num span{font-size:.78rem;color:var(--muted)}
.btn{display:inline-block;background:#1f1f1f;color:#fff;text-decoration:none;font:700 13px system-ui,sans-serif;padding:9px 16px;border-radius:8px}
footer{margin-top:70px;border-top:1px solid var(--hair);padding-top:16px;font-size:.82rem;color:var(--muted)}
"""

# Alle Oberflaechentexte je Sprache. Deutsch ist der Wortlaut der Seite vom 9.10. 18:26 (unveraendert).
S = {'de': dict(
    file='index.html', htmllang='de', title='Goldener Herbst 2026: Reinraum-Fallstudie (FFP)',
    eyebrow='FFP · Goldener Herbst 2026 · Reinraum-Fallstudie · Stand %s',
    h1='Fremdmaterial ersetzen, ohne es zu kopieren',
    sub='Armin Müller-Stahl, die Einleitung: ein Test in zwei Teilen, 8. und 9. Oktober 2026. Wer das Original sieht, schreibt nur einen Brief. Wer erzeugt, sieht das Original nie.',
    vorab='Vorabfassung.', nav_material='Material', lang_de='Deutsch', lang_en='English',
    pend='noch nicht geliefert', urteil='Urteil', kontakt='Kontaktbogen',
    tags={'geliefert': 'Ergebnis', 'ersetzt': 'ersetzt', 'Kontrolle': 'Kontrolle'}, tag_orig='Original',
    orig_cap='Fremdmaterial des Senders; nicht öffentlich. Dieses Material wird ersetzt, nicht kopiert.',
    orig_locked='Im internen Archiv ansehen (Passwort)',
    h_ergebnis='Ergebnis',
    ergebnis_p='Zwei Tests, dieselbe Frage: Lässt sich Fremdmaterial durch Erzeugtes ersetzen, das dieselbe Welt heraufbeschwört, ohne das Original zu kopieren? Links das Original, das nicht verwendet werden darf; daneben die drei erzeugten Fassungen, als Bleistiftzeichnung (Version 1), im 3D-Stil (Version 2) und fotoreal (Version 3), aus demselben Brief und demselben Figurenblatt.',
    ergebnis_h3='Test A: die Einleitung, 30 Sekunden Montage über sechs Jahrzehnte',
    orig_title='Original: die Einleitung',
    orig_text='Archivblock der Sendung, rund zweieinhalb Minuten aus zwölf Quellen. 79 von 96 Ausschnitten wurden von der Rechteabteilung zurückgewiesen.',
    v1='Version 1: Bleistift', v2='Version 2: 3D-Stil', v3='Version 3: Fotoreal',
    ergebnis_note='Weitere Takes (Test B, der Kirchenfürst, fotoreal und 3D-Stil; der Kontrolllauf ohne Figurenblatt; die drei ersetzten Takes) liegen mit Prompt, Kontaktbogen und Ledger unter <a href="videos/">videos/</a> und sind in der Quellenliste als V-001 bis V-009 geführt. Der Kontrolllauf ergab, blind beurteilt: ohne Figurenblatt entsteht ein plausibler alter Kardinal, der nicht er ist. Das Blatt kauft die Ähnlichkeit, die Worte kaufen den Typ.',
    h_warum='Warum',
    warum="""<p>Für die Einleitungen der Sendung hat FFP im Archivsystem des Senders nur Material gesucht, das dort als frei markiert war, es bestellt und in die Einleitungen geschnitten. Die Rechteabteilung des ORF hat anschließend fast alles zurückgewiesen: Von 96 verwendeten Ausschnitten kamen 79 mit „Nein“ oder „Nein, aber“ zurück, 17 waren frei.</p>
<p>Die Fallstudie prüft einen Ausweg: Das Fremdmaterial wird nicht kopiert, sondern durch erzeugtes Material ersetzt, das dieselbe Welt heraufbeschwört, ohne den Schnitt nachzubauen. Dafür gibt es eine Wand: Wer das Original sieht, schreibt nur einen Brief auf Flughöhe eines Pitches. Wer erzeugt, sieht das Original nie.</p>
<p>Beispiel: Armin Müller-Stahl. Sein Einverständnis für Gesicht und Material liegt FFP mündlich vor, die schriftliche Fassung wird nachgereicht; was fehlt, sind die Rechte der Filmproduzenten. Deshalb darf er erscheinen, die Szenen müssen neu sein.</p>""",
    h_wand='Die Wand',
    wand="""<table><tr><th>Analystenseite (ffp-archive)</th><th>Was hinübergeht</th><th>Erzeugerseite (storyboard, imagegen, videogen)</th></tr>
<tr><td>Sieht alles: Schnitt, Quellen, Standbilder im Sekundenabstand, Schnitterkennung innerhalb der Clips, Sprecherspur. Führt eine private Shotliste.</td><td><b>Nur der Brief.</b> Sechs Teile: Welt, Bogen, Stimmung und Bildsprache, Personen als Typen, Rhythmus in Worten, Ausschlüsse. Dazu wiederkehrende Motive. Nie: Titel, Sender, Zahl, Länge oder Reihenfolge der Einstellungen, Kompositionen.</td><td>Sieht das Original nie. Baut aus dem Brief Storyboards in zwei Stilen, dann Bilder und Video. Jede Ablehnung wird protokolliert, jeder Fehlversuch bleibt stehen.</td></tr></table>
<p style="margin-top:12px">Das Gesicht der Hauptfigur kommt aus eigenem Material: Standbilder aus dem Interview, das FFP 2026 mit ihm gedreht hat. Keine Filmbilder, keine Sendungsbilder, keine Pressefotos gehen in die Erzeugung; auch private Set-Fotos, die er uns gab, nicht, weil der Abzug kein Nutzungsrecht ist.</p>""",
    h_briefe='Briefe', briefdir='briefe/',
    briefe_note='Das sind die Texte, die über die Wand gegangen sind. Nichts anderes. Die Dateien liegen unter <a href="briefe/">briefe/</a>.',
    brief_titles=['Brief A: die Einleitung, ganzer Block', 'Brief B: eine Sequenz, der Kirchenfürst', 'Brief B, Anhang: das Figurenblatt'],
    h_figur='Figurenblatt',
    figur_p='Eine Figur, die durch alle Bilder dieselbe bleibt: derselbe Mann, aus fünf Interviewbildern (1080p, Kopf und Schultern, native Pixel) zuerst im echten Alter gebaut, dann in Worten um achtzehn Jahre zurückgesetzt, dann als Kardinal eingekleidet, dann in den 3D-Stil übersetzt, dazu vier Altersblätter. Jeder Schritt ist ein Edit des vorigen mit einer einzigen Variablen. Vor dem ersten Lauf: Blatt neben den Interviewbildern, per Auge, Identität, nicht Alter (Regel R-001).',
    h_vorhersagen='Vorhersagen',
    vorhersagen_p='Jede Vorhersage wurde geschrieben, bevor Credits ausgegeben wurden, und danach benotet; die Prompts hat Philipp vor jedem Lauf gesehen. Neun Takes, alle aus denselben Briefen und demselben Figurenblatt.',
    nums=['Vorhersagen vorab', 'gehalten', 'gescheitert', 'teilweise', 'nicht gelaufen', 'Video-Credits, %d Abbuchungen'], thousands='.',
    vth=['Vor der Ausgabe geschrieben', 'Quote', 'Urteil'],
    h_regeln='Regeln', rth=['Regel', 'Wortlaut'],
    regeln=[('R-001 Identität', 'Vor dem ersten Seeden: Figurenblatt Seite an Seite plus Differenzbild gegen die Interviewbilder, per Auge, geprüft wird Identität, nicht Alter. Kein KI-Upscale auf ein echtes Gesicht, nur Lanczos.'),
            ('R-002 Zeilen', 'Jede erzeugte Eingabe bekommt eine eigene Zeile in der Quellenliste mit Verweis auf ihre Eingaben, Modell, Transport, Größe, Lauf. Wer erzeugt, schickt die Zeile; ffp-archive trägt ein.'),
            ('R-003 Alter', 'Altersedits in Stufen von 15 bis 20 Jahren, jede Stufe als Edit des gebundenen Vorgängers. Das Pro-Modell komponiert oder editiert dieses Gesicht nur im Alter der gebundenen Referenz; jede Altersverschiebung trägt das Flash-Modell.'),
            ('R-004 Wasserzeichen', 'Aufgehoben am 9.10.: Takes und Standbilder gehen so wie sie sind auf die Seite. Bei externer Weitergabe neu entscheiden.'),
            ('P-001 Einwilligungssatz', 'Das Pro-Modell lieferte dieses Gesicht erst mit einem Eingangssatz, der eine schriftliche Einwilligung behauptet. Sie liegt noch nicht vor. Bedingung: schriftlich nachreichen, sonst Satz aus allen Prompts.')],
    h_promptregeln='Prompt-Regeln aus den Läufen', h_beob='Beobachtungen',
    h_fehl='Fehlversuche',
    fehl_p='Bleiben stehen, neben der Korrektur; die ersetzten Takes liegen mit Ledger unter <a href="videos/">videos/</a>.', fth=['Zeile', 'Was', 'Warum'],
    h_beleg='Beleg zum Download',
    beleg_p='Die Fallstudie auf einer Seite: sieben Takes, Vorhersagen mit Quote und Urteil, Regeln, Vorbehalte. Vertraulich / intern. Die englische Fassung liegt auf der <a href="en.html">englischen Seite</a>.',
    h_interview='Interview',
    interview_p='Der nächste Schritt für einen Sender: Ein Redakteur beantwortet ein kurzes geführtes Interview, und die Antworten schalten Vorschläge frei, die zum Format passen, so wie das EWM-Interview bei Empirica ein Arbeitsprotokoll erzeugt.',
    interview_h4='Die Fragen, erster Entwurf',
    fragen=['Welcher Dokumentarstil: Porträt, Reportage, Essay, Archivfilm, Hybrid?', 'Welcher Sender und welches Programm?', 'Welcher Sendeplatz und welche Uhrzeit?', 'Welche Länge?', 'Welches Publikum und welche Tonlage?', 'Welches Material ist frei, welches nicht?'],
    interview_btn='Interview starten', interview_alert='Das Interview folgt. Die Fragen stehen oben; die Vorschläge werden daraus abgeleitet.', interview_mono='Knopf steht, Interview folgt.',
    h_quellen='Quellenliste',
    quellen_p='Jedes Bild, das in einen Lauf geht oder einen Menschen bei der Arbeit leitet, hat eine Zeile, bevor es verwendet wird: Herkunft, Lizenz, ob es in die Erzeugung darf, wer es geprüft hat. %d Zeilen. Vollständig als <a href="quellen/Quellenliste.csv">CSV</a>, Felder und Regeln in der <a href="quellen/LIES_MICH_Quellenliste.md">LIES_MICH</a>.',
    quellen_sum='Alle Zeilen anzeigen', qth=['ID', 'Datei', 'Art', 'Provenienz', 'Urheber · Lizenz', 'Erlaubt', 'Erzeugung', 'Lauf', 'Geprüft'],
    h_offen='Offen',
    h_material='Material',
    material_p='Alles, was zum Ergebnis geführt hat: die weiteren Takes und Bilder, die Briefe, Vorhersagen, Regeln, Fehlversuche, die Belege zum Download, das Interview, die Quellenliste und das interne Archiv. Je Thema einklappbar.',
    weitere_sum='Weitere Takes (Test B, Kontrolle, ersetzte Takes)',
    weitere=['Test B, fotoreal', 'Test B, 3D-Stil', 'Test B, Kontrolle ohne Figurenblatt', 'Test A fotoreal, Take 1 (ersetzt)', 'Test B fotoreal, Take 1 (ersetzt)', 'Test A Bleistift, Take 1 gemischt (ersetzt)'],
    blind='<b>Blind-Test</b>Links die Kontrolle ohne Blatt, Mitte der Take mit Blatt, rechts ein Interviewbild. Philipp sah es blind: links ist er es nicht. Das Blatt kauft die Ähnlichkeit, die Worte kaufen den Typ (H-003).',
    archiv_sum='Archiv 2020 bis 2026 (intern)',
    archiv_p='Das Archiv der Sendung, gepflegt von ffp-archive: Dramaturgie, Material pro Person, Produkte, Analyse, Technik, Rechte. Es ist Teil dieser Seite; <a href="archiv.html">in voller Größe öffnen</a>.',
    archiv_title='Archiv 2020 bis 2026',
    footer='F.F.P. Film &amp; Fernsehproduktion GmbH, Unterer Schreiberweg 29/5, A-1190 Wien, <a href="https://www.ffp.at">www.ffp.at</a> · powered by EmpiricaAI, <a href="https://www.getempirica.com">www.getempirica.com</a> · Keine Rechtsberatung. Seite gebaut aus briefe/, quellen/ und daten/ergebnisse.json (ffp-archive, storyboard).',
), 'en': dict(
    file='en.html', htmllang='en', title='Goldener Herbst 2026: clean-room case study (FFP)',
    eyebrow='FFP · Goldener Herbst 2026 · Clean-room case study · As of %s',
    h1='Replacing third-party material without copying it',
    sub='Armin Müller-Stahl, the opening: a test in two parts, 8 and 9 October 2026. Whoever sees the original writes only a brief. Whoever generates never sees the original.',
    vorab='Preliminary version.', nav_material='Material', lang_de='Deutsch', lang_en='English',
    pend='not delivered yet', urteil='Verdict', kontakt='Contact sheet',
    tags={'geliefert': 'Result', 'ersetzt': 'replaced', 'Kontrolle': 'Control'}, tag_orig='Original',
    orig_cap='Third-party material of the broadcaster; not public. This material is replaced, not copied.',
    orig_locked='View in the internal archive (password)',
    h_ergebnis='Result',
    ergebnis_p='Two tests, the same question: can third-party material be replaced by generated material that evokes the same world without copying the original? On the left the original, which may not be used; beside it the three generated versions, as a pencil drawing (Version 1), in the 3D style (Version 2) and photoreal (Version 3), from the same brief and the same character sheet.',
    ergebnis_h3='Test A: the opening, a 30-second montage across six decades',
    orig_title='Original: the opening',
    orig_text='Archive block of the programme, about two and a half minutes from twelve sources. 79 of 96 excerpts were rejected by the rights department.',
    v1='Version 1: Pencil', v2='Version 2: 3D style', v3='Version 3: Photoreal',
    ergebnis_note='Further takes (test B, the church prince, photoreal and 3D style; the control run without character sheet; the three replaced takes) are under <a href="videos/">videos/</a> with prompt, contact sheet and ledger and are listed in the source list as V-001 to V-009. The control run showed, judged blind: without the character sheet a plausible old cardinal appears who is not him. The sheet buys the likeness, the words buy the type.',
    h_warum='Why',
    warum="""<p>For the openings of the programme, FFP searched the broadcaster's archive system only for material marked as free there, ordered it and cut it into the openings. The ORF rights department then rejected almost all of it: of 96 excerpts used, 79 came back with "no" or "no, but", 17 were free.</p>
<p>The case study tests a way out: the third-party material is not copied but replaced by generated material that evokes the same world without rebuilding the cut. For that there is a wall: whoever sees the original writes only a brief at the altitude of a pitch. Whoever generates never sees the original.</p>
<p>Example: Armin Müller-Stahl. FFP holds his verbal consent for face and material, the written version is to follow; what is missing are the rights of the film producers. So he may appear, the scenes have to be new.</p>""",
    h_wand='The wall',
    wand="""<table><tr><th>Analyst side (ffp-archive)</th><th>What crosses</th><th>Generating side (storyboard, imagegen, videogen)</th></tr>
<tr><td>Sees everything: the cut, sources, stills at one-second intervals, cut detection inside the clips, the narration track. Keeps a private shot list.</td><td><b>Only the brief.</b> Six parts: world, arc, mood and visual language, people as types, rhythm in words, exclusions. Plus recurring motifs. Never: titles, broadcaster, number, length or order of shots, compositions.</td><td>Never sees the original. Builds storyboards in two styles from the brief, then images and video. Every rejection is logged, every failed attempt stays on record.</td></tr></table>
<p style="margin-top:12px">The face of the main character comes from our own material: stills from the interview FFP filmed with him in 2026. No film images, no broadcast images, no press photos go into the generation; nor do private set photos he gave us, because a print is not a licence.</p>""",
    h_briefe='Briefs', briefdir='briefe/en/',
    briefe_note='These are the texts that crossed the wall. Nothing else. Shown here in English translation; the German files under <a href="briefe/">briefe/</a> are the record.',
    brief_titles=['Brief A: the opening, whole block', 'Brief B: one sequence, the church prince', 'Brief B, annex: the character sheet'],
    h_figur='Character sheet',
    figur_p='One character that stays the same through every image: the same man, built first at his real age from five interview stills (1080p, head and shoulders, native pixels), then set back eighteen years in words, then dressed as a cardinal, then translated into the 3D style, plus four age sheets. Every step is an edit of the previous one with a single variable. Before the first run: sheet beside the interview stills, by eye, identity, not age (rule R-001).',
    h_vorhersagen='Predictions',
    vorhersagen_p='Every prediction was written before credits were spent and graded afterwards; Philipp saw the prompts before every run. Nine takes, all from the same briefs and the same character sheet.',
    nums=['predictions in advance', 'held', 'failed', 'partial', 'not run', 'video credits, %d charges'], thousands=',',
    vth=['Written before spending', 'Odds', 'Verdict'],
    h_regeln='Rules', rth=['Rule', 'Wording'],
    regeln=[('R-001 Identity', 'Before the first seeding: character sheet side by side plus a difference image against the interview stills, by eye; what is checked is identity, not age. No AI upscale on a real face, Lanczos only.'),
            ('R-002 Rows', 'Every generated input gets its own row in the source list with a reference to its inputs, model, transport, size, run. Whoever generates sends the row; ffp-archive enters it.'),
            ('R-003 Age', 'Age edits in steps of 15 to 20 years, each step an edit of the bound predecessor. The Pro model composes or edits this face only at the age of the bound reference; every age shift is carried by the Flash model.'),
            ('R-004 Watermark', 'Lifted on 9 Oct: takes and stills go onto the page as they are. Decide afresh before passing anything on externally.'),
            ('P-001 Consent sentence', 'The Pro model delivered this face only with an opening sentence asserting written consent. That consent is not yet on file. Condition: supply it in writing, otherwise the sentence comes out of every prompt.')],
    h_promptregeln='Prompt rules from the runs', h_beob='Observations',
    h_fehl='Failed attempts',
    fehl_p='They stay on record, beside the correction; the replaced takes are under <a href="videos/">videos/</a> with their ledgers.', fth=['Row', 'What', 'Why'],
    h_beleg='Download the record',
    beleg_p='The case study on one page: seven takes, predictions with odds and verdict, rules, flags. Confidential / internal. The German version is on the <a href="index.html">German page</a>.',
    h_interview='Interview',
    interview_p='The next step for a broadcaster: an editor answers a short guided interview, and the answers unlock suggestions that fit the format, the way the EWM interview at Empirica produces a working protocol.',
    interview_h4='The questions, first draft',
    fragen=['Which documentary style: portrait, reportage, essay, archive film, hybrid?', 'Which broadcaster and which programme?', 'Which slot and what time?', 'What length?', 'Which audience and which tone?', 'Which material is cleared, which is not?'],
    interview_btn='Start the interview', interview_alert='The interview follows. The questions are above; the suggestions will be derived from them.', interview_mono='Button is in place, interview follows.',
    h_quellen='Source list',
    quellen_p='Every image that goes into a run or guides a person at work has a row before it is used: origin, licence, whether it may go into the generation, who checked it. %d rows. The rows are the record as kept by ffp-archive and stay in German. Complete as <a href="quellen/Quellenliste.csv">CSV</a>, fields and rules in the <a href="quellen/LIES_MICH_Quellenliste.md">README</a> (German).',
    quellen_sum='Show all rows', qth=['ID', 'File', 'Type', 'Provenance', 'Author · Licence', 'Permitted', 'Generation', 'Run', 'Checked'],
    h_offen='Open',
    h_material='Material',
    material_p='Everything that led to the result: the further takes and stills, the briefs, predictions, rules, failed attempts, the record to download, the interview, the source list and the internal archive. Collapsible per topic.',
    weitere_sum='Further takes (test B, control, replaced takes)',
    weitere=['Test B, photoreal', 'Test B, 3D style', 'Test B, control without character sheet', 'Test A photoreal, take 1 (replaced)', 'Test B photoreal, take 1 (replaced)', 'Test A pencil, take 1 mixed (replaced)'],
    blind='<b>Blind test</b>Left the control without sheet, middle the take with sheet, right an interview still. Philipp saw it blind: on the left it is not him. The sheet buys the likeness, the words buy the type (H-003).',
    archiv_sum='Archive 2020 to 2026 (internal)',
    archiv_p='The programme\'s archive, kept by ffp-archive, in German: dramaturgy, material per person, products, analysis, technology, rights. It is part of this page; <a href="archiv.html">open at full size</a>.',
    archiv_title='Archive 2020 to 2026',
    footer='F.F.P. Film &amp; Fernsehproduktion GmbH, Unterer Schreiberweg 29/5, A-1190 Vienna, <a href="https://www.ffp.at">www.ffp.at</a> · powered by EmpiricaAI, <a href="https://www.getempirica.com">www.getempirica.com</a> · Not legal advice. Page built from briefe/, quellen/ and daten/ergebnisse.json (ffp-archive, storyboard).',
)}
BRIEF_FILES = ['Brief_A_Mueller-Stahl_Einleitung.md', 'Brief_B_Mueller-Stahl_Konklave.md', 'Brief_B_Anhang_Figurenblatt.md']


def build(lang):
    D = data(lang); s = S[lang]
    T = {t['id']: t for t in D['takes']}

    def tag(st):
        c = {'geliefert': 't-ok', 'ersetzt': 't-rep', 'Kontrolle': 't-ctl'}.get(st, 't-open')
        return c, s['tags'].get(st, st)

    def take_card(tid, label=None):
        t = T[tid]; c, l = tag(t['status']); b = t['datei'][:-4]
        return ('<figure><video controls preload="metadata" src="videos/%s" onerror="this.parentNode.classList.add(\'missing\')"></video>'
                '<div class="pend">%s<br><span class="mono">videos/%s</span></div>'
                '<figcaption><b>%s</b><span class="tag %s">%s</span>%s · %s<br>%s<br><small>%s · %s: %s · <a href="videos/%s.prompt.txt">Prompt</a> · <a href="videos/%s.ledger.json">Ledger</a> · <a href="videos/%s_kontakt.jpg">%s</a></small></figcaption></figure>'
                % (esc(t['datei']), s['pend'], esc(t['datei']), esc(label or ('%s, %s' % (t['stil'], t['take']))), c, esc(l), esc(t['stil']), esc(t['take']), esc(t['kurz']), esc(t['id']), s['urteil'], esc(t['urteil']), esc(b), esc(b), esc(b), s['kontakt']))

    def original_card(title, text):
        emb = D.get('original_embed')
        body = emb if emb else '<div class="locked"><div>%s<br><br><a href="archiv.html">%s</a></div></div>' % (esc(text), s['orig_locked'])
        return '<figure>%s<figcaption><b>%s</b><span class="tag t-orig">%s</span>%s</figcaption></figure>' % (body, esc(title), s['tag_orig'], s['orig_cap'])

    secs = []
    # 1 Ergebnis
    secs.append(('ergebnis', s['h_ergebnis'], '<p>%s</p><h3>%s</h3><div class="row4">' % (s['ergebnis_p'], s['ergebnis_h3'])
                 + original_card(s['orig_title'], s['orig_text']) + take_card('V-009', s['v1']) + take_card('V-003', s['v2']) + take_card('V-002', s['v3'])
                 + '</div><p class="note">%s</p>' % s['ergebnis_note']))
    # 2 Warum, 3 Wand
    secs.append(('warum', s['h_warum'], s['warum']))
    secs.append(('wand', s['h_wand'], s['wand']))
    # 4 Briefe
    briefs = ''.join('<details open><summary>%s</summary><div class="brief">%s</div></details>' % (esc(t), md2html(rd(s['briefdir'] + f))) for t, f in zip(s['brief_titles'], BRIEF_FILES))
    secs.append(('briefe', s['h_briefe'], '<p class="note">%s</p>' % s['briefe_note'] + briefs))
    # 5 Figurenblatt
    imgs = ''.join('<figure><img src="bilder/%s" alt="%s" loading="lazy" onerror="this.parentNode.classList.add(\'missing\')"><div class="pend">%s<br><span class="mono">bilder/%s</span></div><figcaption><b>%s · %s</b>%s</figcaption></figure>' % (esc(b['datei']), esc(b['titel']), s['pend'], esc(b['datei']), esc(b['id']), esc(b['titel']), esc(b['status'])) for b in D['bilder'] if b['id'] != 'H-003')
    secs.append(('figur', s['h_figur'], '<p>%s</p><div class="grid">%s</div>' % (s['figur_p'], imgs)))
    # 6 Vorhersagen
    v = D['vorhersagen']; k = D['kosten']
    credits = '{:,}'.format(k['video_credits']).replace(',', s['thousands'])
    nums = ''.join('<div class="num"><b>%s</b><span>%s</span></div>' % (esc(a), esc(b)) for a, b in zip([v['gesamt'], v['gehalten'], v['gescheitert'], v['teilweise'], v['nicht_gelaufen'], credits], s['nums'][:5] + [s['nums'][5] % k['abbuchungen']]))
    vdet = ''
    if D.get('vorhersagen_detail'):
        vdet = '<table><tr>%s</tr>' % ''.join('<th>%s</th>' % h for h in s['vth']) + ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (esc(p['claim']), esc(p['quote']), esc(p['urteil'])) for p in D['vorhersagen_detail']) + '</table>'
    secs.append(('vorhersagen', s['h_vorhersagen'], '<p>%s</p><div class="nums">%s</div>%s' % (s['vorhersagen_p'], nums, vdet)))
    # 7 Regeln
    rt = '<table><tr>%s</tr>' % ''.join('<th>%s</th>' % h for h in s['rth']) + ''.join('<tr><td>%s</td><td>%s</td></tr>' % (esc(a), esc(b)) for a, b in s['regeln']) + '</table>'
    secs.append(('regeln', s['h_regeln'], rt + '<h4>%s</h4><ul>' % s['h_promptregeln'] + ''.join('<li>%s</li>' % esc(b) for b in D.get('prompt_regeln', [])) + '</ul><h4>%s</h4><ul>' % s['h_beob'] + ''.join('<li>%s</li>' % esc(b) for b in D['beobachtungen']) + '</ul>'))
    # 8 Fehlversuche
    secs.append(('fehl', s['h_fehl'], '<p>%s</p><table><tr>%s</tr>' % (s['fehl_p'], ''.join('<th>%s</th>' % h for h in s['fth'])) + ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (esc(f['id']), esc(f['was']), esc(f['warum'])) for f in D['fehlversuche']) + '</table>'))
    # 9 Beleg
    if D.get('beleg_pdf'):
        secs.append(('beleg', s['h_beleg'], '<p>%s</p><p>%s</p>' % (s['beleg_p'], ' '.join('<a class="btn" href="%s">%s</a>' % (esc(p['datei']), esc(p['titel'])) for p in D['beleg_pdf']))))
    # 10 Interview
    secs.append(('interview', s['h_interview'], '<p>%s</p><div class="brief"><h4>%s</h4><ol>%s</ol><p><a class="btn" href="#interview" onclick="alert(%s);return false;">%s</a> <span class="mono" style="display:inline;margin-left:8px">%s</span></p></div>'
                 % (s['interview_p'], s['interview_h4'], ''.join('<li>%s</li>' % esc(q) for q in s['fragen']), esc(json.dumps(s['interview_alert'], ensure_ascii=False)), s['interview_btn'], s['interview_mono'])))
    # 11 Quellen
    qt = '<table><tr>%s</tr>' % ''.join('<th>%s</th>' % h for h in s['qth'])
    for r in rows:
        qt += '<tr><td>%s</td><td>%s<small>%s</small></td><td>%s<small>%s</small></td><td>%s</td><td>%s<small>%s</small></td><td>%s</td><td>%s</td><td>%s</td><td>%s<small>%s</small></td></tr>' % (
            esc(r['ID']), esc(r['Datei']), esc(r['SHA256']), esc(r['Art']), esc(r['Bedingung oder Nachweistext']), esc(r['Provenienz-Typ']), esc(r['Urheber']), esc(r['Lizenz']), esc(r['Erlaubt']), esc(r['Geht in die Erzeugung']), esc(r['Verwendet in Lauf']), esc(r['Gepruft von']), esc(r['Datum']))
    qt += '</table>'
    secs.append(('quellen', s['h_quellen'], '<p>%s</p><details><summary>%s</summary>%s</details>' % (s['quellen_p'] % len(rows), s['quellen_sum'], qt)))
    # 12 Offen
    secs.append(('offen', s['h_offen'], '<ul>' + ''.join('<li>%s</li>' % esc(o) for o in D['offen']) + '</ul>'))

    # Philipp, 9.10. 15:15: ein Knopf. Das Ergebnis steht oben; alles andere liegt unten unter Material, je Thema einklappbar.
    w = s['weitere']
    weitere = '<details open><summary>%s</summary><div class="row3">' % s['weitere_sum'] + take_card('V-005', w[0]) + take_card('V-006', w[1]) + take_card('V-007', w[2]) + '</div><div class="row3">' + take_card('V-001', w[3]) + take_card('V-004', w[4]) + take_card('V-008', w[5]) + '</div><figure style="max-width:960px;margin-top:10px"><img src="bilder/gh_B0_vs_B1v3_vs_interview_shot4.jpg" alt="Blind-Test" loading="lazy"><figcaption>%s</figcaption></figure></details>' % s['blind']
    material = weitere + ''.join('<details open><summary>%s</summary><div style="padding:4px 0 18px">%s</div></details>' % (esc(t), h) for k_, t, h in secs if k_ != 'ergebnis') + '<details id="archiv" open><summary>%s</summary><p>%s</p><iframe src="archiv.html" title="%s" style="width:100%%;height:85vh;border:1px solid var(--hair);border-radius:10px;background:#fff" loading="lazy"></iframe></details>' % (s['archiv_sum'], s['archiv_p'], s['archiv_title'])
    nav = '<a href="#material">%s</a><a class="lang%s" href="index.html" lang="de">%s</a><a class="lang%s" href="en.html" lang="en">%s</a><span class="brand">FFP · GOLDENER HERBST 2026</span>' % (
        s['nav_material'], ' on' if lang == 'de' else '', s['lang_de'], ' on' if lang == 'en' else '', s['lang_en'])
    body = ''.join('<section id="%s"><h2>%s</h2>%s</section>' % (k_, esc(t), h) for k_, t, h in secs if k_ == 'ergebnis') + '<section id="material"><h2>%s</h2><p>%s</p>%s</section>' % (s['h_material'], s['material_p'], material)
    banner = '' if D.get('freigabe_oeffentlich') else '<div class="banner"><b>%s</b> %s</div>' % (s['vorab'], esc(D.get('freigabe_hinweis', '')))
    if D.get('hinweis_test'):
        banner += '<div class="banner" style="border-left-color:#d0021b;background:#fff;border-color:#d0021b;color:#d0021b;font-weight:700;letter-spacing:.02em">%s</div>' % esc(D['hinweis_test'])
    page = """<!doctype html>
<html lang="%s"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title><link rel="alternate" hreflang="de" href="index.html"><link rel="alternate" hreflang="en" href="en.html"><style>%s</style></head>
<body><nav>%s</nav><div class="wrap">
<p class="eyebrow">%s</p>
<h1>%s</h1>
<p class="sub">%s</p>
%s%s
<footer>%s</footer>
</div></body></html>""" % (s['htmllang'], esc(s['title']), CSS, nav, s['eyebrow'] % esc(D['stand']), s['h1'], s['sub'], banner, body, s['footer'])
    with open(os.path.join(ROOT, s['file']), 'w', encoding='utf-8') as f:
        f.write(page)
    print(s['file'], len(page), 'bytes,', len(rows), 'Quellen,', len(D['takes']), 'Takes,', len(D['bilder']), 'Bilder')

for lang in ('de', 'en'):
    build(lang)
