# Reproducible workflow on a public cloud for computational fluid dynamics

* Olivier Mesnard (The George Washington University)
* Lorena A. Barba (The George Washington University)

## Dependencies

* Azure-CLI (last used: `2.0.57`)
* Batch Shipyard (`3.6.1`)
* petibmpy (`0.1`)

```bash
conda create --name py36-cloud python=3.6 pip
conda activate py36-cloud
pip install azure-cli==2.0.57
mkdir -p sfw/batch-shipyard/3.6.1
wget https://github.com/Azure/batch-shipyard/archive/3.6.1.tar.gz -C /tmp
tar -xzf /tmp/3.6.1.tar.gz -C sfw/batch-shipyard/3.6.1 --strip-components=1
./misc/shipyard-install.sh sfw/batch-shipyard/3.6.1
mkdir -p sfw/petibmpy/0.1
wget https://github.com/mesnardo/petibmpy/archive/0.1.tar.gz -C /tmp
tar -xzf /tmp/0.1.tar.gz -C sfw/petibmpy/0.1 --strip-components=1
cd sfw/petibmpy/0.1
conda env update --name=py36-cloud --file=environment.yaml
python setup.py develop
conda deactivate
```

## LICENSE

**Not all content in this repository is open source.** The Python code for creating the figures is shared under a BSD3 License. The written content in any Jupyter Notebooks is shared under a Creative Commons Attribution (CC-BY) license.
But please note that _the manuscript text is not open source;_ we reserve rights to the article content, which will be submitted for publication in a journal. Only fair use applies in this case.
