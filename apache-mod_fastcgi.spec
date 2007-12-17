%define snap 0404142202

#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_fastcgi
%define mod_conf 92_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_fastcgi is a DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	2.4.3
Release:	%mkrel 0.%{snap}.8
Group:		System/Servers
License:	BSD-style
URL:		http://www.fastcgi.com/
Source0:	http://www.fastcgi.com/dist/mod_fastcgi-SNAP-%{snap}.tar.bz2
Source1:	%{mod_conf}
# http://www.goldenbluellc.com/download/mod_fastcgi-SNAP-0503121812.tar.bz2
Patch0:		mod_fastcgi-apache-2.1.x.diff
# a possible enhancement? http://www.3skel.com/fastcgi/fastcgisa-2.4.0_0.1.tar.gz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}

%description
mod_fastcgi provides FastCGI support for the apache web server. FastCGI is a
language independent, scalable, open  extension to CGI that provides high
performance and persistence  without the limitations of server specific APIs.

%prep

%setup -q -n mod_fastcgi-SNAP-0404142202
%patch0 -p1

cp %{SOURCE1} %{mod_conf}


# get rid of the "cannot remove /var/run/fastcgi/dynamic" error at boot
echo "#define DEFAULT_SOCK_DIR \"%{_localstatedir}/mod_fastcgi\"" >> mod_fastcgi.h

%build

%{_sbindir}/apxs -c mod_fastcgi.c f*.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}/var/www/fcgi-bin

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_localstatedir}/mod_fastcgi/dynamic

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc docs/* CHANGES
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%dir /var/www/fcgi-bin
%attr(0755,apache,apache) %dir %{_localstatedir}/mod_fastcgi
%attr(0755,apache,apache) %dir %{_localstatedir}/mod_fastcgi/dynamic
