#Module-Specific definitions
%define apache_version 2.2.6
%define mod_name mod_fastcgi
%define pre SNAP-0910052141
%define mod_conf 92_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	2.4.7
Release:	3
Group:		System/Servers
License:	BSD-style
URL:		http://www.fastcgi.com/
Source0:	http://www.fastcgi.com/dist/%{mod_name}-%{pre}.tar.gz
Source1:	%{mod_conf}
Patch0:		byte-compile-against-apache24.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_fastcgi provides FastCGI support for the apache web server. FastCGI is a
language independent, scalable, open  extension to CGI that provides high
performance and persistence  without the limitations of server specific APIs.

%prep

%setup -q -n %{mod_name}-%{pre}

cp %{SOURCE1} %{mod_conf}
# get rid of the "cannot remove /var/run/fastcgi/dynamic" error at boot
perl -pi -e "s|^#define DEFAULT_SOCK_DIR  DEFAULT_REL_RUNTIMEDIR .*|#define DEFAULT_SOCK_DIR \"/var/lib/mod_fastcgi\"|g" mod_fastcgi.h
%patch0 -p0

%build
#cp Makefile.tmpl Makefile
#make top_dir=/usr/lib64/apache
#%{_bindir}/apxs -c mod_fastcgi.c f*.c
%{_bindir}/apxs -o mod_fastcgi.so -c mod_fastcgi.c fcgi*.c

%install
rm -rf %{buildroot}

#make install
install -d %{buildroot}/var/www/fcgi-bin

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}/var/lib/mod_fastcgi/dynamic

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
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc docs/* CHANGES
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%dir /var/www/fcgi-bin
%attr(0755,apache,apache) %dir /var/lib/mod_fastcgi
%attr(0755,apache,apache) %dir /var/lib/mod_fastcgi/dynamic


%changelog
* Sat May 14 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-13mdv2011.0
+ Revision: 674427
- rebuild

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-12
+ Revision: 662775
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-11mdv2011.0
+ Revision: 588281
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-10mdv2010.1
+ Revision: 515836
- rebuilt for apache-2.2.15

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-9mdv2010.0
+ Revision: 451699
- rebuild

* Fri Jul 31 2009 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-8mdv2010.0
+ Revision: 405137
- rebuild

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-7mdv2009.1
+ Revision: 326490
- rebuild

* Sun Jul 27 2008 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-6mdv2009.0
+ Revision: 250481
- hardcode %%{_localstatedir}

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-5mdv2009.0
+ Revision: 235640
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-4mdv2009.0
+ Revision: 215290
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-3mdv2008.1
+ Revision: 181438
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 2.4.6-2mdv2008.1
+ Revision: 170720
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Thu Dec 27 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.6-1mdv2008.1
+ Revision: 138525
- 2.4.6
- drop redundant patches

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-0.0404142202.8mdv2008.0
+ Revision: 82360
- rebuild

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-0.0404142202.7mdv2008.0
+ Revision: 64320
- use the new %%serverbuild macro

* Wed Jun 13 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-0.0404142202.6mdv2008.0
+ Revision: 38412
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-0.0404142202.5mdv2007.1
+ Revision: 140582
- rebuild

* Tue Feb 27 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-0.0404142202.4mdv2007.1
+ Revision: 126611
- general cleanups

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-0.0404142202.3mdv2007.0
+ Revision: 79250
- Import apache-mod_fastcgi

* Sun Jul 30 2006 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-0.0404142202.3mdv2007.0
- rebuild

* Tue Dec 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-0.0404142202.2mdk
- heh!, first startup failure triggered by the new init script :)

* Mon Dec 12 2005 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-0.0404142202.1mdk
- "new" snapshot + patch
- rebuilt against apache-2.2.0

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.4.2-4mdk
- rebuilt to provide a -debug package too

* Wed Oct 26 2005 Oden Eriksson <oeriksson@mandriva.com> 2.4.2-3mdk
- get rid of the "cannot remove /var/run/fastcgi/dynamic" error at boot

* Mon Oct 17 2005 Oden Eriksson <oeriksson@mandriva.com> 2.4.2-2mdk
- rebuilt against correct apr-0.9.7

* Sat Oct 15 2005 Oden Eriksson <oeriksson@mandriva.com> 2.4.2-1mdk
- rebuilt for apache-2.0.55

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.4.2-3mdk
- added another work around for a rpm bug

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.4.2-2mdk
- added a work around for a rpm bug, "Requires(foo,bar)" don't work

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.4.2-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Thu Mar 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.4.2-6mdk
- use the %%mkrel macro

* Sun Feb 27 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.4.2-5mdk
- fix %%post and %%postun to prevent double restarts

* Wed Feb 16 2005 Stefan van der Eijk <stefan@eijk.nu> 2.0.53_2.4.2-4mdk
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.4.2-3mdk
- fix deps

* Tue Feb 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.4.2-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.4.2-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_2.4.2-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_2.4.2-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_2.4.2-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_2.4.2-1mdk
- 2.4.2
- built for apache 2.0.49

