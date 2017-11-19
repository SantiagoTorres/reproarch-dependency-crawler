FROM santiagotorres/arch-base-devel

LABEL maintainer="Santiago Torres-Arias <santiago@archlinux.org>"

RUN pacman -Syyu --noconfirm python

# this script obtains a database file with the dependent packages
COPY dependency-report.py /

# this script diffs two database files and figure out which dependencies were
# added and which dependencies are no longer needed
COPY update-archive.py /

# this script basically does the following:
#  1) Run arch-repo-archive.py to obtain a new list of dependent packages
#  2) run update archive.py to figure out which packages need to be added and 
#     dropped
#  3) copy the new files to the archive and run repo-add 
COPY entrypoint.sh /

ENTRYPOINT entrypoint.sh
