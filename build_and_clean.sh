#!/bin/bash

# Kompilieren
latexmk -pdf -interaction=nonstopmode main.tex

# Nur wenn der Build erfolgreich war, dann löschen
if [ $? -eq 0 ]; then
    find . -type f \( -name '*.aux' -o -name '*.log' -o -name '*.toc' -o -name '*.bbl' -o -name '*.blg' -o -name '*.out' -o -name '*.fdb_latexmk' -o -name '*.fls' -o -name '*.synctex.gz' -o -name '*.run.xml' \) -delete
else
    echo "Build failed. Not cleaning up."
fi
