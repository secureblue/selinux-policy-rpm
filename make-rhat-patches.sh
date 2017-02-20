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
git rev-parse --verify origin/${FEDORA_VERSION}; git diff eb4512f6eb13792c76ff8d3e6f2df3a7155db577 origin/${FEDORA_VERSION} > policy-${FEDORA_VERSION}-base.patch
popd > /dev/null

pushd selinux-policy-contrib > /dev/null
# prepare policy patches against upstream commits matching the last upstream merge
git rev-parse --verify origin/${FEDORA_VERSION}; git diff 64302b790bf2b39d93610e1452c8361d56966ae0 origin/${FEDORA_VERSION} > policy-${FEDORA_VERSION}-contrib.patch
popd > /dev/null

pushd container-selinux > /dev/null
# Actual container-selinux files are in master branch
#git checkout -b ${DOCKER_FEDORA_VERSION} -t origin/${DOCKER_FEDORA_VERSION} -q
tar -czf container-selinux.tgz container.if container.te container.fc
popd > /dev/null

pushd $DISTGIT_PATH > /dev/null
cp $POLICYSOURCES/selinux-policy/policy-${FEDORA_VERSION}-base.patch .
cp $POLICYSOURCES/selinux-policy-contrib/policy-${FEDORA_VERSION}-contrib.patch .
cp $POLICYSOURCES/container-selinux/container-selinux.tgz .
popd > /dev/null

popd > /dev/null
rm -rf $POLICYSOURCES

echo "policy-rawhide-{contrib,base}.patches and container.tgz with container policy files have been created."
