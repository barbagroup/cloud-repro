#!/usr/bin/env bash
# Installs Batch Shipyard within conda environment.
# Creates a symbolink link in $HOME/.local/bin.
# CLI: ./shipyard-install.sh <path to Batch Shipyard directory>

pkgdir=$1
envname="py36-cloud"

cd $pkgdir
cat > get_shipyard_version.py <<- EOM
from convoy import version

if __name__ == "__main__":
    print(version.__version__)
EOM

version=$((python get_shipyard_version.py) 2>&1)
rm -f get_shipyard_version.py

bindir="$HOME/.local/bin"
execname="shipyard${version//./}"

source ~/.bashrc

#conda create --name $envname --yes python=3.6
conda activate $envname
conda install --yes pip
pip install --upgrade setuptools
pip uninstall -y azure-storage
pip install --upgrade -r requirements.txt
pip install --upgrade --no-deps -r req_nodeps.txt
conda deactivate

cat > $bindir/$execname <<- EOM
#!/usr/bin/env bash

source ~/.bashrc

set -e
set -f

BATCH_SHIPYARD_ROOT_DIR=$pkgdir

if [ -z \$BATCH_SHIPYARD_ROOT_DIR ]; then
    echo Batch Shipyard root directory not set.
    echo Please rerun the install.sh script.
    exit 1
fi

conda activate $envname
python3 \$BATCH_SHIPYARD_ROOT_DIR/shipyard.py \$*
conda deactivate
EOM

chmod +x $bindir/$execname
rm -f $bindir/shipyard
ln -s $bindir/$execname $bindir/shipyard

exit 0
