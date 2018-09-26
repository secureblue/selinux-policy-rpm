#!/bin/bash

DISTGIT_PATH=$(pwd)

FEDORA_VERSION=rawhide
DOCKER_FEDORA_VERSION=master
DISTGIT_BRANCH=master
REPO_SELINUX_POLICY=${REPO_SELINUX_POLICY:-https://github.com/fedora-selinux/selinux-policy}
REPO_SELINUX_POLICY_BRANCH=${REPO_SELINUX_POLICY_BRANCH:-$FEDORA_VERSION}
REPO_SELINUX_POLICY_CONTRIB=${REPO_SELINUX_POLICY_CONTRIB:-https://github.com/fedora-selinux/selinux-policy-contrib}
REPO_SELINUX_POLICY_CONTRIB_BRANCH=${REPO_SELINUX_POLICY_CONTRIB_BRANCH:-$FEDORA_VERSION}
REPO_CONTAINER_SELINUX=${REPO_CONTAINER_SELINUX:-https://github.com/containers/container-selinux}

# When -l is specified, we use locally created tarballs and don't download them from github
DOWNLOAD_DEFAULT_GITHUB_TARBALLS=1
if [ "$1" == "-l" ]; then
    DOWNLOAD_DEFAULT_GITHUB_TARBALLS=0
fi

git checkout $DISTGIT_BRANCH -q

POLICYSOURCES=`mktemp -d policysources.XXXXXX`
pushd $POLICYSOURCES > /dev/null

git clone -q $REPO_SELINUX_POLICY selinux-policy
git clone -q $REPO_SELINUX_POLICY_CONTRIB selinux-policy-contrib
git clone -q $REPO_CONTAINER_SELINUX container-selinux

pushd selinux-policy > /dev/null
# prepare policy patches against upstream commits matching the last upstream merge
git checkout $REPO_SELINUX_POLICY_BRANCH
BASE_HEAD_ID=$(git rev-parse HEAD)
BASE_SHORT_HEAD_ID=$(c=${BASE_HEAD_ID}; echo ${c:0:7})
git archive --prefix=selinux-policy-$BASE_HEAD_ID/ --format tgz HEAD > $DISTGIT_PATH/selinux-policy-$BASE_SHORT_HEAD_ID.tar.gz
popd > /dev/null

pushd selinux-policy-contrib > /dev/null
# prepare policy patches against upstream commits matching the last upstream merge
git checkout $REPO_SELINUX_POLICY_CONTRIB_BRANCH
CONTRIB_HEAD_ID=$(git rev-parse HEAD)
CONTRIB_SHORT_HEAD_ID=$(c=${CONTRIB_HEAD_ID}; echo ${c:0:7})
git archive --prefix=selinux-policy-contrib-$CONTRIB_HEAD_ID/ --format tgz HEAD > $DISTGIT_PATH/selinux-policy-contrib-$CONTRIB_SHORT_HEAD_ID.tar.gz
popd > /dev/null

pushd container-selinux > /dev/null
# Actual container-selinux files are in master branch
#git checkout -b ${DOCKER_FEDORA_VERSION} -t origin/${DOCKER_FEDORA_VERSION} -q
tar -czf container-selinux.tgz container.if container.te container.fc
popd > /dev/null

pushd $DISTGIT_PATH > /dev/null
if [ $DOWNLOAD_DEFAULT_GITHUB_TARBALLS == 1 ]; then
    wget -O selinux-policy-${BASE_SHORT_HEAD_ID}.tar.gz https://github.com/fedora-selinux/selinux-policy/archive/${BASE_HEAD_ID}.tar.gz &> /dev/null
    wget -O selinux-policy-contrib-${CONTRIB_SHORT_HEAD_ID}.tar.gz https://github.com/fedora-selinux/selinux-policy-contrib/archive/${CONTRIB_HEAD_ID}.tar.gz &> /dev/null
fi
cp $POLICYSOURCES/container-selinux/container-selinux.tgz .
popd > /dev/null

popd > /dev/null
rm -rf $POLICYSOURCES

# Update commit ids in selinux-policy.spec file
sed -i "s/%global commit0 [^ ]*$/%global commit0 $BASE_HEAD_ID/" selinux-policy.spec
sed -i "s/%global commit1 [^ ]*$/%global commit1 $CONTRIB_HEAD_ID/" selinux-policy.spec

# Update sources
sha512sum --tag selinux-policy-${BASE_SHORT_HEAD_ID}.tar.gz selinux-policy-contrib-${CONTRIB_SHORT_HEAD_ID}.tar.gz container-selinux.tgz > sources

echo -e "\nSELinux policy tarballs  and container.tgz with container policy files have been created."
echo "Commit ids of selinux-policy and selinux-policy-contrib in spec file were changed to:"
echo "commit0 " ${BASE_HEAD_ID}
echo "commit1 " ${CONTRIB_HEAD_ID}
