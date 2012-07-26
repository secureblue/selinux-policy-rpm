#! /usr/bin/python -Es
# Copyright (C) 2012 Red Hat 
# AUTHOR: Dan Walsh <dwalsh@redhat.com>
# see file 'COPYING' for use and warranty information
#
# semanage is a tool for managing SELinux configuration files
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License as
#    published by the Free Software Foundation; either version 2 of
#    the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA     
#                                        02111-1307  USA
#
#  
import seobject
import selinux
import datetime
import setools
import sys

all_attributes = map(lambda x: x['name'], setools.seinfo(setools.ATTRIBUTE))
entrypoints =  setools.seinfo(setools.ATTRIBUTE,"entry_type")[0]["types"]
alldomains =  setools.seinfo(setools.ATTRIBUTE,"domain")[0]["types"]
domains = []

for d in alldomains:
    found = False
    if d[:-2] + "_exec_t" not in entrypoints:
        continue
    name = d.split("_")[0]
    if name in domains or name == "pam":
        continue
    domains.append(name)

domains.sort()

file_types =  setools.seinfo(setools.ATTRIBUTE,"file_type")[0]["types"]
file_types.sort()

port_types =  setools.seinfo(setools.ATTRIBUTE,"port_type")[0]["types"]
port_types.sort()

portrecs = seobject.portRecords().get_all_by_type()
filerecs = seobject.fcontextRecords()
files_dict = {}
fdict = filerecs.get_all()
for i in fdict:
    if fdict[i]:
        if fdict[i][2] in files_dict:
            files_dict[fdict[i][2]].append(i)
        else:
            files_dict[fdict[i][2]] = [i]
boolrecs = seobject.booleanRecords()
bools = seobject.booleans_dict.keys()

man = {}
date = datetime.datetime.now().strftime("%d %b %Y")
def prettyprint(f,trim):
    return " ".join(f[:-len(trim)].split("_"))

class ManPage:
    def __init__(self, domainname, path="/tmp"):
        self.domainname = domainname
        if self.domainname[-1]=='d':
            self.short_name = self.domainname[:-1]
        else:
            self.short_name = domainname

        self.anon_list = []
        self.fd = open("%s/%s_selinux.8" % (path, domainname), 'w')

        self.attributes = {}
        self.ptypes = []
        self.get_ptypes()

        for domain_type in self.ptypes:
            self.attributes[domain_type] = setools.seinfo(setools.TYPE,("%s") % domain_type)[0]["attributes"]

        self.header()
        self.booleans()
        self.nsswitch_domain()
        self.public_content()
        self.file_context()
        self.port_types()
        self.process_types()
        self.footer()
        self.fd.close()

    def get_ptypes(self):
        for f in alldomains:
            if f.startswith(self.short_name):
                self.ptypes.append(f)

    def header(self):
        self.fd.write('.TH  "%(domainname)s_selinux"  "8"  "%(domainname)s" "dwalsh@redhat.com" "%(domainname)s SELinux Policy documentation"'
                 % {'domainname':self.domainname})
        self.fd.write(r"""
.SH "NAME"
%(domainname)s_selinux \- Security Enhanced Linux Policy for the %(domainname)s processes
.SH "DESCRIPTION"

Security-Enhanced Linux secures the %(domainname)s processes via flexible mandatory access
control.  
""" % {'domainname':self.domainname})


    def explain(self, f):
        if f.endswith("_var_run_t"):
            return "store the %s files under the /run directory." % prettyprint(f, "_var_run_t")
        if f.endswith("_pid_t"):
            return "store the %s files under the /run directory." % prettyprint(f, "_pid_t")
        if f.endswith("_var_lib_t"):
            return "store the %s files under the /var/lib directory."  % prettyprint(f, "_var_lib_t")
        if f.endswith("_var_t"):
            return "store the %s files under the /var directory."  % prettyprint(f, "_var_lib_t")
        if f.endswith("_var_spool_t"):
            return "store the %s files under the /var/spool directory." % prettyprint(f, "_spool_t")
        if f.endswith("_spool_t"):
            return "store the %s files under the /var/spool directory." % prettyprint(f, "_spool_t")
        if f.endswith("_cache_t") or f.endswith("_var_cache_t"):
            return "store the files under the /var/cache directory."
        if f.endswith("_keytab_t"):
            return "treat the files as kerberos keytab files."
        if f.endswith("_lock_t"):
            return "treat the files as %s lock data, stored under the /var/lock directory" % prettyprint(f,"_lock_t")
        if f.endswith("_log_t"):
            return "treat the data as %s log data, usually stored under the /var/log directory." % prettyprint(f,"_log_t")
        if f.endswith("_config_t"):
            return "treat the files as %s configuration data, usually stored under the /etc directory." % prettyprint(f,"_config_t")
        if f.endswith("_conf_t"):
            return "treat the files as %s configuration data, usually stored under the /etc directory." % prettyprint(f,"_conf_t")
        if f.endswith("_exec_t"):
            return "transition an executable to the %s_t domain." % f[:-len("_exec_t")]
        if f.endswith("_cgi_content_t"):
            return "treat the files as %s cgi content." % prettyprint(f, "_cgi_content_t")
        if f.endswith("_rw_content_t"):
            return "treat the files as %s read/write content." % prettyprint(f,"_rw_content_t")
        if f.endswith("_rw_t"):
            return "treat the files as %s read/write content." % prettyprint(f,"_rw_t")
        if f.endswith("_write_t"):
            return "treat the files as %s read/write content." % prettyprint(f,"_write_t")
        if f.endswith("_db_t"):
            return "treat the files as %s database content." % prettyprint(f,"_db_t")
        if f.endswith("_ra_content_t"):
            return "treat the files as %s read/append content." % prettyprint(f,"_ra_conten_t")
        if f.endswith("_cert_t"):
            return "treat the files as %s certificate data." % prettyprint(f,"_cert_t")
        if f.endswith("_key_t"):
            return "treat the files as %s key data." % prettyprint(f,"_key_t")

        if f.endswith("_secret_t"):
            return "treat the files as %s secret data." % prettyprint(f,"_key_t")

        if f.endswith("_ra_t"):
            return "treat the files as %s read/append content." % prettyprint(f,"_ra_t")

        if f.endswith("_ro_t"):
            return "treat the files as %s read/only content." % prettyprint(f,"_ro_t")

        if f.endswith("_modules_t"):
            return "treat the files as %s modules." % prettyprint(f, "_modules_t")

        if f.endswith("_content_t"):
            return "treat the files as %s content." % prettyprint(f, "_content_t")

        if f.endswith("_state_t"):
            return "treat the files as %s state data." % prettyprint(f, "_state_t")

        if f.endswith("_files_t"):
            return "treat the files as %s content." % prettyprint(f, "_files_t")

        if f.endswith("_file_t"):
            return "treat the files as %s content." % prettyprint(f, "_file_t")

        if f.endswith("_data_t"):
            return "treat the files as %s content." % prettyprint(f, "_data_t")

        if f.endswith("_file_t"):
            return "treat the data as %s content." % prettyprint(f, "_file_t")

        if f.endswith("_tmp_t"):
            return "store %s temporary files in the /tmp directories." % prettyprint(f, "_tmp_t")
        if f.endswith("_etc_t"):
            return "store %s files in the /etc directories." % prettyprint(f, "_tmp_t")
        if f.endswith("_home_t"):
            return "store %s files in the users home directory." % prettyprint(f, "_home_t")
        if f.endswith("_tmpfs_t"):
            return "store %s files on a tmpfs file system." % prettyprint(f, "_tmpfs_t")
        if f.endswith("_unit_file_t"):
            return "treat files as a systemd unit file." 
        if f.endswith("_htaccess_t"):
            return "treat the file as a %s access file." % prettyprint(f, "_htaccess_t")

        return "treat the files as %s data." % prettyprint(f,"_t")

    def booleans(self):
        self.booltext = ""
        for b in bools:
            if b.find(self.short_name) >= 0:
                if b.endswith("anon_write"):
                    self.anon_list.append(b)
                else:
                    desc = seobject.booleans_dict[b][2][0].lower() + seobject.booleans_dict[b][2][1:]
                    if desc[-1] == ".":
                        desc = desc[:-1]
                    self.booltext += """
.PP
If you want to %s, you must turn on the %s boolean.

.EX
.B setsebool -P %s 1
.EE
""" % (desc, b, b)
    
        if self.booltext != "":        
            self.fd.write("""
.SH BOOLEANS
SELinux policy is customizable based on least access required.  %s policy is extremely flexible and has several booleans that allow you to manipulate the policy and run %s with the tightest access possible.

""" % (self.domainname, self.domainname))

            self.fd.write(self.booltext)

    def nsswitch_domain(self):
        nsswitch_types = []
        nsswitch_booleans = ['authlogin_nsswitch_use_ldap', 'kerberos_enabled']
        nsswitchbooltext = ""
        if "nsswitch_domain" in all_attributes:
            self.fd.write("""
.SH NSSWITCH DOMAIN
""")
            for k in self.attributes.keys():    
                if "nsswitch_domain" in self.attributes[k]:
                    nsswitch_types.append(k)

            if len(nsswitch_types):
                for i in nsswitch_booleans:
                    desc = seobject.booleans_dict[i][2][0].lower() + seobject.booleans_dict[i][2][1:-1]
                    nsswitchbooltext += """
.PP
If you want to %s for the %s, you must turn on the %s boolean.

.EX
setsebool -P %s 1
.EE
""" % (desc,(", ".join(nsswitch_types)), i, i)

        self.fd.write(nsswitchbooltext)

    def process_types(self):
        if len(self.ptypes) == 0:
            return
        self.fd.write(r"""
.SH PROCESS TYPES
SELinux defines process types (domains) for each process running on the system
.PP
You can see the context of a process using the \fB\-Z\fP option to \fBps\bP
.PP
Policy governs the access confined processes have to files. 
SELinux %(domainname)s policy is very flexible allowing users to setup their %(domainname)s processes in as secure a method as possible.
.PP 
The following process types are defined for %(domainname)s:
""" % {'domainname':self.domainname})
        self.fd.write("""
.EX
.B %s 
.EE""" % ", ".join(self.ptypes))
        self.fd.write("""
.PP
Note: 
.B semanage permissive -a PROCESS_TYPE 
can be used to make a process type permissive. Permissive process types are not denied access by SELinux. AVC messages will still be generated.
""")

    def port_types(self):
        self.ports = []
        for f in port_types:
            if f.startswith(self.short_name):
                self.ports.append(f)

        if len(self.ports) == 0:
            return
        self.fd.write("""
.SH PORT TYPES
SELinux defines port types to represent TCP and UDP ports. 
.PP
You can see the types associated with a port by using the following command: 

.B semanage port -l

.PP
Policy governs the access confined processes have to these ports. 
SELinux %(domainname)s policy is very flexible allowing users to setup their %(domainname)s processes in as secure a method as possible.
.PP 
The following port types are defined for %(domainname)s:""" % {'domainname':self.domainname})

        for p in self.ports:
            self.fd.write("""

.EX
.TP 5
.B %s 
.TP 10
.EE
""" % p)
            once = True
            for prot in ( "tcp", "udp" ):
               if (p,prot) in portrecs:
                    if once:
                        self.fd.write("""

Default Defined Ports:""")
                    once = False
                    self.fd.write(r"""
%s %s
.EE""" % (prot, ",".join(portrecs[(p,prot)])))

    def file_context(self):
        self.fd.write(r"""
.SH FILE CONTEXTS
SELinux requires files to have an extended attribute to define the file type. 
.PP
You can see the context of a file using the \fB\-Z\fP option to \fBls\bP
.PP
Policy governs the access confined processes have to these files. 
SELinux %(domainname)s policy is very flexible allowing users to setup their %(domainname)s processes in as secure a method as possible.
.PP 
The following file types are defined for %(domainname)s:
""" % {'domainname':self.domainname})
        for f in file_types:
            if f.startswith(self.domainname):
                self.fd.write("""

.EX
.PP
.B %s 
.EE

- Set files with the %s type, if you want to %s
""" % (f, f, self.explain(f)))

                if f in files_dict:
                    plural = ""
                    if len(files_dict[f]) > 1:
                        plural = "s"
                        self.fd.write("""
.br
.TP 5
Path%s: 
%s""" % (plural, files_dict[f][0][0]))
                        for x in files_dict[f][1:]:
                            self.fd.write(", %s" % x[0])

        self.fd.write("""

.PP
Note: File context can be temporarily modified with the chcon command.  If you want to permanently change the file context you need to use the 
.B semanage fcontext 
command.  This will modify the SELinux labeling database.  You will need to use
.B restorecon
to apply the labels.
""")

    def public_content(self):
        if len(self.anon_list) > 0:
            self.fd.write("""
.SH SHARING FILES
If you want to share files with multiple domains (Apache, FTP, rsync, Samba), you can set a file context of public_content_t and public_content_rw_t.  These context allow any of the above domains to read the content.  If you want a particular domain to write to the public_content_rw_t domain, you must set the appropriate boolean.
.TP
Allow %(domainname)s servers to read the /var/%(domainname)s directory by adding the public_content_t file type to the directory and by restoring the file type.
.PP
.B
semanage fcontext -a -t public_content_t "/var/%(domainname)s(/.*)?"
.br
.B restorecon -F -R -v /var/%(domainname)s
.pp
.TP
Allow %(domainname)s servers to read and write /var/tmp/incoming by adding the public_content_rw_t type to the directory and by restoring the file type.  This also requires the allow_%(domainname)sd_anon_write boolean to be set.
.PP
.B
semanage fcontext -a -t public_content_rw_t "/var/%(domainname)s/incoming(/.*)?"
.br
.B restorecon -F -R -v /var/%(domainname)s/incoming

"""  % {'domainname':self.domainname})
            for b in self.anon_list:
                desc = seobject.booleans_dict[b][2][0].lower() + seobject.booleans_dict[b][2][1:]
                self.fd.write("""
.PP
If you want to %s, you must turn on the %s boolean.

.EX
.B setsebool -P %s 1
.EE
""" % (desc, b, b))

    def footer(self):
        self.fd.write("""
.SH "COMMANDS"
.B semanage fcontext
can also be used to manipulate default file context mappings.
.PP
.B semanage permissive
can also be used to manipulate whether or not a process type is permissive.
.PP
.B semanage module
can also be used to enable/disable/install/remove policy modules.
""")

        if len(self.ports) > 0:
            self.fd.write("""
.B semanage port
can also be used to manipulate the port definitions
""")

        if self.booltext != "":        
            self.fd.write("""
.B semanage boolean
can also be used to manipulate the booleans
""")

        self.fd.write("""
.PP
.B system-config-selinux 
is a GUI tool available to customize SELinux policy settings.

.SH AUTHOR	
This manual page was autogenerated by genman.py.

.SH "SEE ALSO"
selinux(8), %s(8), semanage(8), restorecon(8), chcon(1)
""" % self.domainname)

        if self.booltext != "":        
            self.fd.write(", setsebool(8)")

if len(sys.argv) > 2:
        domains = sys.argv[2:]

for domainname in domains:
    ManPage(domainname, sys.argv[1])
