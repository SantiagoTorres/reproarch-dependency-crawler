#!/usr/bin/env python3
import sys

def diff_dependencies(new_list_filename, old_list_filename, repository):

    with open(new_list_filename) as fp:
        new_files = set(fp.read().split("\n"))

    with open(old_list_filename) as fp:
        old_files = set(fp.read().split("\n"))

    packages_to_remove = old_files - new_files
    packages_to_add = new_files - old_files

    with open("new-packages-{}".format(repository), "wt") as fp:
        for package in packages_to_add:
            fp.write("{}\n".format(package))


    with open("deleted-packages-{}".format(repository), "wt") as fp:
        for package in packages_to_remove:
            fp.write("{}\n".format(package))

if __name__ == "__main__":
    if len(sys.argv) > 3:
        new_list_filename = sys.argv[1]
        old_list_filename = sys.argv[2]
        repository = sys.argv[3]

    else:
        print("{} <new-list> <old-list> <repository-name>".format(sys.argv[0]))
        sys.exit(1)

    diff_dependencies(new_list_filename, old_list_filename, repository)
