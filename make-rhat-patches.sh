#!/bin/bash

DISTGIT_PATH=$(pwd)

FEDORA_VERSION=rawhide
DOCKER_FEDORA_VERSION=master
DISTGIT_BRANCH=master

git checkout $DISTGIT_BRANCH -q

POLICYSOURCES=`mktemp -d policysources.XXXXXX`
pushd $POLICYSOURCES > /dev/null

git clone git@github.com:fedora-selinux/selinux-policy.git -q
git clone git@github.com:fedora-cloud/docker-selinux.git -q

pushd selinux-policy > /dev/null
# prepare policy patches against upstream commits matching the last upstream merge
git rev-parse --verify origin/${FEDORA_VERSION}-base; git diff eb4512f6eb13792c76ff8d3e6f2df3a7155db577 origin/${FEDORA_VERSION}-base > policy-${FEDORA_VERSION}-base.patch
git rev-parse --verify origin/${FEDORA_VERSION}-contrib; git diff 64302b790bf2b39d93610e1452c8361d56966ae0 origin/${FEDORA_VERSION}-contrib > policy-${FEDORA_VERSION}-contrib.patch
popd > /dev/null

pushd docker-selinux > /dev/null
git checkout -b ${DOCKER_FEDORA_VERSION} -t origin/${DOCKER_FEDORA_VERSION} -q
tar -czf docker-selinux.tgz docker.if docker.te docker.fc
popd > /dev/null

pushd $DISTGIT_PATH > /dev/null
cp $POLICYSOURCES/selinux-policy/policy-${FEDORA_VERSION}-{base,contrib}.patch .
cp $POLICYSOURCES/docker-selinux/docker-selinux.tgz .
popd > /dev/null

popd > /dev/null
rm -rf $POLICYSOURCES

echo "policy-rawhide-{contrib,base}.patches and docker.tgz with docker policy files have been created."
