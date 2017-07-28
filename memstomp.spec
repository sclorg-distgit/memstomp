%{?scl:%{?scl_package:%scl_package binutils}}

%global		githash 38573e7d
Name:		%{?scl_prefix}memstomp
Version:	0.1.5
Release:	5%{?dist}
Summary:	Warns of memory argument overlaps to various functions
Group:		Development/Debuggers
# The entire source code is LGPLV3+ with the exception of backtrace-symbols.c which
# is GPLv2+ by way of being a hacked up old version of binutils's addr2line.
# backtrace-symbols.c is built into an independent .so to avoid license contamination
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
Patch5: memstomp-rh1093173.patch
Patch6: memstomp-rh1133815.patch
Patch7: memstomp-implicit-int.patch


%define alternatives_cmd %{!?scl:%{_sbindir}}%{?scl:%{_root_sbindir}}/alternatives
%define alternatives_cmdline %{alternatives_cmd}%{?scl: --altdir %{_sysconfdir}/alternatives --admindir %{_scl_root}/var/lib/alternatives}

%{?scl:Requires:%scl_runtime}


%description 
memstomp is a simple program that can be used to identify
places in code which trigger undefined behavior due to
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
%patch7 -p1


%build
autoreconf
%configure
# We force -O0 here because memstomp essentially relies on GCC
# not removing any of its checks.  GCC continues to get better
# and twarting its optimizer isn't something I have any interest
# in maintaining over time.  So just force -O0 for stupid code
# generation.
make %{?_smp_mflags} CFLAGS+="-O0 -fno-strict-aliasing"
make -k check

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc README LGPL3 GPL2 GPL3
%{_bindir}/memstomp
%{_libdir}/libmemstomp.so
%{_libdir}/libmemstomp-backtrace-symbols.so
%{_mandir}/man1/memstomp.1.gz

%changelog
* Tue Jul 26 2016 Jeff Law <law@redhat.com> 0.1.5-5
- Resync with Fedora and rebuild for DTS 6

