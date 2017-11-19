#!/bin/bash

# this variable should contain all the information about the root of the
# repository
REPO_ROOT="/repo/"
ARCHIVE_NAME="archive"
EXTENSION='.pkg.tar.xz'

if [ ! -e ${REPO_ROOT}/$ARCHIVE_NAME/ ]
then
    mkdir -vp ${REPO_ROOT}/${ARCHIVE_NAME}/os/x86_64
fi

# copy the old database and the old package-dependencies
cp ${REPO_ROOT}/os/x86_64/package-dependencies.txt{,.old}
mv data.json{,.old}

# update the dependency databases
for arch in core community extra 
do
    python dependency-report.py ${REPO_ROOT}/${arch}/os/x86_64/

    # run the diffing script to obtain the new packages and the old ones
    update-archive.py package-dependencies.txt{,.old} ${repo}

    # add all new packages
    while read new_package 
    do 
        cp ${REPO_ROOT}/${repo}/os/x86_64/${new_package}.*.${EXTENSION} ${REPO_ROOT}/${ARCHIVE_NAME}/
        cp ${REPO_ROOT}/${repo}/os/x86_64/${new_package}.*.${EXTENSION}.sig ${REPO_ROOT}/${ARCHIVE_NAME}/

        cd ${REPO_ROOT}/${repo}/os/x86_64/ && repo-add ${ARCHIVE_NAME}.db ${new_package} && cd -
    done < new-packages-${repo}.txt

    while read old_package
    do 
        cd ${REPO_ROOT}/${ARCHIVE_NAME}/os/x86_64/ && repo-remove -R && cd -
        rm ${REPO_ROOT}/${ARCHIVE_NAME}/os/x86_64/${old_package}.*.${EXTENSION}
        rm ${REPO_ROOT}/${ARCHIVE_NAME}/os/x86_64/${old_package}.*.${EXTENSION}.sig
    done < deleted-packages-${repo}.txt
done
