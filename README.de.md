[![pages-build-deployment](https://github.com/J0J0HA/test/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/J0J0HA/test/actions/workflows/pages/pages-build-deployment)
# AutoDocs
AutoDocs konvertiert ausgewählte `.md`-Dateien zu `.html`-Dateien und überträgt sie zusammen mit anderen ausgewählten Dateien in den /docs ordner von GitHub Pages.

## Beispiel
Dieses Repository enthält selbst den Workflow für AutoDocs.  
[Hier](https://j0j0ha.github.io/AutoDocs/README.de) kannst du die automatisch generierte `.html`-Datei online sehen.  
[Hier](https://j0j0ha.github.io/AutoDocs/README.en) findest du auch die automatisch generierte `.html`-Datei der englischen Version.  

## Setup
* Kopiere die Ordner `/autodocs` und `/sources` und die Datei `/.github/workflows/AutoDocs.yml` in dein eigenes Repository.
* Gehe in den Einstellungen deines Repositorys auf "Pages", und wähle unter "Source" "main" und "/docs" aus. Klicke anschließend auf "Save"
* Gehe nun in den Order `/autodocs` und bearbeite `config.yml` (siehe "Konfiguration" unten)
* Anschließend werden die Dateien unter `files:` in den (neu erstellten) Ordner /docs kopiert. `.md`-Dateien werden einmal als `.html`, einmal als `.md` gespeichert, falls du beabsichtigst, eine `.md`-Datei zum Download anzubieten (oder so).
* Durch den push sollte sich die GitHub Page von selbst anpassen. (evtl. Musst du den Cache deinen Browsers löschen und einige Minuten warten.)

## Konfiguration
Datei `config.yml`:
```
index: README.md                               # The md file to be shown at /  (optional)
scripts:                                       # list of js files to load      (optional)
  - sources/script.js
style:                                         # Container for styling         (optional)
  favicon: sources/favicon.png                 # Link to the favicon           (optional)
  load:                                        # list of css files to load     (optional)
    - sources/style.css                        
  themes:                                      # list of themes (name: link)   (optional)
    dark: sources/themes/dark.css
    light: sources/themes/light.css
  default theme: dark                          # default theme                 (optional)
folders:                                       # folders to create in docs     (required)
  - sources                                    # IMPORTANT: Lower level folders first
  - sources/themes
files:                                         # files to be included in /docs (required)
  - README.md                                  # You can use "*" for all files in the folder
  - README.de.md                               # or "**" for all sub folders and the files
  - README.en.md                               # tey conatin (recursive)
  - sources/**
```

Datei `template.html`:
> Diese Datei wird als Grundlage für die einzelnen Seiten genutzt. %extra% ist der generierte Zusatz durch `style` in der `config.yml`, %title% ist der Dateipfad und %content% ist der generierte HTML-Code selbst.
