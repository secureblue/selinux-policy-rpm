%define distro redhat
%define monolithic n
%define BUILD_STRICT 0
%define BUILD_TARGETED 0
%define BUILD_MLS 1
%define POLICYVER 20
%define POLICYCOREUTILSVER 1.29.26-1
%define CHECKPOLICYVER 1.29.4-1
Summary: SELinux policy configuration
Name: selinux-policy
Version: 2.2.19
Release: 3
License: GPL
Group: System Environment/Base
Source: serefpolicy-%{version}.tgz
patch: policy-20060207.patch
Source1: modules-targeted.conf
Source2: booleans-targeted.conf
Source4: setrans-targeted.conf
Source5: modules-mls.conf
Source6: booleans-mls.conf	
Source8: setrans-mls.conf
Source9: modules-strict.conf
Source10: booleans-strict.conf
Source12: setrans-strict.conf
Source13: policygentool

Url: http://serefpolicy.sourceforge.net
BuildRoot: %{_tmppath}/serefpolicy-buildroot
BuildArch: noarch
BuildRequires: checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils >= %{POLICYCOREUTILSVER}
PreReq: policycoreutils >= %{POLICYCOREUTILSVER}
Obsoletes: policy 

%description 
SELinux Base package

%files 
%{_mandir}/man8/*
%doc /usr/share/doc/%{name}-%{version}

%define setupCmds() \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} bare \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} conf \
cp -f ${RPM_SOURCE_DIR}/modules-%1.conf  ./policy/modules.conf \
cp -f ${RPM_SOURCE_DIR}/booleans-%1.conf ./policy/booleans.conf \

%define installCmds() \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} base.pp \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} modules \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=$RPM_BUILD_ROOT install \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=$RPM_BUILD_ROOT install-appconfig \
#%{__cp} *.pp $RPM_BUILD_ROOT/%{_usr}/share/selinux/%1/ \
%{__mkdir} -p $RPM_BUILD_ROOT/%{_sysconfdir}/selinux/%1/policy \
%{__mkdir} -p $RPM_BUILD_ROOT/%{_sysconfdir}/selinux/%1/modules/active \
%{__mkdir} -p $RPM_BUILD_ROOT/%{_sysconfdir}/selinux/%1/contexts/files \
touch $RPM_BUILD_ROOT/%{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
touch $RPM_BUILD_ROOT/%{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} enableaudit \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} base.pp \
install -m0644 base.pp ${RPM_BUILD_ROOT}%{_usr}/share/selinux/%1/enableaudit.pp \
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/booleans \
touch $RPM_BUILD_ROOT%{_sysconfdir}/selinux/config \
touch $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/selinux \
touch $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/seusers \
touch $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
touch $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
touch $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/contexts/files/homedir_template \
touch $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
install -m0644 ${RPM_SOURCE_DIR}/setrans-%1.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/selinux/%1/setrans.conf \
%nil

%define fileList() \
%defattr(-,root,root) \
%dir %{_usr}/share/selinux \
%dir %{_usr}/share/selinux/%1 \
%{_usr}/share/selinux/%1/*.pp \
%dir %{_sysconfdir}/selinux \
%ghost %config(noreplace) %{_sysconfdir}/selinux/config \
%ghost %{_sysconfdir}/sysconfig/selinux \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %{_sysconfdir}/selinux/%1/setrans.conf \
%ghost %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/modules \
%{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
%{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
%attr(700,root,root) %dir %{_sysconfdir}/selinux/%1/modules/active \
#%verify(not md5 size mtime) %attr(600,root,root) %config(noreplace) %{_sysconfdir}/selinux/%1/modules/active/seusers \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%ghost %{_sysconfdir}/selinux/%1/policy/policy.* \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/customizable_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/dbus_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/default_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_type \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/failsafe_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/initrc_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/removable_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/userhelper_context \
%dir %{_sysconfdir}/selinux/%1/contexts/files \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/homedir_template \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
%config %{_sysconfdir}/selinux/%1/contexts/files/media

%define saveFileContext() \
if [ -s /etc/selinux/config ]; then \
	. %{_sysconfdir}/selinux/config; \
	FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
	if [ "${SELINUXTYPE}" == %1 -a -f ${FILE_CONTEXT} ]; then \
		cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.pre; \
	fi \
fi

%define rebuildpolicy() \
( cd /usr/share/selinux/%1; \
x=`ls | grep -v -e base.pp -e enableaudit.pp | awk '{ print "-i " $1 }'`; \
semodule -b base.pp $x -s %1; \
);\
rm -f %{_sysconfdir}/selinux/%1/policy/policy.*.rpmnew

%define relabel() \
. %{_sysconfdir}/selinux/config; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
if [ "${SELINUXTYPE}" == %1 -a -f ${FILE_CONTEXT}.pre ]; then \
	fixfiles -C ${FILE_CONTEXT}.pre restore; \
	rm -f ${FILE_CONTEXT}.pre; \
fi; 

%description
SELinux Reference Policy - modular.

%prep 
%setup -q -n serefpolicy-%{version}
%patch0 -p1 
	
%install
# Build targeted policy
%{__rm} -fR $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8/
install -m 644 man/man8/*.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/

# Build targeted policy
# Commented out because only targeted ref policy currently builds
%setupCmds targeted targeted-mcs y
%installCmds targeted targeted-mcs y

# Build strict policy
# Commented out because only targeted ref policy currently builds
make NAME=strict TYPE=strict-mcs DISTRO=%{distro} DIRECT_INITRC=y MONOLITHIC=%{monolithic} bare 
make NAME=strict TYPE=strict-mcs DISTRO=%{distro} DIRECT_INITRC=y MONOLITHIC=%{monolithic} conf
%installCmds strict strict-mcs y

# Build mls policy
%setupCmds mls strict-mls n
%installCmds mls strict-mls n

# Install devel
make clean
make 
make DESTDIR=$RPM_BUILD_ROOT PKGNAME=%{name}-%{version} install-headers install-docs
install -m 755 ${RPM_SOURCE_DIR}/policygentool ${RPM_BUILD_ROOT}/usr/share/selinux/refpolicy/
install -m 755 doc/Makefile.example ${RPM_BUILD_ROOT}/usr/share/selinux/refpolicy/Makefile


%clean
%{__rm} -fR $RPM_BUILD_ROOT

%package targeted
Summary: SELinux targeted base policy
Group: System Environment/Base
Provides: selinux-policy-base
Obsoletes: selinux-policy-targeted-sources
Prereq: policycoreutils >= %{POLICYCOREUTILSVER}
Prereq: coreutils
Prereq: selinux-policy = %{version}-%{release}

%description targeted
SELinux Reference policy targeted base module.

%files targeted
%fileList targeted

%pre targeted
%saveFileContext targeted

%post targeted
if [ ! -s /etc/selinux/config ]; then
	#
	#	New install so we will default to targeted policy
	#
	echo "
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#	enforcing - SELinux security policy is enforced.
#	permissive - SELinux prints warnings instead of enforcing.
#	disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of these two values:
#	targeted - Only targeted network daemons are protected.
#	strict - Full SELinux protection.
#	mls - Multi Level Security protection.
SELINUXTYPE=targeted 
# SETLOCALDEFS= Check local definition changes
SETLOCALDEFS=0 

" > /etc/selinux/config

	ln -sf ../selinux/config /etc/sysconfig/selinux 
	restorecon /etc/selinux/config 2> /dev/null
else
	# if first time update booleans.local needs to be copied to sandbox
	[ -f /etc/selinux/targeted/booleans.local ] && mv /etc/selinux/targeted/booleans.local /etc/selinux/targeted/modules/active/
	[ -f /etc/selinux/targeted/seusers ] && cp -f /etc/selinux/targeted/seusers /etc/selinux/targeted/modules/active/seusers
	grep -q "^SETLOCALDEFS" /etc/selinux/config || echo -n "
# SETLOCALDEFS= Check local definition changes
SETLOCALDEFS=0 
">> /etc/selinux/config
fi
%rebuildpolicy targeted
%relabel targeted

%triggerpostun targeted -- selinux-policy-targeted <= 2.0.7
%rebuildpolicy targeted

%package mls 
Summary: SELinux mls base policy
Group: System Environment/Base
Provides: selinux-policy-base
Obsoletes: selinux-policy-mls-sources
Prereq: policycoreutils >= %{POLICYCOREUTILSVER}
Prereq: coreutils
Prereq: selinux-policy = %{version}-%{release}

%description mls 
SELinux Reference policy mls base module.

%pre mls 
%saveFileContext mls

%post mls 
%rebuildpolicy mls 
%relabel mls

%triggerpostun mls -- mls <= 2.0.7
%{rebuildpolicy} mls 

%files mls
%fileList mls

%package strict 
Summary: SELinux strict base policy
Group: System Environment/Base
Provides: selinux-policy-base
Obsoletes: selinux-policy-strict-sources
Prereq: policycoreutils >= %{POLICYCOREUTILSVER}
Prereq: coreutils
Prereq: selinux-policy = %{version}-%{release}

%description strict 
SELinux Reference policy strict base module.

%pre strict 
%saveFileContext strict

%post strict 
%rebuildpolicy strict 
%relabel strict

%triggerpostun strict -- strict <= 2.0.7
%{rebuildpolicy} strict 

%files strict
%fileList strict

%package devel
Summary: SELinux policy devel sources
Group: System Environment/Base
Prereq: checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils >= %{POLICYCOREUTILSVER} make
Prereq: selinux-policy = %{version}-%{release}

%description devel
SELinux Reference policy development files

%files devel
%defattr(-,root,root) 
%dir %{_usr}/share/selinux/refpolicy
%dir %{_usr}/share/selinux/refpolicy/include
%{_usr}/share/selinux/refpolicy/include/*
%{_usr}/share/selinux/refpolicy/Makefile
%{_usr}/share/selinux/refpolicy/policygentool

%changelog

* Wed Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.19-3
- Fix load_policy to work on MLS
- Fix cron_rw_system_pipes for postfix_postdrop_t
- Allow audotmount to run showmount

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.19-2
- Fix swapon
- allow httpd_sys_script_t to be entered via a shell
- Allow httpd_sys_script_t to read eventpolfs

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.19-1
- Update from upstream

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.18-2
- allow cron to read apache files

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.18-1
- Fix vpnc policy to work from NetworkManager

* Mon Feb 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.17-2
- Update to upstream
- Fix semoudle polcy

* Thu Feb 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.16-1
- Update to upstream 
- fix sysconfig/selinux link

* Wed Feb 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-4
- Add router port for zebra
- Add imaze port for spamd
- Fixes for amanda and java

* Tue Feb 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-3
- Fix bluetooth handling of usb devices
- Fix spamd reading of ~/
- fix nvidia spec

* Tue Feb 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-1
- Update to upsteam

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.14-2
- Add users_extra files

* Fri Feb 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.14-1
- Update to upstream

* Fri Feb 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.13-1
- Add semodule policy

* Tue Feb 7 2006 Dan Walsh <dwalsh@redhat.com> 2.2.12-1
- Update from upstream


* Mon Feb 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.11-2
- Fix for spamd to use razor port

* Fri Feb 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.11-1
- Fixes for mcs
- Turn on mount and fsadm for unconfined_t

* Wed Feb 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.10-1
- Fixes for the -devel package

* Wed Feb 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.9-2
- Fix for spamd to use ldap

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.9-1
- Update to upstream

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.8-2
- Update to upstream
- Fix rhgb, and other Xorg startups

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.7-1
- Update to upstream

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-3
- Separate out role of secadm for mls

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-2
- Add inotifyfs handling

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-1
- Update to upstream
- Put back in changes for pup/zen

* Tue Jan 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.5-1
- Many changes for MLS 
- Turn on strict policy

* Mon Jan 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.4-1
- Update to upstream

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.3-1
- Update to upstream
- Fixes for booting and logging in on MLS machine

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.2-1
- Update to upstream
- Turn off execheap execstack for unconfined users
- Add mono/wine policy to allow execheap and execstack for them
- Add execheap for Xdm policy

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.1-1
- Update to upstream
- Fixes to fetchmail,

* Tue Jan 17 2006 Dan Walsh <dwalsh@redhat.com> 2.1.13-1
- Update to upstream

* Tue Jan 17 2006 Dan Walsh <dwalsh@redhat.com> 2.1.12-3
- Fix for procmail/spamassasin
- Update to upstream
- Add rules to allow rpcd to work with unlabeled_networks.

* Sat Jan 14 2006 Dan Walsh <dwalsh@redhat.com> 2.1.11-1
- Update to upstream
- Fix ftp Man page

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 2.1.10-1
- Update to upstream

* Wed Jan 11 2006 Jeremy Katz <katzj@redhat.com> - 2.1.9-2
- fix pup transitions (#177262)
- fix xen disks (#177599)

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 2.1.9-1
- Update to upstream

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-3
- More Fixes for hal and readahead

* Mon Jan 9 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-2
- Fixes for hal and readahead

* Mon Jan 9 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-1
- Update to upstream
- Apply 
* Fri Jan 7 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-4
- Add wine and fix hal problems

* Thu Jan 6 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-3
- Handle new location of hal scripts

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-2
- Allow su to read /etc/mtab

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-1
- Update to upstream

* Tue Jan 3 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-24
- Fix  "libsemanage.parse_module_headers: Data did not represent a module." problem

* Tue Jan 3 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-23
- Allow load_policy to read /etc/mtab

* Mon Jan 2 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-22
- Fix dovecot to allow dovecot_auth to look at /tmp

* Mon Jan 2 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-21
- Allow restorecon to read unlabeled_t directories in order to fix labeling.

* Fri Dec 30 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-20
- Add Logwatch policy

* Wed Dec 28 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-18
- Fix /dev/ub[a-z] file context

* Tue Dec 27 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-17
- Fix library specification
- Give kudzu execmem privs

* Thu Dec 22 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-16
- Fix hostname in targeted policy

* Wed Dec 21 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-15
- Fix passwd command on mls

* Wed Dec 21 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-14
- Lots of fixes to make mls policy work

* Tue Dec 20 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-13
- Add dri libs to textrel_shlib_t
- Add system_r role for java
- Add unconfined_exec_t for vncserver
- Allow slapd to use kerberos

* Mon Dec 19 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-11
- Add man pages

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-10
- Add enableaudit.pp

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-9
- Fix mls policy

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-8
- Update mls file from old version

* Thu Dec 15 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-5
- Add sids back in
- Rebuild with update checkpolicy

* Thu Dec 15 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-4
- Fixes to allow automount to use portmap
- Fixes to start kernel in s0-s15:c0.c255

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-3
- Add java unconfined/execmem policy 

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-2
- Add file context for /var/cvs
- Dontaudit webalizer search of homedir

* Tue Dec 13 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-1
- Update from upstream

* Tue Dec 13 2005 Dan Walsh <dwalsh@redhat.com> 2.1.4-2
- Clean up spec
- range_transition crond to SystemHigh

* Mon Dec 12 2005 Dan Walsh <dwalsh@redhat.com> 2.1.4-1
- Fixes for hal
- Update to upstream

* Mon Dec 12 2005 Dan Walsh <dwalsh@redhat.com> 2.1.3-1
- Turn back on execmem since we need it for java, firefox, ooffice
- Allow gpm to stream socket to itself

* Mon Dec 12 2005 Jeremy Katz <katzj@redhat.com> - 2.1.2-3
- fix requirements to be on the actual packages so that policy can get
  created properly at install time

* Sun Dec  10 2005 Dan Walsh <dwalsh@redhat.com> 2.1.2-2
- Allow unconfined_t to execmod texrel_shlib_t

* Sat Dec  9 2005 Dan Walsh <dwalsh@redhat.com> 2.1.2-1
- Update to upstream 
- Turn off allow_execmem and allow_execmod booleans
- Add tcpd and automount policies

* Fri Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-3
- Add two new httpd booleans, turned off by default
	* httpd_can_network_relay
	* httpd_can_network_connect_db

* Fri Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-2
- Add ghost for policy.20

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-1
- Update to upstream
- Turn off boolean allow_execstack

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-3
- Change setrans-mls to use new libsetrans
- Add default_context rule for xdm

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-2.
- Change Requires to PreReg for requiring of policycoreutils on install

* Wed Dec  7 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-1.
- New upstream release

* Wed Dec  7 2005 Dan Walsh <dwalsh@redhat.com> 2.0.11-2.
Add xdm policy

* Tue Dec  6 2005 Dan Walsh <dwalsh@redhat.com> 2.0.11-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.9-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.8-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.7-3
- Also trigger to rebuild policy for versions up to 2.0.7.

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 2.0.7-2
- No longer installing policy.20 file, anaconda handles the building of the app.

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 2.0.6-2
- Fixes for dovecot and saslauthd

* Wed Nov 23 2005 Dan Walsh <dwalsh@redhat.com> 2.0.5-4
- Cleanup pegasus and named 
- Fix spec file
- Fix up passwd changing applications

* Tue Nov 21 2005 Dan Walsh <dwalsh@redhat.com> 2.0.5-1
-Update to latest from upstream

* Tue Nov 21 2005 Dan Walsh <dwalsh@redhat.com> 2.0.4-1
- Add rules for pegasus and avahi

* Mon Nov 21 2005 Dan Walsh <dwalsh@redhat.com> 2.0.2-2
- Start building MLS Policy

* Fri Nov 18 2005 Dan Walsh <dwalsh@redhat.com> 2.0.2-1
- Update to upstream

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 2.0.1-2
- Turn on bash

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 2.0.1-1
- Initial version
