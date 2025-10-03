#! /bin/sh -x 

mv ./selinux-policy-rpm/* .
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

