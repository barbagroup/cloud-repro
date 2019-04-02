"""Build the list of files to rsync for the Zenodo repository."""

import pathlib


scriptdir = pathlib.Path(__file__).absolute().parent
rootdir = scriptdir.parent

excludes = ['.git', '.vscode', '__pycache__',
            '.xmf', '.pyc',
            'credentials.yaml', 'id_rsa', 'l_mpi_2017.2.174.tgz']

filepath = scriptdir / 'files4zenodo.txt'
with open(filepath, 'w') as outfile:
    filepaths = rootdir.rglob('*')
    filepaths = [p for p in filepaths if not p.is_dir()]
    filepaths = [p for p in filepaths
                 if not any(s in p.as_posix() for s in excludes)]
    zenodos = [p for p in filepaths if '.zenodo' in p.name]
    for zenodo in zenodos:
        parent = zenodo.parent
        filepaths = [p for p in filepaths
                     if parent.as_posix() not in p.as_posix()]
        with open(zenodo, 'r') as infile:
            lines = infile.readlines()
            for line in lines:
                path2 = parent / line.strip()
                if path2.is_dir():
                    filepaths.extend(path2.rglob('*'))
                else:
                    filepaths.append(path2)
    filepaths = [p for p in filepaths if '/zenodo/' not in p.as_posix()]
    filepaths = [p for p in filepaths
                 if not any(s in p.as_posix() for s in excludes)]
    filepaths = [str(p.relative_to(rootdir)) + '\n' for p in filepaths]
    outfile.writelines(filepaths)
