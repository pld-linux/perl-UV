#
# Conditional build:
%bcond_with	system_libuv	# use system libuv [not ready for 1.x]
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	UV
%include	/usr/lib/rpm/macros.perl
Summary:	UV - Perl interface to libuv
Summary(pl.UTF-8):	UV - perlowy interfejs do libuv
Name:		perl-UV
Version:	0.24
Release:	2
License:	MIT
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/T/TY/TYPESTER/%{pdir}-%{version}.tar.gz
# Source0-md5:	826db3b5609cfafe59030347579f6e54
Patch0:		%{name}-system-libuv.patch
URL:		http://search.cpan.org/dist/UV/
%{?with_system_libuv:BuildRequires:	libuv-devel >= 0.10}
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Test-TCP
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
UV provides low-level interface to libuv,
<https://github.com/joyent/libuv>, platform layer for Node.js.

Low-level means this module's functions maps to libuv functions
directly. uv_listen maps to UV::listen, uv_tcp_connect to
UV::tcp_connect, and so on.

%description -l pl.UTF-8
Moduł UV udostępnia niskopoziomowy interfejs do biblioteki libuv
(<https://github.com/joent/libuv>) - zależnej od platformy warstwy
Node.js.

Niskopoziomowość oznacza, że funkcje tego modułu odwzorowują się
bezpośrednio na funkcje libuv. uv_listen odwzorowuje się na
UV::listen, uv_tcp_connect na UV::tcp_connect itd.

%prep
%setup -q -n %{pdir}-%{version}
%if %{with system_libuv}
%patch0 -p1
%endif

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a example $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes LICENSE README.md
%{perl_vendorarch}/UV.pm
%dir %{perl_vendorarch}/auto/UV
%attr(755,root,root) %{perl_vendorarch}/auto/UV/UV.so
%{_mandir}/man3/UV.3pm*
%{_examplesdir}/%{name}-%{version}
