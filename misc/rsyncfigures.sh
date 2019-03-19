#!/usr/bin/env bash
# Rsync figures for manuscript.

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
rootdir="$( cd "$(dirname "$scriptdir")" ; pwd -P )"

listpath="$scriptdir/rsyncfigureslist.txt"
destdir="$rootdir/tex/figures/"

mkdir -p $destdir

rsync -av --no-relative --files-from=$listpath $rootdir $destdir

exit 0
