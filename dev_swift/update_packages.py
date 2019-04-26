from pathlib import Path
import os, shutil

path = Path.cwd()
packages = []
for x in path.iterdir(): 
    if x.is_dir() and x.name.startswith("FastaiNotebook"): packages.append(x)
packages.sort()
for i,p in enumerate(packages):
    fname = '_'.join(p.name.split('_')[1:])
    source = (p/"Sources"/p.name/fname).with_suffix('.swift')
    for p1 in packages[i+1:]:
        dest = (p1/"Sources"/p1.name/fname).with_suffix('.swift')
        try: shutil.copy(source, dest)
        except shutil.SameFileError:
            pass