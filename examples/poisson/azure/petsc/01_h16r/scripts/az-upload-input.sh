#!/usr/bin/env zsh

sharename="fileshare"
dirname="poisson/petsc/001"
accountname="mesnardostorage"

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
casedir="$( cd "$(dirname "$scriptdir")" ; pwd -P )"

source ~/.zshrc

conda activate py36-az

az storage directory create \
	--name $dirname \
	--share-name $sharename \
	--account-name $accountname

cp -r $casedir/../config $casedir

az storage file upload-batch \
	--source $casedir \
	--destination $sharename/$dirname \
	--account-name $accountname

rm -rf $casedir/config

conda deactivate

exit 0
