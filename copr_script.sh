#!/bin/sh -eux

LATEST_COMMIT=$(git ls-remote https://github.com/secureblue/selinux-policy.git refs/heads/f42-secureblue | awk '{print $1}')
SECUREBLUE_REPO_URL='https://github.com/secureblue/selinux-policy'

git clone https://src.fedoraproject.org/rpms/selinux-policy.git
cd ./selinux-policy
git checkout f42
sed --sandbox -i \
  -e "s|^%global giturl .*|%global giturl $SECUREBLUE_REPO_URL|" \
  -e "s/^%global commit .*/%global commit $LATEST_COMMIT/" \
  -e '/^Version: /s/$/_secureblue/' \
  selinux-policy.spec
for cil_policy_file in ./cil/*.cil; do
    policy_file_name=$(basename "$cil_policy_file")
    sed -i "/make clean/a semodule -v -i ${policy_file_name}"  selinux-policy.spec
done
cd ..

mv ./selinux-policy/* .
git clone https://github.com/fedora-selinux/macro-expander.git
mv ./macro-expander/macro-expander.sh ./macro-expander-bin
rm -rf ./macro-expander
mv ./macro-expander-bin ./macro-expander

git clone https://github.com/containers/container-selinux.git
cd container-selinux

find . -type f ! -name 'container.fc' ! -name 'container.if' ! -name 'container.te' -delete
find . -type d -empty -delete

tar -czvf container-selinux.tgz container.fc container.if container.te
mv container-selinux.tgz ..
cd ..

