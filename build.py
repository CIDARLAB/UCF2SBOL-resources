import os
import json
from glob import glob
import re

def merge_coll(x, y):
    z = {**x, **y}
    return z
    
distdir = "dist/"

if not os.path.isdir(distdir):
    os.mkdir(distdir)

lib = {}

files = glob("resources/Cello-UCF/files/v2/**/*.json", recursive=True)

for f in files:
    key = re.sub(".(UCF|input|output).json$", "", os.path.basename(f))
    if key not in lib:
        lib[key] = []
    lib[key].append(f)

for key in lib:
    output = []
    for f in lib[key]:
        with open(f) as fp:
            segment = json.load(fp)
        t = re.search("(UCF|input|output)", os.path.basename(f)).groups()[0]
        hint_glob = "resources/hint/files/v2/**/{}".format(os.path.basename(f))
        g = glob(hint_glob, recursive=True)
        if len(g) > 0:
            hint_file = g[0]
            with open(hint_file) as fp:
                hint = json.load(fp)
            for ref_coll in segment:
                z = ref_coll.copy()
                for coll in hint:
                    if ref_coll["collection"] == coll["collection"] and ref_coll["name"] == coll["name"]:
                        z = merge_coll(ref_coll, coll)
                        hint.remove(coll)
                        break
                output.append(z)
            output += hint
        else:
            output += segment
                    
    with open(distdir + key + ".SynBioHub.json", "w") as fp:
        json.dump(output, fp, indent=4)
