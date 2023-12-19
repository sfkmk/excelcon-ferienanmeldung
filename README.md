# Excel-Datenkonverter für Ferienanmeldungen

### Übersicht
Das Tool ist für die pädagogischen Fachkräfte an unseren Schulstandorten gedacht. Es transformiert die Ferienanmeldungen von Schülerinnen und Schülern aus einem vorgegebenen Excel-Format in ein übersichtlicheres, benutzerfreundliches Format. Diese Umwandlung erleichtert die Planung und Organisation der Betreuung während der Ferienzeiten.

### Funktionsweise
Das Skript liest Excel-Dateien aus einem festgelegten Eingabeverzeichnis (`./input`). Jede Datei wird bearbeitet, um die Daten in ein neues Format zu überführen, das die folgenden Informationen enthält:
- Name des Kindes
- Klasse
- Anwesenheitstage
- Besondere Betreuungsbedürfnisse (Frühdienst, Spätdienst)
- Anmerkungen zur Abholsituation (z.B., ob das Kind alleine geht)

Die transformierten Daten werden im Verzeichnis `./output` gespeichert.

### Installation und Nutzung
1. Stelle sicher, dass Python und `pandas` auf deinem System installiert sind.
2. Platziere die zu transformierenden Excel-Dateien im `./input`-Verzeichnis.
3. Führe `main.py` aus.
4. Überprüfe das `./output`-Verzeichnis für die transformierten Dateien.

### Anforderungen
- Python 3.x
- `pandas`-Bibliothek

### Unterstützung und Feedback
Bei Fragen oder Problemen wende dich bitte an Samuel (IT-Administrator). Feedback und Verbesserungsvorschläge sind immer willkommen.

### Hinweise
- Dieses Tool wurde speziell für unsere internen Anforderungen entwickelt. Eine Anpassung für andere Formate oder Anforderungen kann notwendig sein.
- Die Vertraulichkeit der Daten muss stets gewahrt bleiben. Stelle sicher, dass die Excel-Dateien sicher gehandhabt werden.

---

Entwickelt mit ❤️ von Samuel.