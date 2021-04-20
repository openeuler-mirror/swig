Name:          swig
Version:       3.0.12
Release:       25
Summary:       Links C/C++/Objective C to languages for some advanced programing
License:       GPLv3+ and BSD
URL:           http://swig.sourceforge.net/
Source0:       http://downloads.sourceforge.net/project/swig/swig/swig-%{version}/swig-%{version}.tar.gz
Source1:       description.h2m

Patch0001:     swig308-Do-not-use-isystem.patch
Patch0002:     swig-3.0.12-Fix-testsuite-to-work-without-.-in-INC.patch
#https://patch-diff.githubusercontent.com/raw/swig/swig/pull/968/swig-node-v7.patch
Patch0003:     swig-node-v7.patch
Patch0004:     swig-3.0.12-Fix-generated-code-for-constant-expressions-containi.patch
Patch0005:     swig-3.0.12-Fix-type-promotion-wrapping-some-non-trivial-constan.patch
Patch0006:     swig-3.0.12-Correct-php-testcase.patch
Patch0007:     swig-3.0.12-Fix-go-version-matching-in-configure-for-go1.10.patch
Patch0008:     swig-3.0.12-Coverity-fix-issue-reported-for-SWIG_Python_FixMetho.patch
Patch0009:     swig-3.0.12-Fix-Coverity-issue-reported-for-setslice-pycontainer.patch
Patch0010:     swig-3.0.12-Coverity-fix-issue-reported-for-wrapper-argument-che.patch
Patch0011:     swig-3.0.12-Coverity-fix-issue-reported-for-SWIG_Python_ConvertF.patch

BuildRequires: perl-interpreter pcre-devel python3-devel autoconf automake gawk dos2unix
BuildRequires: gcc-c++ help2man perl-devel perl(base) perl(Config) perl(Devel::Peek)
BuildRequires: perl(ExtUtils::MakeMaker) perl(fields) perl(Math::BigInt) perl(strict)
BuildRequires: perl(Test::More) perl(vars) perl(warnings) boost-devel bison tcl-devel
BuildRequires: lua-devel ruby-devel

Provides:      %{name}-gdb = %{version}-%{release}
Obsoletes:     %{name}-gdb < %{version}-%{release}
Requires:      %{name}-help = %{version}-%{release}


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
* Tue Apr 20 2021 panxiaohe <panxiaohe@huawei.com> - 3.0.12-25
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:use make macros to run check in parallel

* Tue Feb 23 2021 licihua <licihua@huawei.com> - 3.0.12-24
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:Move make check stage to %check

* Fri Nov 06 2020 liuweibo <liuweibo10@huawei.com> - 3.0.12-23
- append help requires to swig

* Fri Nov 29 2019 wutao <wutao61@huawei.com> - 3.0.12-22
- Package init
