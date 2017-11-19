#!/usr/bin/env python3
import tarfile
import os
import glob
import pprint
import json
import sys

EXTENSION = "xz"

def read_buildinfo(path):
    if not os.path.exists(path) or not os.path.isfile(path):
        # XXX
        raise Exception("This is not a valid path!")

    with tarfile.open(path, "r:*") as fp:
        try:
            buildinfo = fp.extractfile(".BUILDINFO").read()
        except:
            #print("couldn't find .BULIDINFO for {}".format(path))
            return ""

    return buildinfo.decode()

def build_pkg_from_package_name(path):
    return os.path.basename(path).rsplit("-", 1)[0].lstrip("./")

def decode_buildinfo_lines(buildinfo):
    result = []

    # FIXME: what about epochs? we probably need to care about packages
    for line in buildinfo.splitlines():
        if line.startswith("installed"):
            pkg = line.split(" = ")[1]
            name, pkgver, pkgrel = pkg.rsplit("-", 2)
            result.append("{}-{}-{}".format(name, pkgver, pkgrel))

    return result

# XXX I opted for this ugly-looking dict update solution rather than something
# more pythonic/elegant for this first sketch. It'd make sense to use something
# smarter in the future...
def add_package_to_dict(pkgdict, package, dependent_package): 
    if package not in pkgdict:
        pkgdict[package] = [dependent_package]

    elif dependent_package not in pkgdict[package]:
        pkgdict[package].append(dependent_package)

def find_tarfiles(path = "."):
    return glob.glob(os.path.join(path, 
        "*.{}".format(EXTENSION)))

def main(path = ".", database_file = 'data.json'):

    try:
        with open('data.json') as fp:
            all_packages = json.load(fp)
    except Exception:
        all_packages = {}

    package_paths = find_tarfiles(path)

    for package_path in package_paths:
        buildinfo = read_buildinfo(package_path)
        thispackage = build_pkg_from_package_name(package_path)

        for package in decode_buildinfo_lines(buildinfo):
            add_package_to_dict(all_packages, package, thispackage)

    
    with open('data.json', 'wt') as fp:
        json.dump(all_packages, fp)

    with open("package-dependencies.txt", "wt") as fp:
        for line in all_packages.keys():
            fp.write("{}\n".format(line))

# FIXME: should populate a dictionary for fast lookup of all the package names,
# and versions
if __name__ == "__main__":
    path = "."
    if len(sys.argv) > 1:
        path = sys.argv[1]

    main(path)
