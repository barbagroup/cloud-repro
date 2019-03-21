#!/usr/bin/env bash
# Clean LaTeX-generated files.

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $scriptdir
rm -f *.aux *.blg *.fdb_latexmk *.fls *.log *.synctex.gz

exit 0
