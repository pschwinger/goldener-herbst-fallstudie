# Quellenliste der Fallstudie Reinraum 2026

Jedes Bild, das in einen Erzeugungslauf geht oder einen Menschen bei der Arbeit leitet, bekommt eine Zeile, bevor es verwendet wird. Wer das Bild einbringt, schreibt die Zeile; ffp-archive fuehrt die Liste. Die Liste wird ein Abschnitt im Reiter Fallstudie und im PDF.

## Felder

- ID: fortlaufend je Vorsilbe. Q Quelle (Bild, Video, Text, Modell), R Regel, P Prompt-Element, M Mesh-Uebergabe, G erzeugtes Bild (Figurenblatt, Altersblatt, Testbild), V erzeugter Video-Take, H nur fuer Menschen (Vergleichsbilder, fremde Fotos), D Dokument (Ergebnisbericht, PDF).
- Datei: Dateiname oder Muster.
- SHA256: Pruefsumme der Datei, damit spaeter nachweisbar ist, welches Bild genau gemeint war.
- Art: Gesichtsquelle, Ortsreferenz, Stilreferenz, Erzeugt (Figurenblatt, Standbild, Clip).
- Provenienz-Typ, nach dem Muster aus Reevaluate (Olympia): eigenes Material / erzeugt aus eigenem Material / gemeinfrei / CC0 / CC-BY / nur fuer Menschen / erzeugt.
- Quelle: Pfad oder URL.
- Urheber, Lizenz, Abrufdatum.
- Erlaubt: ja / nein / ja, mit Bedingung.
- Bedingung oder Nachweistext: der Satz, der bei jeder Weiterverwendung mitreist (bei CC-BY der Credit; bei eigenem Material die Einwilligung).
- Geht in die Erzeugung: ja / nein. Nein heisst: nur Menschen sehen es (Stilreferenzen, Ortsbilder zum Vergleich).
- Verwendet in Lauf: Kennung des Erzeugungslaufs (kommt von imagegen oder videogen).
- Gepruft von, Datum.

## Regeln

1. Kein Bild aus ORF-Material, aus Kinofilmen oder aus der Sendung geht in die Erzeugung. Die Wand bleibt: Worte und das Figurenblatt aus eigenem Material.
2. Ortsreferenzen zuerst in Worten. Wenn Bilder, dann nur gemeinfrei oder CC0; CC-BY nur mit Nachweistext; nie CC-BY-SA (die Lizenz vererbt sich auf das Ergebnis), nie Stockbilder mit KI-Klausel, nie Pressefotos, nie Filmbilder.
3. Innenraeume des Vatikans werden erfunden, nicht nachgebaut.
4. Erzeugte Bilder bekommen ebenfalls eine Zeile (Art: Erzeugt) mit Verweis auf die Zeilen ihrer Eingaben.
5. Fehlschlaege bleiben in der Liste und werden nicht geloescht (Regel aus Reevaluate: der Fehlschlag steht neben der Korrektur).

- trainiertes Modell aus eigenem Material: ein Modell (z. B. Higgsfield Soul), das nur aus Zeilen mit eigenem Material trainiert wurde; eigene Zeile, Einwilligung muss das Training abdecken.
- Erzeugt: Figurenblaetter, Altersblaetter, Testbilder, Keyframes, Clips; immer mit Verweis auf die Zeilen ihrer Eingaben, Modell, Transport, Groesse, Lauf.
