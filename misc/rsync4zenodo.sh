#!/usr/bin/env bash
# Rsync data to be uploaded to Zenodo.

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
rootdir="$( cd "$(dirname "$scriptdir")" ; pwd -P )"

python $scriptdir/listfiles4zenodo.py

listpath=$scriptdir/files4zenodo.txt
destdir=$rootdir/zenodo

mkdir -p $destdir

rsync -av --files-from=$listpath $rootdir $destdir

rm -f $listpath

exit 0
