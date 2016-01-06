%{?scl:%{?scl_package:%scl_package binutils}}

%define	githash 38573e7d
Name:		%{?scl_prefix}memstomp
Version:	0.1.5
Release:	3%{?dist}
Summary:	Warns of memory argument overlaps to various functions
Group:		Development/Debuggers
License:	LGPLv3+ and GPLv2+
URL:		git://fedorapeople.org/home/fedora/wcohen/public_git/memstomp
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone git://fedorapeople.org/home/fedora/wcohen/public_git/memstomp
# cd memstomp
# git archive --prefix memstomp-0.1.5-38573e7d/ master | gzip > memstomp-0.1.5-38573e7d.tar.gz
Source0:	memstomp-%{version}-%{githash}.tar.gz
Requires:	util-linux
BuildRequires:	binutils-devel autoconf automake dejagnu
BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Patch0: memstomp-testsuite.patch
Patch1: memstomp-man.patch
Patch2: memstomp-rh961495.patch
Patch3: memstomp-rh962763.patch
Patch4: memstomp-quietmode.patch
Patch5: memstomp-rh1133815.patch
Patch6: memstomp-rh1093173.patch


%define alternatives_cmd %{!?scl:%{_sbindir}}%{?scl:%{_root_sbindir}}/alternatives
%define alternatives_cmdline %{alternatives_cmd}%{?scl: --altdir %{_sysconfdir}/alternatives --admindir %{_scl_root}/var/lib/alternatives}

%{?scl:Requires:%scl_runtime}


%description 
memstomp is a simple program that can be used to identify
places in code which trigger undefined behaviour due to
overlapping memory arguments to certain library calls.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%prep
%setup -q -n memstomp-%{version}-%{githash}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1


%build
autoreconf

%configure
make %{?_smp_mflags} CFLAGS+="-fno-strict-aliasing"
make -k check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README LGPL3 GPL2 GPL3
%{_bindir}/memstomp
%{_libdir}/libmemstomp.so
%{_libdir}/libmemstomp-backtrace-symbols.so
%{_mandir}/man1/memstomp.1.gz

%changelog
* Thu Dec 18 2014 Jeff Law <law@redhat.com> 0.1.5-3
- Add checking of various str* and mem* for NULL arguments (#1093173)

* Tue Aug 26 2014 Jeff Law <law@redhat.com> 0.1.5-2
- Adjust PC values in saved frame addresses to get line number
  associations correct (#1133815).

* Mon May 19 2014 Marek Polacek <polacek@redhat.com> 0.1.5-1
- Rebase to 0.1.5 (#1096161)

* Thu May 30 2013 Jeff Law <law@redhat.com> 0.1.4-11
- Add -q/--quiet options for quiet mode.

* Tue May 14 2013 Jeff Law <law@redhat.com> 0.1.4-10
- Link in libiberty (#962763)

* Thu May 9 2013 Jeff Law <law@redhat.com> 0.1.4-9
- Improve man page (#961518)

* Thu May 9 2013 Jeff Law <law@redhat.com> 0.1.4-8
- Fix typo in initialization message (#961495)

* Thu Mar 28 2013 Jeff Law <law@redhat.com> 0.1.4-7
- Rebuild with new build roots

* Mon Mar 18 2013 Jeff Law <law@redhat.com> 0.1.4-6
- Bring back $RPM_BUILD_ROOT

* Fri Mar 15 2013 Jeff Law <law@redhat.com> 0.1.4-5
- Build tests with -fno-builtin

* Mon Mar 11 2013 Jeff Law <law@redhat.com> 0.1.4-4
- Add manpage
- Add initial testsuite

* Fri Feb 22 2013 Jeff Law <law@redhat.com> 0.1.4-3
- Change %%define to %%global for git hash
- Remove git hash from version # in changelog

* Wed Feb 20 2013 Jeff Law <law@redhat.com> 0.1.4-2
- Build with -fno-strict-aliasing

* Tue Feb 5 2013 Jeff Law <law@redhat.com> 0.1.4-1
- Initial release
