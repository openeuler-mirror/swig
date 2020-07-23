Name:          swig
Version:       4.0.2
Release:       1
Summary:       Links C/C++/Objective C to languages for some advanced programing
License:       GPLv3+ and BSD
URL:           http://swig.sourceforge.net/
Source0:       http://downloads.sourceforge.net/project/swig/swig/swig-%{version}/swig-%{version}.tar.gz
Source1:       description.h2m

BuildRequires: perl-interpreter pcre-devel python3-devel autoconf automake gawk dos2unix
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

make check

%install
make clean-examples

cd Examples/
find -type f -name 'Makefile.in' -delete -print

rm -rf test-suite
find -type f -name '*.dsp' -delete -print
find -type f -name '*.dsw' -delete -print

for all in `find -type f`; do
    dos2unix -k $all
    chmod -x $all
done
cd -

%make_install

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
%license LICENSE LICENSE-GPL LICENSE-UNIVERSITIES
%doc COPYRIGHT
%exclude %{_datadir}/%name/%{version}/octave/std_carray.i

%files help
%license LICENSE LICENSE-GPL LICENSE-UNIVERSITIES
%doc Doc Examples README TODO
%doc ANNOUNCE CHANGES CHANGES.current
%{_mandir}/man1/swig.1*

%changelog
* Thu Jul 23 2020 shixuantong <shixuantong@huawei.com> - 4.0.2-1
- update to 4.0.2-1

* Fri Nov 29 2019 wutao <wutao61@huawei.com> - 3.0.12-22
- Package init
