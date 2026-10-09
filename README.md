# Goldener Herbst 2026 — Reinraum-Fallstudie (FFP)

Statische Seite: Fremdmaterial ersetzen, ohne es zu kopieren. Beispiel Armin Müller-Stahl, Einleitung.

- `index.html` wird von der Practice **ffp-archive** aus `build/build_index.py` gebaut (Quellen: `briefe/`, `quellen/`, `daten/ergebnisse.json`). Neu bauen: `python3 build/build_index.py`.
- `en.html` ist die englische Seite (Knopf Deutsch | English oben). Englische Texte: `daten/ergebnisse.en.json` (je ID, nur Texte; Zahlen, Dateien und Status stehen einmal in `ergebnisse.json`) und `briefe/en/` (Übersetzungen; `briefe/` bleibt das Original). Beide Seiten baut `python3 build/build_index.py`. Pflegt storyboard.
- `videos/` und `bilder/` liefern **storyboard / videogen / imagegen** (siehe die LIES_MICH dort). `daten/ergebnisse.json` darf storyboard fortschreiben; danach neu bauen.
- Kein ORF-Material, keine Filmbilder, nichts von der Analystenseite. Nur Worte, eigenes Material und Erzeugnisse.
- Öffentlich auf GitHub Pages seit 09.10.2026 (Entscheidung Philipp Schwinger): https://pschwinger.github.io/goldener-herbst-fallstudie/ — die schriftliche Einwilligung wird nachgereicht (Q-012).
- `archiv.html` ist der Archivbereich (offen, ohne Passwort seit 09.10.2026 15:25, Entscheidung Philipp Schwinger): Archivsuche, Interviews, das Original. **Für die erzeugenden Practices (storyboard, imagegen, videogen) tabu** — Reinraum-Wand. `archiv.html`, `quellen/Quellenliste.csv` und `briefe/` pflegt nur ffp-archive.

F.F.P. Film & Fernsehproduktion GmbH, Wien · powered by EmpiricaAI
