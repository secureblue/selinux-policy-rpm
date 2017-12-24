#!/bin/bash

DISTGIT_PATH=$(pwd)

FEDORA_VERSION=rawhide
DOCKER_FEDORA_VERSION=master
DISTGIT_BRANCH=master

git checkout $DISTGIT_BRANCH -q

POLICYSOURCES=`mktemp -d policysources.XXXXXX`
pushd $POLICYSOURCES > /dev/null

git clone git@github.com:fedora-selinux/selinux-policy.git -q
git clone git@github.com:fedora-selinux/selinux-policy-contrib.git -q
git clone git@github.com:projectatomic/container-selinux.git -q

pushd selinux-policy > /dev/null
# prepare policy patches against upstream commits matching the last upstream merge
git checkout $FEDORA_VERSION
BASE_HEAD_ID=$(git rev-parse HEAD)
BASE_SHORT_HEAD_ID=$(c=${BASE_HEAD_ID}; echo ${c:0:7})
popd > /dev/null

pushd selinux-policy-contrib > /dev/null
# prepare policy patches against upstream commits matching the last upstream merge
git checkout $FEDORA_VERSION
CONTRIB_HEAD_ID=$(git rev-parse HEAD)
CONTRIB_SHORT_HEAD_ID=$(c=${CONTRIB_HEAD_ID}; echo ${c:0:7})
popd > /dev/null

pushd container-selinux > /dev/null
# Actual container-selinux files are in master branch
#git checkout -b ${DOCKER_FEDORA_VERSION} -t origin/${DOCKER_FEDORA_VERSION} -q
tar -czf container-selinux.tgz container.if container.te container.fc
popd > /dev/null

pushd $DISTGIT_PATH > /dev/null
wget -nc https://github.com/fedora-selinux/selinux-policy/archive/${BASE_HEAD_ID}/selinux-policy-${BASE_SHORT_HEAD_ID}.tar.gz &> /dev/null
wget -nc https://github.com/fedora-selinux/selinux-policy-contrib/archive/${CONTRIB_HEAD_ID}/selinux-policy-contrib-${CONTRIB_SHORT_HEAD_ID}.tar.gz &> /dev/null
cp $POLICYSOURCES/container-selinux/container-selinux.tgz .
popd > /dev/null

popd > /dev/null
rm -rf $POLICYSOURCES

echo -e "\nSELinux policy tarballs  and container.tgz with container policy files have been created."
echo "Replace commit ids of selinux-policy and selinux-policy-contrib in spec file to:"
echo "commit0 " ${BASE_HEAD_ID}
echo "commit1 " ${CONTRIB_HEAD_ID}
