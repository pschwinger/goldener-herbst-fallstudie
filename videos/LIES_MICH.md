# videos/ — Lieferung durch storyboard / videogen

Dateinamen genau wie in der Quellenliste (Spalte Datei, ohne `_RAW`):

| Zeile | Datei hier | Inhalt |
|---|---|---|
| V-001 | gh_A1_full.mp4 | Test A, fotoreal, Take 1 (ersetzt, bleibt als Fehlversuch) |
| V-002 | gh_A1_v4_full.mp4 | Test A, fotoreal, Take 2 |
| V-003 | gh_A2_full.mp4 | Test A, 3D-Stil |
| V-004 | gh_B1_full.mp4 | Test B, fotoreal, Take 1 (ersetzt, bleibt als Fehlversuch) |
| V-005 | gh_B1_v3_full.mp4 | Test B, fotoreal, Take 2 |
| V-006 | gh_B2_full.mp4 | Test B, 3D-Stil |
| V-007 | gh_B0_full.mp4 | Test B, Kontrolle ohne Figurenblatt |

Dazu je Take, gleicher Stamm: `<stamm>_kontakt.jpg` (Kontaktbogen), `<stamm>.prompt.txt` (Prompt wie gefeuert), `<stamm>.ledger.json`.

## Encoding (GitHub: 100 MB je Datei, Pages liefert kein LFS)

    ffmpeg -i IN.mp4 -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 23 -preset slow -vf "scale=1920:-2" -an -movflags +faststart OUT.mp4

- Ziel unter 95 MB je Datei. Wird eine Montage größer: `-crf 26` oder `scale=1280:-2`.
- Kein Ton (es gibt keinen; keine synthetische Stimme).
- Prüfsumme (`shasum -a 256`, erste 16 Zeichen) in die Zeile der Quellenliste; ffp-archive prüft vor dem Einbau.

Die Seite (`index.html`) zeigt jede Datei, sobald sie hier liegt; fehlt sie, steht „noch nicht geliefert".
