%define distro redhat
%define direct_initrc y
%define monolithic n
%define polname1 targeted
%define polname2 mls
%define polname3 strict
%define POLICYVER 20
%define POLICYCOREUTILSVER 1.27.28-3
%define CHECKPOLICYVER 1.27.17-7
Summary: SELinux policy configuration
Name: selinux-policy
Version: 2.0.5
Release: 4
License: GPL
Group: System Environment/Base
Source: serefpolicy-%{version}.tgz
patch: policy-20051114.patch
Source1: modules-%{polname1}.conf
Source2: booleans-%{polname1}.conf
Source3: seusers-%{polname1}
Source4: setrans-%{polname1}.conf
Source5: modules-%{polname2}.conf
Source6: booleans-%{polname2}.conf
Source7: seusers-%{polname2}
Source8: setrans-%{polname2}.conf

Url: http://serefpolicy.sourceforge.net
BuildRoot: %{_tmppath}/serefpolicy-buildroot
BuildArch: noarch
BuildRequires: checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils >= %{POLICYCOREUTILSVER}
Requires: policycoreutils >= %{POLICYCOREUTILSVER}
Obsoletes: policy 

%package %{polname1}
Summary: SELinux %{polname1} base policy
Group: System Environment/Base
Provides: selinux-policy-base
Obsoletes: selinux-policy-%{polname1}-sources

%description %{polname1}
SELinux Reference policy targeted base module.

%define installCmds() \
cp -f ${RPM_SOURCE_DIR}/modules-%1.conf  ./policy/modules.conf \
cp -f ${RPM_SOURCE_DIR}/booleans-%1.conf ./policy/booleans.conf \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} base.pp \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} modules \
%{__mkdir} -p $RPM_BUILD_ROOT/%{_usr}/share/selinux/%1/ \
%{__cp} *.pp $RPM_BUILD_ROOT/%{_usr}/share/selinux/%1/ \
%{__mkdir} -p $RPM_BUILD_ROOT/%{_sysconfdir}/selinux/%1/policy \
%{__mkdir} -p $RPM_BUILD_ROOT/%{_sysconfdir}/selinux/%1/modules/active \
%{__mkdir} -p $RPM_BUILD_ROOT/%{_sysconfdir}/selinux/%1/contexts/files \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=y DESTDIR=$RPM_BUILD_ROOT install-appconfig \
semodule_expand $RPM_BUILD_ROOT/usr/share/selinux/%1/base.pp $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/booleans \
touch $RPM_BUILD_ROOT%{_sysconfdir}/selinux/config \
touch $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/seusers \
touch $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
touch $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/contexts/files/homedir_template \
touch $RPM_BUILD_ROOT%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
install -m0644 ${RPM_SOURCE_DIR}/seusers-%1 ${RPM_BUILD_ROOT}%{_sysconfdir}/selinux/%1/modules/active/seusers \
install -m0644 ${RPM_SOURCE_DIR}/setrans-%1.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/selinux/%1/setrans.conf \
%nil

%define fileList() \
%defattr(-,root,root) \
%dir %{_usr}/share/selinux \
%dir %{_usr}/share/selinux/%1 \
%config %{_usr}/share/selinux/%1/base.pp \
%dir %{_sysconfdir}/selinux \
%ghost %config(noreplace) %{_sysconfdir}/selinux/config \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %{_sysconfdir}/selinux/%1/setrans.conf \
%ghost %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/modules \
%attr(700,root,root) %dir %{_sysconfdir}/selinux/%1/modules/active \
%verify(not md5 size mtime) %attr(600,root,root) %config(noreplace) %{_sysconfdir}/selinux/%1/modules/active/seusers \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%verify(not md5 size mtime) %attr(600,root,root) %config(noreplace) %{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/customizable_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/dbus_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_type \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/failsafe_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/initrc_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/removable_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/userhelper_context \
%dir %{_sysconfdir}/selinux/%1/contexts/files \
%ghost %config %{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
%ghost %config %{_sysconfdir}/selinux/%1/contexts/files/homedir_template \
%ghost %config %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
%config %{_sysconfdir}/selinux/%1/contexts/files/media

%define saveFileContext() \
. %{_sysconfdir}/selinux/config; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
if [ "${SELINUXTYPE}" == %1 -a -f ${FILE_CONTEXT} ]; then \
	cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.pre; \
fi 

%define rebuildpolicy() \
semodule -b /usr/share/selinux/%1/base.pp -s %1 \
for file in $(ls /usr/share/selinux/%1 | grep -v base.pp) \
do \
	semodule -i /usr/share/selinux/%1/$file -s %1;\
done; \
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
make conf
%{__rm} -fR $RPM_BUILD_ROOT
%installCmds %{polname1} targeted-mcs %{direct_initrc}

# Build mls policy
make clean
make conf
%installCmds %{polname2} strict-mls n


# Build strict policy
# Commented out because only targeted ref policy currently builds
# make clean
# make conf
#%#installCmds %{polname3} strict-mcs %{direct_initrc}

%clean
%{__rm} -fR $RPM_BUILD_ROOT

%files %{polname1}
%fileList %{polname1}

%pre %{polname1}
%saveFileContext %{polname1}

%post %{polname1}
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

	ln -sf /etc/selinux/config /etc/sysconfig/selinux 
	restorecon /etc/selinux/config 2> /dev/null
else
	# if first time update booleans.local needs to be copied to sandbox
	[ -f /etc/selinux/%{polname1}/booleans.local ] && mv /etc/selinux/%{polname1}/booleans.local /etc/selinux/%{polname1}/modules/active/
	[ -f /etc/selinux/%{polname1}/seusers ] && cp -f /etc/selinux/%{polname1}/seusers /etc/selinux/%{polname1}/modules/active/seusers
	grep -q "^SETLOCALDEFS" /etc/selinux/config || echo -n "
# SETLOCALDEFS= Check local definition changes
SETLOCALDEFS=0 
">> /etc/selinux/config
fi
%rebuildpolicy %{polname1}
%relabel %{polname1}

%triggerpostun %{polname1} -- selinux-policy-%{polname1} <= 2.0.0
%rebuildpolicy %{polname1}

%package %{polname2} 
Summary: SELinux %{polname2} base policy
Group: System Environment/Base
Provides: selinux-policy-base
Obsoletes: selinux-policy-%{polname2}-sources

%description %{polname2} 
SELinux Reference policy %{polname2} base module.

%pre %{polname2} 
%saveFileContext %{polname2}

%post %{polname2} 
%rebuildpolicy %{polname2} 
%relabel %{polname2}

%triggerpostun %{polname2} -- %{polname2} <= 2.0.0
%{rebuildpolicy} %{polname2} 

%files %{polname2}
%fileList %{polname2}

%if 0
%package %{polname3} 
Summary: SELinux %{polname3} base policy
Group: System Environment/Base
Provides: selinux-policy-base
Obsoletes: selinux-policy-%{polname3}-sources

%description %{polname3} 
SELinux Reference policy %{polname3} base module.

%pre %{polname3} 
%saveFileContext %{polname3}

%post %{polname3} 
%rebuildpolicy %{polname3} 
%relabel %{polname3}

%triggerpostun %{polname3} -- %{polname3} <= 2.0.0
%{rebuildpolicy} %{polname3} 

%files %{polname3}
#%#fileList %{polname3}
%endif


%changelog
* Wed Nov 23 2003 Dan Walsh <dwalsh@redhat.com> 2.0.5-4
- Cleanup pegasus and named 
- Fix spec file
- Fix up passwd changing applications

* Tue Nov 21 2003 Dan Walsh <dwalsh@redhat.com> 2.0.5-1
-Update to latest from upstream

* Tue Nov 21 2003 Dan Walsh <dwalsh@redhat.com> 2.0.4-1
- Add rules for pegasus and avahi

* Mon Nov 21 2003 Dan Walsh <dwalsh@redhat.com> 2.0.2-2
- Start building MLS Policy

* Fri Nov 18 2003 Dan Walsh <dwalsh@redhat.com> 2.0.2-1
- Update to upstream

* Wed Nov 9 2003 Dan Walsh <dwalsh@redhat.com> 2.0.1-2
- Turn on bash

* Wed Nov 9 2003 Dan Walsh <dwalsh@redhat.com> 2.0.1-1
- Initial version
