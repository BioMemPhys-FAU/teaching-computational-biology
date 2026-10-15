# Computational Biology: Moleküldynamik in 2D

Das deutschsprachige Notebook [MD_2D_Berendsen.ipynb](md_engine/MD_2D_Berendsen.ipynb) enthält eine eigenständige, kommentierte NumPy-Engine: Lennard-Jones-Paare, periodische Ränder, Velocity-Verlet, 2D-Berendsen-Thermostat und -Barostat, NumPy-Messreihen und einen eingebetteten HTML-Trajektorienplayer. Jupyter öffnen und **Run All** ausführen. Die Animation benötigt weder FFmpeg noch Widgets.

## Mit Binder starten

1. Diesen Projektordner mit `environment.yml` im Repository-Wurzelverzeichnis in ein öffentliches GitHub-Repository hochladen.
2. Auf [mybinder.org](https://mybinder.org) die Repository-URL und den gewünschten Branch, Tag oder Commit eintragen.
3. Als zu öffnenden Notebook-Pfad `md_engine/MD_2D_Berendsen.ipynb` wählen und den erzeugten Link teilen.
4. Für einen Kurs möglichst einen festen Commit oder Release-Tag verwenden. Vor der Veranstaltung einen echten Start samt **Run All** und Animation testen; der erste Image-Build kann länger dauern.

Link-Schema (OWNER, REPO und REF ersetzen):

```text
https://mybinder.org/v2/gh/OWNER/REPO/REF?labpath=md_engine%2FMD_2D_Berendsen.ipynb
```

`environment.yml` legt Python 3.14 sowie die lokal getesteten direkten Python-Abhängigkeiten fest. Binder stellt die Jupyter-Infrastruktur bereit. Das ist kein vollständiger Lock aller transitiven Abhängigkeiten. Ein Build und Browser-Test auf mybinder.org ist noch nicht erfolgt; es ist noch kein öffentliches Repository verknüpft.

**Studierende:** Binder speichert Änderungen nicht dauerhaft. Das bearbeitete Notebook und gegebenenfalls exportierte `.npz`-Daten vor dem Beenden herunterladen. Für längere Läufe lokal oder auf einem Hochschul-JupyterHub arbeiten. Die Standardeinstellungen sind für kurze interaktive Übungen gedacht; viele Teilchen erhöhen die Rechenkosten quadratisch.

## Lokal starten

Mit Conda oder Mamba:

```sh
conda env create -f environment.yml
conda activate teaching-computational-biology
python -m pip install jupyterlab
jupyter lab md_engine/MD_2D_Berendsen.ipynb
```

## Prüfung

```sh
python md_engine/validate_md.py
```

Die Tests prüfen Kraft gegen Potentialgradient, Impulserhaltung, periodische Invarianz, Virial, kinetischen Druck, Energieerhaltung ohne Regler, die 2D-Reglerschritte und konsistente Speicherung.

Vollständiger lokaler Notebook-Durchlauf am 15.10.2026 mit Python 3.14, NumPy 2.5.4 und Matplotlib 3.11.2: 12 000 Simulationsschritte mit 64 Teilchen in 9,61 s (ohne Animationserzeugung); 1 201 Messpunkte und 301 Trajektorienbilder. Player auf 160 Bilder begrenzt. Notebook mit Ausgaben ca. 3,4 MB. Die Laufzeit auf Binder kann abweichen. Relative Energiespanne im kurzen NVE-Test: 5,57 × 10⁻⁵. Alle Codezellen wurden erfolgreich in einem frischen Jupyter-Kernel ausgeführt; die HTML-Ausgabe wurde erzeugt.

Berendsen erzeugt keine korrekten kanonischen/isobar-isothermen Fluktuationen. Das Notebook erläutert diese Einschränkung und die 2D-Formeln; es ist ein Lehrmodell.

## Quellen für die Binder-Vorbereitung

- [The Turing Way: Zero-to-Binder](https://book.the-turing-way.org/communication/binder/zero-to-binder/)
- [repo2docker: environment.yml](https://repo2docker.readthedocs.io/en/latest/configuration/research/)
- [Binder: Ressourcen und Sitzungsgrenzen](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html)
