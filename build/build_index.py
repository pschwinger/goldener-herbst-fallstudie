#!/usr/bin/env python3
"""build/build_index.py — baut index.html aus briefe/, quellen/ und daten/ergebnisse.json.
Aufruf im Repo: python3 build/build_index.py   (keine Abhaengigkeiten ausser Python 3)
Regel: keine Pfade der Analystenseite, kein ORF-Material, nur Worte, eigenes Material und Erzeugnisse."""
import json, csv, html, os, io

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

D = json.loads(rd('daten/ergebnisse.json'))
rows = list(csv.DictReader(io.StringIO(rd('quellen/Quellenliste.csv')), delimiter=';'))

CSS = """
:root{--ink:#1f1f1f;--steel:#474747;--muted:#6f6f6f;--hair:#dedede;--surface:#f7f7f7;--bronze:#a06a24;--red:#8a2b2b;--good:#3f7a4c;--amber:#fff7e6;--amberline:#f0d9a0}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font-family:system-ui,-apple-system,"Helvetica Neue",Arial,sans-serif;font-size:15.5px;line-height:1.55}
.wrap{max-width:1060px;margin:0 auto;padding:28px 24px 100px}
nav{position:sticky;top:0;z-index:9;background:#fff;border-bottom:1px solid var(--hair);padding:8px 14px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
nav a{text-decoration:none;font:700 12px system-ui,sans-serif;padding:5px 9px;border-radius:7px;background:#efefef;color:var(--ink)}nav a:hover{background:#e2e2e2}
nav .brand{margin-left:auto;font:700 11px ui-monospace,Menlo,monospace;letter-spacing:.14em;color:#7a7a7a}
.eyebrow{font:11px ui-monospace,Menlo,monospace;letter-spacing:.24em;text-transform:uppercase;color:var(--bronze);margin:0 0 12px}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:500;font-size:clamp(2rem,5vw,3rem);line-height:1.05;letter-spacing:-.01em;margin:0 0 10px}
.sub{font-style:italic;color:var(--steel);font-size:1.05rem;max-width:70ch;margin:0 0 6px}
h2{font-family:Georgia,serif;font-weight:500;font-size:1.6rem;margin:0 0 8px}h3{font-size:1.05rem;margin:18px 0 6px}
h4{font:700 12px ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--bronze);margin:16px 0 4px}
section{margin-top:52px;scroll-margin-top:60px}p{margin:0 0 12px;max-width:76ch}
.k{font:10.5px ui-monospace,Menlo,monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--bronze);margin:0 0 8px}
.banner{background:var(--amber);border:1px solid var(--amberline);border-left:5px solid var(--red);padding:10px 14px;border-radius:8px;margin:0 0 24px;font-size:14px}
.note{background:var(--amber);border:1px solid var(--amberline);padding:8px 12px;border-radius:7px;font-size:13.5px;margin:0 0 12px}
table{border-collapse:collapse;width:100%;margin-top:10px;font-size:.9rem}th{font:700 10.5px ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);text-align:left;border-bottom:1px solid #cfcfcf;padding:6px 8px}
td{border-bottom:1px solid var(--hair);padding:6px 8px;vertical-align:top}td small,.mono{font:11.5px ui-monospace,Menlo,monospace;color:var(--muted);display:block}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin:14px 0}
figure{margin:0;background:var(--surface);border:1px solid var(--hair);border-radius:10px;overflow:hidden}
figure video,figure img{display:block;width:100%;background:#000}figure img{background:#eee}
figcaption{padding:8px 10px;font-size:.82rem;color:var(--muted);line-height:1.4}figcaption b{display:block;color:var(--ink);font-size:.86rem}
.pend{display:none;padding:28px 10px;text-align:center;color:var(--muted);font-size:.85rem;background:#eee}
.missing video,.missing img{display:none}.missing .pend{display:block}
.tag{display:inline-block;font:9.5px ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;padding:1px 7px;border-radius:5px;margin-right:5px;color:#fff}
.t-ok{background:var(--good)}.t-rep{background:#8a8a8a}.t-ctl{background:#3a6ea5}.t-open{background:var(--bronze)}
.brief{background:var(--surface);border:1px solid var(--hair);border-radius:10px;padding:6px 18px 14px;margin:10px 0}.brief p{max-width:78ch}
details summary{cursor:pointer;font-weight:700;padding:8px 0}
.nums{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin:12px 0}.num{background:var(--surface);border:1px solid var(--hair);border-radius:10px;padding:10px 12px}.num b{display:block;font-size:1.5rem;font-family:Georgia,serif;font-weight:500}.num span{font-size:.78rem;color:var(--muted)}
footer{margin-top:70px;border-top:1px solid var(--hair);padding-top:16px;font-size:.82rem;color:var(--muted)}
"""

secs = []
# Warum
secs.append(('warum', 'Warum', """
<p class="lede">Für die Einleitungen der Sendung hat FFP im Archivsystem des Senders nur Material gesucht, das dort als frei markiert war, es bestellt und in die Einleitungen geschnitten. Die Rechteabteilung des ORF hat anschließend fast alles zurückgewiesen: Von 96 verwendeten Ausschnitten kamen 79 mit „Nein“ oder „Nein, aber“ zurück, 17 waren frei.</p>
<p>Die Fallstudie prüft einen Ausweg: Das Fremdmaterial wird nicht kopiert, sondern durch erzeugtes Material ersetzt, das dieselbe Welt heraufbeschwört, ohne den Schnitt nachzubauen. Dafür gibt es eine Wand: Wer das Original sieht, schreibt nur einen Brief auf Flughöhe eines Pitches. Wer erzeugt, sieht das Original nie.</p>
<p>Beispiel: Armin Müller-Stahl. Sein Einverständnis für Gesicht und Material liegt FFP mündlich vor, die schriftliche Fassung wird nachgereicht; was fehlt, sind die Rechte der Filmproduzenten. Deshalb darf er erscheinen, die Szenen müssen neu sein.</p>
<h3>Die zwei Tests</h3>
<table><tr><th></th><th>Material</th><th>Frage</th><th>Stile</th></tr>
<tr><td><b>Test A</b></td><td>Der ganze Archivblock der Einleitung, rund zweieinhalb Minuten aus zwölf Quellen unter einem Sprechertext</td><td>Trägt ein Brief auf Flughöhe eine ganze Montage?</td><td>3D-Stil und fotoreal</td></tr>
<tr><td><b>Test B</b></td><td>Eine einzelne Stelle: wenige Sekunden aus einem Kinofilm, in dem er einen Kirchenfürsten spielt</td><td>Entsteht aus einer erfundenen Konklave-Szene „gleiche Geschichte, anderer Film“ statt „gleicher Film, neu gezeichnet“?</td><td>3D-Stil und fotoreal</td></tr></table>"""))
# Wand
secs.append(('wand', 'Die Wand', """
<table><tr><th>Analystenseite (ffp-archive)</th><th>Was hinübergeht</th><th>Erzeugerseite (storyboard, imagegen, videogen)</th></tr>
<tr><td>Sieht alles: Schnitt, Quellen, Standbilder im Sekundenabstand, Schnitterkennung innerhalb der Clips, Sprecherspur. Führt eine private Shotliste.</td><td><b>Nur der Brief.</b> Sechs Teile: Welt, Bogen, Stimmung und Bildsprache, Personen als Typen, Rhythmus in Worten, Ausschlüsse. Dazu wiederkehrende Motive. Nie: Titel, Sender, Zahl, Länge oder Reihenfolge der Einstellungen, Kompositionen.</td><td>Sieht das Original nie. Baut aus dem Brief Storyboards in zwei Stilen, dann Bilder und Video. Jede Ablehnung wird protokolliert, jeder Fehlversuch bleibt stehen.</td></tr></table>
<p style="margin-top:12px">Das Gesicht der Hauptfigur kommt aus eigenem Material: Standbilder aus dem Interview, das FFP 2026 mit ihm gedreht hat. Keine Filmbilder, keine Sendungsbilder, keine Pressefotos gehen in die Erzeugung; auch private Set-Fotos, die er uns gab, nicht, weil der Abzug kein Nutzungsrecht ist.</p>
<p>Der Fremdvergleich am Ende: Ein Unbeteiligter sieht Original und Ergebnis nebeneinander und sagt, ob es „gleiche Geschichte, anderer Film“ ist oder „gleicher Film, neu gezeichnet“. Nur das Erste ist das Ziel.</p>"""))
# Briefe
briefs = ''.join('<details%s><summary>%s</summary><div class="brief">%s</div></details>' % (' open' if i == 0 else '', esc(t), md2html(rd('briefe/' + f))) for i, (t, f) in enumerate([
    ('Brief A: die Einleitung, ganzer Block', 'Brief_A_Mueller-Stahl_Einleitung.md'),
    ('Brief B: eine Sequenz, der Kirchenfürst', 'Brief_B_Mueller-Stahl_Konklave.md'),
    ('Brief B, Anhang: das Figurenblatt', 'Brief_B_Anhang_Figurenblatt.md')]))
secs.append(('briefe', 'Briefe', '<p class="note">Das sind die Texte, die über die Wand gegangen sind. Nichts anderes. Die Dateien liegen unter <a href="briefe/">briefe/</a>.</p>' + briefs))
# Figurenblatt
imgs = ''.join('<figure><img src="bilder/%s" alt="%s" loading="lazy" onerror="this.parentNode.classList.add(\'missing\')"><div class="pend">noch nicht geliefert<br><span class="mono">bilder/%s</span></div><figcaption><b>%s · %s</b>%s</figcaption></figure>' % (esc(b['datei']), esc(b['titel']), esc(b['datei']), esc(b['id']), esc(b['titel']), esc(b['status'])) for b in D['bilder'])
secs.append(('figur', 'Figurenblatt', """
<p>Eine Figur, die durch alle Bilder dieselbe bleibt: derselbe Mann, aus fünf Interviewbildern (1080p, Kopf und Schultern, native Pixel) zuerst im echten Alter gebaut, dann in Worten um achtzehn Jahre zurückgesetzt, dann als Kardinal eingekleidet, dann in den 3D-Stil übersetzt. Jeder Schritt ist ein Edit des vorigen mit einer einzigen Variablen. Vor dem ersten Lauf: Blatt neben den Interviewbildern, per Auge, Identität, nicht Alter (Regel R-001).</p>
<div class="grid">""" + imgs + '</div>'))
# Regeln
secs.append(('regeln', 'Regeln aus dem Lauf', """
<table><tr><th>Regel</th><th>Wortlaut</th></tr>
<tr><td>R-001 Identität</td><td>Vor dem ersten Seeden: Figurenblatt Seite an Seite plus Differenzbild gegen die Interviewbilder, per Auge, geprüft wird Identität, nicht Alter. Kein KI-Upscale auf ein echtes Gesicht, nur Lanczos.</td></tr>
<tr><td>R-002 Zeilen</td><td>Jede erzeugte Eingabe bekommt eine eigene Zeile in der Quellenliste mit Verweis auf ihre Eingaben, Modell, Transport, Größe, Lauf. Wer erzeugt, schickt die Zeile; ffp-archive trägt ein.</td></tr>
<tr><td>R-003 Alter</td><td>Altersedits in Stufen von 15 bis 20 Jahren, jede Stufe als Edit des gebundenen Vorgängers. Das Pro-Modell komponiert oder editiert dieses Gesicht nur im Alter der gebundenen Referenz; jede Altersverschiebung trägt das Flash-Modell.</td></tr>
<tr><td>R-004 Wasserzeichen</td><td>Aufgehoben am 9.10.: Takes und Standbilder gehen so wie sie sind auf die interne Seite. Bei externer Weitergabe neu entscheiden.</td></tr>
<tr><td>P-001 Einwilligungssatz</td><td>Das Pro-Modell lieferte dieses Gesicht erst mit einem Eingangssatz, der eine schriftliche Einwilligung behauptet. Sie liegt noch nicht vor. Bedingung: schriftlich nachreichen, sonst Satz aus allen Prompts.</td></tr></table>
<h4>Beobachtungen</h4><ul>""" + ''.join('<li>%s</li>' % esc(b) for b in D['beobachtungen']) + '</ul>' + ('<h4>Prompt-Regeln aus den Läufen (storyboard)</h4><ul>' + ''.join('<li>%s</li>' % esc(b) for b in D.get('prompt_regeln', [])) + '</ul>' if D.get('prompt_regeln') else '')))
# Ergebnisse
def tag(st):
    return {'geliefert': ('t-ok', 'geliefert'), 'ersetzt': ('t-rep', 'ersetzt'), 'Kontrolle': ('t-ctl', 'Kontrolle')}.get(st, ('t-open', st))
takes = ''
for t in D['takes']:
    c, l = tag(t['status'])
    takes += '<figure><video controls preload="metadata" src="videos/%s" onerror="this.parentNode.classList.add(\'missing\')"></video><div class="pend">noch nicht geliefert<br><span class="mono">videos/%s</span></div><figcaption><b>%s · Test %s · %s · %s</b><span class="tag %s">%s</span>%s<br><small>Urteil: %s</small></figcaption></figure>' % (esc(t['datei']), esc(t['datei']), esc(t['id']), esc(t['test']), esc(t['stil']), esc(t['take']), c, esc(l), esc(t['kurz']), esc(t['urteil']))
v = D['vorhersagen']; k = D['kosten']
nums = ''.join('<div class="num"><b>%s</b><span>%s</span></div>' % (esc(a), esc(b)) for a, b in [(v['gesamt'], 'Vorhersagen vorab'), (v['gehalten'], 'gehalten'), (v['gescheitert'], 'gescheitert'), (v['teilweise'], 'teilweise'), (v['offen'], 'warten auf Urteil'), (v['nicht_gelaufen'], 'nicht gelaufen'), ('{:,}'.format(k['video_credits']).replace(',', '.'), 'Video-Credits, %d Abbuchungen' % k['abbuchungen'])])
vdet = ''
if D.get('vorhersagen_detail'):
    vdet = '<h4>Vorhersagen im Einzelnen</h4><table><tr><th>Vor der Ausgabe geschrieben</th><th>Quote</th><th>Urteil</th></tr>' + ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (esc(p['claim']), esc(p['quote']), esc(p['urteil'])) for p in D['vorhersagen_detail']) + '</table>'
secs.append(('ergebnisse', 'Ergebnisse', '<p>Sieben Takes, alle aus denselben Briefen und demselben Figurenblatt; die Prompts der Erzeugerseite hat Philipp vor jedem Lauf gesehen. Vorhersagen wurden vor der Erzeugung geschrieben und danach benotet.</p><div class="nums">' + nums + '</div><div class="grid">' + takes + '</div><p class="note">Fehlt ein Video, liegt die Datei noch nicht unter <a href="videos/">videos/</a> (Lieferung durch videogen, siehe LIES_MICH dort).</p>' + vdet))
# Beleg (PDF)
if D.get('beleg_pdf'):
    secs.append(('beleg', 'Beleg zum Download', '<p>Die Fallstudie auf einer Seite, Deutsch und Englisch: sieben Takes, Vorhersagen mit Quote und Urteil, Regeln, Vorbehalte. Vertraulich / intern.</p><div class="grid">' + ''.join('<figure><figcaption style="padding:16px 14px"><b><a href="%s">%s</a></b>%s<br><span class="mono">%s</span></figcaption></figure>' % (esc(p['datei']), esc(p['titel']), esc(p['kurz']), esc(p['datei'])) for p in D['beleg_pdf']) + '</div>'))
# Interview (Platzhalter)
secs.append(('interview', 'Interview', """
<p>Der nächste Schritt für einen Sender: Ein Redakteur beantwortet ein kurzes geführtes Interview, und die Antworten schalten Vorschläge frei, die zum Format passen, so wie das EWM-Interview bei Empirica ein Arbeitsprotokoll erzeugt.</p>
<div class="brief"><h4>Die Fragen, erster Entwurf</h4><ol>
<li>Welcher Dokumentarstil: Porträt, Reportage, Essay, Archivfilm, Hybrid?</li>
<li>Welcher Sender und welches Programm?</li>
<li>Welcher Sendeplatz und welche Uhrzeit?</li>
<li>Welche Länge?</li>
<li>Welches Publikum und welche Tonlage?</li>
<li>Welches Material ist frei, welches nicht?</li>
</ol>
<p><a href="#interview" style="display:inline-block;background:#1f1f1f;color:#fff;text-decoration:none;font:700 13px system-ui,sans-serif;padding:9px 16px;border-radius:8px" onclick="alert('Das Interview folgt. Die Fragen stehen oben; die Vorschläge werden daraus abgeleitet.');return false;">Interview starten</a> <span class="mono" style="display:inline;margin-left:8px">Knopf steht, Interview folgt.</span></p></div>"""))
# Fehlversuche
secs.append(('fehl', 'Fehlversuche', '<p>Bleiben stehen, neben der Korrektur.</p><table><tr><th>Zeile</th><th>Was</th><th>Warum</th></tr>' + ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (esc(f['id']), esc(f['was']), esc(f['warum'])) for f in D['fehlversuche']) + '</table>'))
# Blind
secs.append(('blind', 'Blind-Test', """
<p>Kontrolllauf B-0: derselbe Text, kein Figurenblatt. Ergebnis ein plausibler alter Kardinal. Philipp sah das Bild blind und sagte: nicht er. Daneben der Take mit Blatt und ein Interviewbild. Das Blatt kauft die Ähnlichkeit, die Worte kaufen den Typ.</p>
<figure style="max-width:960px"><img src="bilder/gh_B0_vs_B1v3_vs_interview_shot4.jpg" alt="Blind-Test" loading="lazy" onerror="this.parentNode.classList.add('missing')"><div class="pend">noch nicht geliefert<br><span class="mono">bilder/gh_B0_vs_B1v3_vs_interview_shot4.jpg</span></div><figcaption><b>H-003 · Kontrolle, Take mit Blatt, Interviewbild</b>Nur für Menschen, nie Bildeingabe.</figcaption></figure>"""))
# Quellen
qt = '<table><tr><th>ID</th><th>Datei</th><th>Art</th><th>Provenienz</th><th>Urheber · Lizenz</th><th>Erlaubt</th><th>Erzeugung</th><th>Lauf</th><th>Geprüft</th></tr>'
for r in rows:
    qt += '<tr><td>%s</td><td>%s<small>%s</small></td><td>%s<small>%s</small></td><td>%s</td><td>%s<small>%s</small></td><td>%s</td><td>%s</td><td>%s</td><td>%s<small>%s</small></td></tr>' % (
        esc(r['ID']), esc(r['Datei']), esc(r['SHA256']), esc(r['Art']), esc(r['Bedingung oder Nachweistext']), esc(r['Provenienz-Typ']), esc(r['Urheber']), esc(r['Lizenz']), esc(r['Erlaubt']), esc(r['Geht in die Erzeugung']), esc(r['Verwendet in Lauf']), esc(r['Gepruft von']), esc(r['Datum']))
qt += '</table>'
secs.append(('quellen', 'Quellenliste', '<p>Jedes Bild, das in einen Lauf geht oder einen Menschen bei der Arbeit leitet, hat eine Zeile, bevor es verwendet wird: Herkunft, Lizenz, ob es in die Erzeugung darf, wer es geprüft hat. %d Zeilen. Vollständig als <a href="quellen/Quellenliste.csv">CSV</a>, Felder und Regeln in der <a href="quellen/LIES_MICH_Quellenliste.md">LIES_MICH</a>.</p>' % len(rows) + qt))
# Offen
secs.append(('offen', 'Offen', '<ul>' + ''.join('<li>%s</li>' % esc(o) for o in D['offen']) + '</ul>'))

nav = ''.join('<a href="#%s">%s</a>' % (k, esc(t)) for k, t, _ in secs) + '<a href="archiv.html" style="background:#1f1f1f;color:#fff">Archiv (intern, Passwort)</a><span class="brand">FFP · GOLDENER HERBST 2026</span>'
body = ''.join('<section id="%s"><h2>%s</h2>%s</section>' % (k, esc(t), h) for k, t, h in secs)
banner = '' if D.get('freigabe_oeffentlich') else '<div class="banner"><b>Vorabfassung.</b> %s</div>' % esc(D.get('freigabe_hinweis', ''))
page = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Goldener Herbst 2026 — Reinraum-Fallstudie (FFP)</title><style>%s</style></head>
<body><nav>%s</nav><div class="wrap">
<p class="eyebrow">FFP · Goldener Herbst 2026 · Reinraum-Fallstudie · Stand %s</p>
<h1>Fremdmaterial ersetzen, ohne es zu kopieren</h1>
<p class="sub">Armin Müller-Stahl, die Einleitung: ein Test in zwei Teilen, 8. und 9. Oktober 2026. Wer das Original sieht, schreibt nur einen Brief. Wer erzeugt, sieht das Original nie.</p>
%s%s
<footer>F.F.P. Film &amp; Fernsehproduktion GmbH, Unterer Schreiberweg 29/5, A-1190 Wien, <a href="https://www.ffp.at">www.ffp.at</a> · powered by EmpiricaAI, <a href="https://www.getempirica.com">www.getempirica.com</a> · Keine Rechtsberatung. Seite gebaut von der Practice ffp-archive aus briefe/, quellen/ und daten/ergebnisse.json.</footer>
</div></body></html>""" % (CSS, nav, esc(D['stand']), banner, body)
with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(page)
print('index.html', len(page), 'bytes,', len(rows), 'Quellen,', len(D['takes']), 'Takes,', len(D['bilder']), 'Bilder')
