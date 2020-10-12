## Purpose

SELinux Fedora Policy is a fork of the [SElinux reference policy](https://github.com/SELinuxProject/refpolicy/). The [fedora-selinux/selinux-policy](https://github.com/selinux-policy/selinux-policy.git) repo makes Fedora packaging simpler and more transparent for packagers, upstream developers, and users. It is used for applying downstream Fedora fixes, for communication about proposed/committed changes, and for communication with upstream and the community. It reflects the upstream repository structure to make submitting patches to upstream easy.

## Structure

### GitHub
On GitHub, we have two repositories (selinux-policy and selinux-policy-contrib) for dist-git repository.

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

Note: As opposed to dist-git, the Rawhide content in both selinux-policy and selinux-policy-contrib repositories resides in _rawhide_ branches rather than _master_.

### dist-git
Package sources in dist-git are composed from _selinux-policy_, _selinux-policy-contrib_, and _macro-expander_ repository snapshot tarballs, _container-selinux_ policy files snapshot, and from other config files.

## Build process

1. Clone the [fedora-selinux/selinux-policy](https://github.com/fedora-selinux/selinux-policy) repository.

        $ cd ~/devel/github
        $ git clone git@github.com:fedora-selinux/selinux-policy.git
        $ cd selinux-policy

2. Clone the [fedora-selinux/selinux-policy-contrib](https://github.com/fedora-selinux/selinux-policy-contrib) repository.

        $ cd ~/devel/github
        $ git clone git@github.com:fedora-selinux/selinux-policy-contrib.git
        $ cd selinux-policy-contrib

3. Create, backport, cherry-pick needed changes to a particular branch and push them.

4. Clone the **selinux-policy** dist-git repository.

        $ cd ~/devel/dist-git
        $ fedpkg clone selinux-policy
        $ cd selinux-policy

5. Download the latest snaphots from selinux-policy and selinux-policy-contrib github repositories.

        $ ./make-rhat-patches.sh

6. Add changes to the dist-git repository, bump release, create a changelog entry, commit and push.
7. Build the package.

        $ fedpkg build
