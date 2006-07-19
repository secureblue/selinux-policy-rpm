%define distro redhat
%define polyinstatiate n
%define monolithic n
%if %{?BUILD_STRICT:0}%{!?BUILD_STRICT:1}
%define BUILD_STRICT 1
%endif
%if %{?BUILD_TARGETED:0}%{!?BUILD_TARGETED:1}
%define BUILD_TARGETED 1
%endif
%if %{?BUILD_MLS:0}%{!?BUILD_MLS:1}
%define BUILD_MLS 1
%endif
%define POLICYVER 20
%define POLICYCOREUTILSVER 1.30.14-3
%define CHECKPOLICYVER 1.30.4-1
Summary: SELinux policy configuration
Name: selinux-policy
Version: 2.3.3
Release: 5
License: GPL
Group: System Environment/Base
Source: serefpolicy-%{version}.tgz
patch: policy-20060608.patch
Source1: modules-targeted.conf
Source2: booleans-targeted.conf
Source3: Makefile.devel
Source4: setrans-targeted.conf
Source5: modules-mls.conf
Source6: booleans-mls.conf	
Source8: setrans-mls.conf
Source9: modules-strict.conf
Source10: booleans-strict.conf
Source12: setrans-strict.conf
Source13: policygentool

Url: http://serefpolicy.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils >= %{POLICYCOREUTILSVER}
PreReq: policycoreutils >= %{POLICYCOREUTILSVER}
Obsoletes: policy 

%description 
SELinux Base package

%files 
%{_mandir}/man8/*
%doc %{_usr}/share/doc/%{name}-%{version}
%dir %{_usr}/share/selinux
%dir %{_sysconfdir}/selinux
%ghost %config(noreplace) %{_sysconfdir}/selinux/config
%ghost %{_sysconfdir}/sysconfig/selinux

%package devel
Summary: SELinux policy development
Group: System Environment/Base
Prereq: checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils >= %{POLICYCOREUTILSVER}
Prereq: selinux-policy = %{version}-%{release}

%description devel
SELinux Policy development package

%files devel
%dir %{_usr}/share/selinux/devel
%dir %{_usr}/share/selinux/devel/include
%{_usr}/share/selinux/devel/include/*
%{_usr}/share/selinux/devel/Makefile
%{_usr}/share/selinux/devel/policygentool
%{_usr}/share/selinux/devel/example.*
%attr(755,root,root) %{_usr}/share/selinux/devel/policyhelp

%define setupCmds() \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%3 bare \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%3  conf \
cp -f ${RPM_SOURCE_DIR}/modules-%1.conf  ./policy/modules.conf \
cp -f ${RPM_SOURCE_DIR}/booleans-%1.conf ./policy/booleans.conf \

%define installCmds() \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%3 base.pp \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%3 modules \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%3 install \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%3 install-appconfig \
#%{__cp} *.pp %{buildroot}/%{_usr}/share/selinux/%1/ \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/policy \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/modules/active \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/contexts/files \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%3  enableaudit \
make -W base.conf NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%3 base.pp \
install -m0644 base.pp %{buildroot}%{_usr}/share/selinux/%1/enableaudit.pp \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/booleans \
touch %{buildroot}%{_sysconfdir}/selinux/%1/seusers \
touch %{buildroot}%{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/homedir_template \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
install -m0644 ${RPM_SOURCE_DIR}/setrans-%1.conf %{buildroot}%{_sysconfdir}/selinux/%1/setrans.conf \
ln -sf ../devel/include %{buildroot}%{_usr}/share/selinux/%1 \
%nil

%define fileList() \
%defattr(-,root,root) \
%dir %{_usr}/share/selinux/%1 \
%{_usr}/share/selinux/%1/*.pp \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %{_sysconfdir}/selinux/%1/setrans.conf \
%ghost %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/modules \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
%attr(700,root,root) %dir %{_sysconfdir}/selinux/%1/modules/active \
#%verify(not md5 size mtime) %attr(600,root,root) %config(noreplace) %{_sysconfdir}/selinux/%1/modules/active/seusers \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%ghost %{_sysconfdir}/selinux/%1/policy/policy.* \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config %{_sysconfdir}/selinux/%1/contexts/customizable_types \
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
%config %{_sysconfdir}/selinux/%1/contexts/files/media \
%{_usr}/share/selinux/%1/include

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
x=`ls *.pp | grep -v -e base.pp -e enableaudit.pp | awk '{ print "-i " $1 }'`; \
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
%patch -p1

%install
# Build targeted policy
%{__rm} -fR %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man8/
install -m 644 man/man8/*.8 %{buildroot}%{_mandir}/man8/
mkdir -p %{buildroot}%{_sysconfdir}/selinux
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/selinux/config
touch %{buildroot}%{_sysconfdir}/sysconfig/selinux

# Install devel
make clean
make NAME=targeted TYPE=targeted-mcs DISTRO=%{distro} DIRECT_INITRC=y MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name}-%{version} POLY=%3 install-headers install-docs
mkdir %{buildroot}%{_usr}/share/selinux/devel/
mv %{buildroot}%{_usr}/share/selinux/targeted/include %{buildroot}%{_usr}/share/selinux/devel/include
install -m 755 ${RPM_SOURCE_DIR}/policygentool %{buildroot}%{_usr}/share/selinux/devel/
install -m 644 ${RPM_SOURCE_DIR}/Makefile.devel %{buildroot}%{_usr}/share/selinux/devel/Makefile
install -m 644 doc/example.* %{buildroot}%{_usr}/share/selinux/devel/
echo  "htmlview file:///usr/share/doc/selinux-policy-%{version}/html/index.html"> %{buildroot}%{_usr}/share/selinux/devel/policyhelp
chmod +x %{buildroot}%{_usr}/share/selinux/devel/policyhelp

%if %{BUILD_TARGETED}
# Build targeted policy
# Commented out because only targeted ref policy currently builds
%setupCmds targeted targeted-mcs y n
%installCmds targeted targeted-mcs y  n
%endif

%if %{BUILD_STRICT}
# Build strict policy
# Commented out because only targeted ref policy currently builds
make NAME=strict TYPE=strict-mcs DISTRO=%{distro} DIRECT_INITRC=y MONOLITHIC=%{monolithic} POLY=n bare 
make NAME=strict TYPE=strict-mcs DISTRO=%{distro} DIRECT_INITRC=y MONOLITHIC=%{monolithic} POLY=n conf
cp -f ${RPM_SOURCE_DIR}/modules-strict.conf  ./policy/modules.conf 
%installCmds strict strict-mcs y n
ln -sf ../devel/include %{buildroot}%{_usr}/share/selinux/strict 
%endif

%if %{BUILD_MLS}
# Build mls policy
%setupCmds mls strict-mls n y
%installCmds mls strict-mls n y 
%endif

%clean
%{__rm} -fR %{buildroot}

%post
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
	. /etc/selinux/config
	# if first time update booleans.local needs to be copied to sandbox
	[ -f /etc/selinux/${SELINUXTYPE}/booleans.local ] && mv /etc/selinux/${SELINUXTYPE}/booleans.local /etc/selinux/targeted/modules/active/
	[ -f /etc/selinux/${SELINUXTYPE}/seusers ] && cp -f /etc/selinux/${SELINUXTYPE}/seusers /etc/selinux/${SELINUXTYPE}/modules/active/seusers
	grep -q "^SETLOCALDEFS" /etc/selinux/config || echo -n "
# SETLOCALDEFS= Check local definition changes
SETLOCALDEFS=0 
">> /etc/selinux/config
fi

%postun
if [ $1 = 0 ]; then
	setenforce 0 2> /dev/null
	if [ ! -s /etc/selinux/config ]; then
		echo "SELINUX=disabled" > /etc/selinux/config
	else
		sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
	fi
fi


%if %{BUILD_TARGETED}
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

%pre targeted
%saveFileContext targeted

%post targeted
%rebuildpolicy targeted
%relabel targeted

%triggerpostun targeted -- selinux-policy-targeted <= 2.0.7
%rebuildpolicy targeted

%files targeted
%fileList targeted

%endif

%if %{BUILD_MLS}
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

%files mls
%fileList mls

%endif

%if %{BUILD_STRICT}

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

%triggerpostun strict -- selinux-policy-strict <= 2.2.35-2
cd /usr/share/selinux/strict
x=`ls *.pp | grep -v -e base.pp -e enableaudit.pp | awk '{ print "-i " $1 }'`
semodule -b base.pp -r bootloader -r clock -r dpkg -r fstools -r hotplug -r init -r libraries -r locallogin -r logging -r lvm -r miscfiles -r modutils -r mount -r mta -r netutils -r selinuxutil -r storage -r sysnetwork -r udev -r userdomain -r vpnc -r xend $x -s strict

%triggerpostun strict -- strict <= 2.0.7
%{rebuildpolicy} strict 

%files strict
%fileList strict

%endif

%changelog
* Wed Jul 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-5
- add boolean to allow zebra to write config files

* Tue Jul 18 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-4
- setroubleshootd fixes

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-3
- Allow prelink to read bin_t symlink
- allow xfs to read random devices
- Change gfs to support xattr


* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-2
- Remove spamassassin_can_network boolean

* Fri Jul 14 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-1
- Update to upstream
- Fix lpr domain for mls

* Fri Jul 14 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-4
- Add setroubleshoot policy

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-3
- Turn off auditallow on setting booleans

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-2
- Multiple fixes

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-1
- Update to upstream

* Thu Jun 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.1-1
- Update to upstream
- Add new class for kernel key ring

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.49-1
- Update to upstream

* Tue Jun 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.48-1
- Update to upstream

* Tue Jun 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-5
- Break out selinux-devel package

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-4
- Add ibmasmfs

* Thu Jun 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-3
- Fix policygentool gen_requires

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-1
- Update from Upstream

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.46-2
- Fix spec of realplay

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.46-1
- Update to upstream

* Mon Jun 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-3
- Fix semanage

* Mon Jun 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-2
- Allow useradd to create_home_dir in MLS environment

* Thu Jun 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-1
- Update from upstream

* Tue Jun 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.44-1
- Update from upstream

* Tue Jun 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-4
- Add oprofilefs

* Sun May 28 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-3
- Fix for hplip and Picasus

* Sat May 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-2
- Update to upstream

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-1
- Update to upstream

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-4
- fixes for spamd

* Wed May 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-3
- fixes for java, openldap and webalizer

* Mon May 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-2
- Xen fixes

* Thu May 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-1
- Upgrade to upstream

* Thu May 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.41-1
- allow hal to read boot_t files
- Upgrade to upstream

* Wed May 17 2006 Dan Walsh <dwalsh@redhat.com> 2.2.40-2
- allow hal to read boot_t files

* Tue May 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.40-1
- Update from upstream

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.39-2
- Fixes for amavis

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.39-1
- Update from upstream

* Fri May 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-6
- Allow auditctl to search all directories

* Thu May 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-5
- Add acquire service for mono.

* Thu May 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-4
- Turn off allow_execmem boolean
- Allow ftp dac_override when allowed to access users homedirs

* Wed May 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-3
- Clean up spec file
- Transition from unconfined_t to prelink_t

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-2
- Allow execution of cvs command

* Fri May 5 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-1
- Update to upstream

* Wed May 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.37-1
- Update to upstream

* Mon May 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.36-2
- Fix libjvm spec

* Tue Apr 25 2006 Dan Walsh <dwalsh@redhat.com> 2.2.36-1
- Update to upstream

* Tue Apr 25 2006 James Antill <jantill@redhat.com> 2.2.35-2
- Add xm policy
- Fix policygentool

* Mon Apr 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.35-1
- Update to upstream
- Fix postun to only disable selinux on full removal of the packages

* Fri Apr 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-3
- Allow mono to chat with unconfined

* Thu Apr 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-2
- Allow procmail to sendmail
- Allow nfs to share dosfs

* Thu Apr 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-1
- Update to latest from upstream
- Allow selinux-policy to be removed and kernel not to crash

* Tue Apr 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.33-1
- Update to latest from upstream
- Add James Antill patch for xen
- Many fixes for pegasus

* Sat Apr 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.32-2
- Add unconfined_mount_t
- Allow privoxy to connect to httpd_cache
- fix cups labeleing on /var/cache/cups

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.32-1
- Update to latest from upstream

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.31-1
- Update to latest from upstream
- Allow mono and unconfined to talk to initrc_t dbus objects

* Tue Apr 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.30-2
- Change libraries.fc to stop shlib_t form overriding texrel_shlib_t

* Tue Apr 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.30-1
- Fix samba creating dirs in homedir
- Fix NFS so its booleans would work

* Mon Apr 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-6
- Allow secadm_t ability to relabel all files
- Allow ftp to search xferlog_t directories
- Allow mysql to communicate with ldap
- Allow rsync to bind to rsync_port_t

* Mon Apr 10 2006 Russell Coker <rcoker@redhat.com> 2.2.29-5
- Fixed mailman with Postfix #183928
- Allowed semanage to create file_context files.
- Allowed amanda_t to access inetd_t TCP sockets and allowed amanda_recover_t
  to bind to reserved ports.  #149030
- Don't allow devpts_t to be associated with tmp_t.
- Allow hald_t to stat all mountpoints.
- Added boolean samba_share_nfs to allow smbd_t full access to NFS mounts.
  #169947
- Make mount run in mount_t domain from unconfined_t to prevent mislabeling of
  /etc/mtab.
- Changed the file_contexts to not have a regex before the first ^/[a-z]/
  whenever possible, makes restorecon slightly faster.
- Correct the label of /etc/named.caching-nameserver.conf
- Now label /usr/src/kernels/.+/lib(/.*)? as usr_t instead of
  /usr/src(/.*)?/lib(/.*)? - I don't think we need anything else under /usr/src
  hit by this.
- Granted xen access to /boot, allowed mounting on xend_var_lib_t, and allowed
  xenstored_t rw access to the xen device node.

* Tue Apr 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-4
- More textrel_shlib_t file path fixes
- Add ada support

* Mon Apr 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-3
- Get auditctl working in MLS policy

* Mon Apr 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-2
- Add mono dbus support
- Lots of file_context fixes for textrel_shlib_t in FC5
- Turn off execmem auditallow since they are filling log files

* Fri Mar 30 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-1
- Update to upstream

* Thu Mar 30 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-3
- Allow automount and dbus to read cert files

* Thu Mar 30 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-2
- Fix ftp policy
- Fix secadm running of auditctl

* Mon Mar 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-1
- Update to upstream

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.27-1
- Update to upstream

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.25-3
- Fix policyhelp

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.25-2
- Fix pam_console handling of usb_device
- dontaudit logwatch reading /mnt dir

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 2.2.24-1
- Update to upstream

* Wed Mar 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-19
- Get transition rules to create policy.20 at SystemHigh

* Tue Mar 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-18
- Allow secadmin to shutdown system
- Allow sendmail to exec newalias

* Tue Mar 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-17
- MLS Fixes
	dmidecode needs mls_file_read_up
- add ypxfr_t
- run init needs access to nscd
- udev needs setuid
- another xen log file
- Dontaudit mount getattr proc_kcore_t

* Tue Mar 14 2006 Karsten Hopp <karsten@redhat.de> 2.2.23-16
- fix buildroot usage (#185391)

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-15
- Get rid of mount/fsdisk scan of /dev messages
- Additional fixes for suspend/resume

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-14
- Fake make to rebuild enableaudit.pp

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-13
- Get xen networking running.

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-12
- Fixes for Xen
- enableaudit should not be the same as base.pp
- Allow ps to work for all process

* Thu Mar  9 2006 Jeremy Katz <katzj@redhat.com> - 2.2.23-11
- more xen policy fixups

* Wed Mar  8 2006 Jeremy Katz <katzj@redhat.com> - 2.2.23-10
- more xen fixage (#184393)

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-9
- Fix blkid specification
- Allow postfix to execute mailman_que

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-8
- Blkid changes
- Allow udev access to usb_device_t
- Fix post script to create targeted policy config file

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-7
- Allow lvm tools to create drevice dir

* Tue Mar 7 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-5
- Add Xen support

* Mon Mar 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-4
- Fixes for cups
- Make cryptosetup work with hal

* Sun Mar 5 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-3
- Load Policy needs translock

* Sat Mar 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-2
- Fix cups html interface

* Sat Mar 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-1
- Add hal changes suggested by Jeremy
- add policyhelp to point at policy html pages

* Mon Feb 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.22-2
- Additional fixes for nvidia and cups

* Mon Feb 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.22-1
- Update to upstream
- Merged my latest fixes
- Fix cups policy to handle unix domain sockets

* Sat Feb 25 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-9
- NSCD socket is in nscd_var_run_t needs to be able to search dir

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-8
- Fixes Apache interface file

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-7
- Fixes for new version of cups

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-6
- Turn off polyinstatiate util after FC5

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-5
- Fix problem with privoxy talking to Tor

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-4
- Turn on polyinstatiation

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-3
- Don't transition from unconfined_t to fsadm_t

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-2
- Fix policy update model.

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-1
- Update to upstream

* Wed Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.20-1
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
