Name:          swig
Version:       4.0.2
Release:       6
Summary:       Links C/C++/Objective C to languages for some advanced programing
License:       GPLv3+ and BSD
URL:           http://swig.sourceforge.net/
Source0:       http://downloads.sourceforge.net/project/swig/swig/swig-%{version}/swig-%{version}.tar.gz
Source1:       description.h2m

Patch1:        backport-PCRE2.patch
Patch2:        backport-Few-more-PCRE-to-PCRE2-changes.patch
Patch3:        backport-configure.ac-Add-missing-shell-quoting.patch
Patch4:        Backport-php-8-support-from-upstream.patch
Patch5:        0001-Ruby-Fix-deprecation-warnings-with-Ruby-3.x.patch
Patch6:        0001-gcc-12-warning-fix-in-test-case.patch

BuildRequires: perl-interpreter pcre2-devel python3-devel autoconf automake gawk dos2unix
BuildRequires: gcc-c++ help2man perl-devel perl(base) perl(Config) perl(Devel::Peek)
BuildRequires: perl(ExtUtils::MakeMaker) perl(fields) perl(Math::BigInt) perl(strict)
BuildRequires: perl(Test::More) perl(vars) perl(warnings) boost-devel bison tcl-devel
BuildRequires: lua-devel ruby-devel

Provides:      %{name}-gdb = %{version}-%{release}
Obsoletes:     %{name}-gdb < %{version}-%{release}

%description
SWIG is a compiler that attempts to make it easy to integrate C, C++,
or Objective-C code with scripting languages including Perl, Tcl, and
Python.In a nutshell, you give it a bunch of ANSI C/C++ declarations and
it generates an interface between C and your favorite scripting language.
However, this is only scratching the surface of what SWIG can do--some
of its more advanced features include automatic documentation generation,
module and library management, extensive customization options, and more.

%package help
Summary:   Help document for the swig package
License:   BSD
BuildArch: noarch

Provides:  %{name}-doc = %{version}-%{release}
Obsoletes: %{name}-doc < %{version}-%{release}

%description help
Help document for the swig package.

%prep
%autosetup -n %{name}-%{version} -p1

%build
./autogen.sh

%configure --without-ocaml --without-python --with-python3=%__python3 --without-go --disable-ccache;
%make_build

%check
%make_build check

%install
%make_install
install -d %{buildroot}%{_datadir}/swig
cp -a Examples %{buildroot}%{_datadir}/swig/examples
rm -rf %{buildroot}%{_datadir}/swig/examples/test-suite

# rm files that are not needed for running or rebuilding the examples
find %{buildroot}%{_datadir}/swig \
	-name '*.dsp' -o -name '*.vcproj' -o -name '*.sln' -o \
	-name '*.o' -o -name '*_wrap.c' -o -name '*.csproj' -o \
	-name '*.dsw' | xargs rm

find %{buildroot}%{_datadir}/swig -name '*.h' -perm /111 | \
	xargs --no-run-if-empty chmod -x

echo "Options:" >help_swig
%{buildroot}%{_bindir}/swig --help >>help_swig

sed -i -e 's/^\(\s\+-[^-]\+\)- \(.*\)$/\1 \2/' help_swig
sed -i -e 's/^\(\s\+-\w\+-[^-]*\)- \(.*\)$/\1 \2/' help_swig

cat >h2m_helper_swig <<'EOF'
[ "$1" == "--version" ] && echo "" || cat help_swig
EOF
chmod a+x h2m_helper_swig

help2man -N --section 1 ./h2m_helper_swig --include %{SOURCE1} -o %{name}.1

mkdir -p %{buildroot}%{_mandir}/man1/
install -p -m 0644 %{name}.1 %{buildroot}%{_mandir}/man1/

install -d %{buildroot}%{_datadir}/%{name}/gdb
install -pm 644 Tools/swig.gdb %{buildroot}%{_datadir}/%{name}/gdb

%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/examples
%license LICENSE LICENSE-GPL LICENSE-UNIVERSITIES

%doc COPYRIGHT
%exclude %{_datadir}/%name/%{version}/octave/std_carray.i

%files help
%license LICENSE LICENSE-GPL LICENSE-UNIVERSITIES
%doc Doc/{Devel,Manual} README TODO
%{_datadir}/%{name}/examples
%doc ANNOUNCE CHANGES CHANGES.current
%{_mandir}/man1/swig.1*

%changelog
* Thu Jul 13 2023 chenchen <chen_aka_jan@163.com> - 4.0.2-6
- fix build error caused by upgrading gcc to 12.3.0

* Mon Jun 05 2023 misaka00251 <liuxin@iscas.ac.cn> - 4.0.2-5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:Backport php 8 support from upstream

* Thu Jun 9 2022 zoulin <zoulin13@h-partners.com> - 4.0.2-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:Modify the dependency from pcre to pcre2

* Tue Apr 20 2021 panxiaohe <panxiaohe@huawei.com> - 4.0.2-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:use make macros to run check in parallel

* Tue Feb 23 2021 licihua <licihua@huawei.com> - 4.0.2-2
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:Move make check stage to %check

* Thu Jul 23 2020 shixuantong <shixuantong@huawei.com> - 4.0.2-1
- update to 4.0.2-1

* Fri Nov 29 2019 wutao <wutao61@huawei.com> - 3.0.12-22
- Package init
