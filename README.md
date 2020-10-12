## Purpose

SELinux Fedora Policy is a large patch off the mainline. The [fedora-selinux/selinux-policy](https://github.com/selinux-policy/selinux-policy.git) makes Fedora Policy packaging more simple and transparent for developers, upstream developers and users. It is used for applying downstream Fedora fixes, for communication about proposed/committed changes, for communication with upstream and the community. It reflects upstream repository structure to make submitting patches to upstream easy.

## Structure

### github
On GitHub, we have two repositories (selinux-policy and selinux-policy-contrib ) for dist-git repository.

    $ cd selinux-policy
    $ git remote -v
    origin	git@github.com:fedora-selinux/selinux-policy.git (fetch)


    $ git branch -r
    origin/HEAD -> origin/master
    origin/f27
    origin/f28
    origin/master
    origin/rawhide

    $ cd selinux-policy-contrib
    $ git remote -v
    origin	git@github.com:fedora-selinux/selinux-policy-contrib.git (fetch)

    $ git branch -r
    origin/HEAD -> origin/master
    origin/f27
    origin/f28
    origin/master
    origin/rawhide

Note: _master_ branch on GitHub does not reflect master branch in dist-git. For this purpose, we created the _rawhide github branches in both selinux-policy and selinux-policy-contrib repositories.

### dist-git
Package sources in dist-git are generally composed from a _selinux-policy and _selinux-policy-contrib repository snapshots tarballs and from other config files.

## Build process

1. clone [fedora-selinux/selinux-policy](https://github.com/fedora-selinux/selinux-policy) repository

		$ cd ~/devel/github
		$ git clone git@github.com:fedora-selinux/selinux-policy.git
		$ cd selinux-policy

2. clone [fedora-selinux/selinux-policy-contrib](https://github.com/fedora-selinux/selinux-policy-contrib) repository

		$ cd ~/devel/github
		$ git clone git@github.com:fedora-selinux/selinux-policy-contrib.git
		$ cd selinux-policy-contrib

3. create, backport, cherry-pick needed changes to a particular branch and push them

4. clone **selinux-policy** dist-git repository

		$ cd ~/devel/dist-git
		$ fedpkg clone selinux-policy
		$ cd selinux-policy

4. Download the latest snaphots from selinux-policy and selinux-policy-contrib github repositories

        $ ./make-rhat-patches.sh

5. add changes to the dist-git repository, bump release, create a changelog entry, commit and push
6. build the package

         $ fedpkg build
