#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_fastcgi
%define load_order 192

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	2.4.6
Release:	15
Group:		System/Servers
License:	BSD-style
URL:		http://www.fastcgi.com/
Source0:	http://www.fastcgi.com/dist/%{mod_name}-%{version}.tar.gz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}

%description
mod_fastcgi provides FastCGI support for the apache web server. FastCGI is a
language independent, scalable, open  extension to CGI that provides high
performance and persistence  without the limitations of server specific APIs.

%prep

%setup -q -n %{mod_name}-%{version}

# get rid of the "cannot remove /var/run/fastcgi/dynamic" error at boot
perl -pi -e "s|^#define DEFAULT_SOCK_DIR  DEFAULT_REL_RUNTIMEDIR .*|#define DEFAULT_SOCK_DIR \"/var/lib/mod_fastcgi\"|g" mod_fastcgi.h

%build

apxs -c mod_fastcgi.c f*.c

%install

install -d %{buildroot}/var/www/fcgi-bin
install -d %{buildroot}%{_libdir}/apache
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}/var/lib/mod_fastcgi/dynamic

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/

cat > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{load_order}_%{mod_name}.conf << EOF
LoadModule fastcgi_module %{_libdir}/%{mod_name}.so

ScriptAlias /fcgi-bin/ /var/www/fcgi-bin/

<Directory /var/www/fcgi-bin>

    AllowOverride All
    Options ExecCGI

    SetHandler fastcgi-script
    AddHandler fastcgi-script .fcg .fcgi .fpl

    Order allow,deny
    Allow from all

</Directory>
EOF

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
%doc docs/* CHANGES
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/*.conf
%attr(0755,root,root) %{_libdir}/apache/*.so
%dir /var/www/fcgi-bin
%attr(0755,apache,apache) %dir /var/lib/mod_fastcgi
%attr(0755,apache,apache) %dir /var/lib/mod_fastcgi/dynamic
