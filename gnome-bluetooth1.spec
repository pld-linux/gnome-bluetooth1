#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	GNOME Bluetooth Subsystem
Summary(pl.UTF-8):	Podsystem GNOME Bluetooth
Name:		gnome-bluetooth1
# keep 3.x here as gnome-bluetooth-1.0 API
Version:	3.34.5
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-bluetooth/3.34/gnome-bluetooth-%{version}.tar.xz
# Source0-md5:	d83faa54abaf64bb40b5313bc233e74e
Patch0:		gnome-bluetooth-meson.patch
URL:		https://wiki.gnome.org/Projects/GnomeBluetooth
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.38.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk+3-devel >= 3.12.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.9}
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libxml2-progs
BuildRequires:	meson >= 0.49.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Bluetooth provides tools for controlling and communicating with
Bluetooth devices.

%description -l pl.UTF-8
GNOME Bluetooth dostarcza narzędzia do kontrolowania i komunikowania
się z urządzeniami Bluetooth.

%package libs
Summary:	GNOME Bluetooth 1.0 subsystem shared libraries
Summary(pl.UTF-8):	Współdzielone biblioteki dla podsystemu GNOME Bluetooth 1.0
License:	LGPL v2+
Group:		X11/Libraries
Requires:	glib2 >= 1:2.38.0
Requires:	gtk+3 >= 3.12.0
Requires:	libnotify >= 0.7.0
Obsoletes:	gnome-bluetooth-libs < 3.35

%description libs
GNOME Bluetooth 1.0 subsystem shared libraries.

%description libs -l pl.UTF-8
Współdzielone biblioteki dla podsystemu GNOME Bluetooth.

%package devel
Summary:	Header files for GNOME Bluetooth 1.0 subsystem
Summary(pl.UTF-8):	Pliki nagłówkowe dla podsystemu GNOME Bluetooth 1.0
License:	LGPL v2+
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.38.0
Requires:	gtk+3-devel >= 3.12.0
Obsoletes:	gnome-bluetooth-devel < 3.35
Obsoletes:	gnome-bluetooth-static < 3.32

%description devel
Header files for GNOME Bluetooth 1.0 subsystem.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla podsystemu GNOME Bluetooth 1.0.

%package apidocs
Summary:	GNOME Bluetooth 1.0 library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki GNOME Bluetooth 1.0
Group:		Documentation
Obsoletes:	gnome-bluetooth-apidocs < 3.35
BuildArch:	noarch

%description apidocs
GNOME Bluetooth 1.0 library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GNOME Bluetooth 1.0.

%prep
%setup -q -n gnome-bluetooth-%{version}
%patch -P0 -p1

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true} \
	-Dicon_update=false

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# keep just library and used data
%{__rm} $RPM_BUILD_ROOT%{_bindir}/bluetooth-sendto \
	$RPM_BUILD_ROOT%{_desktopdir}/bluetooth-sendto.desktop \
	$RPM_BUILD_ROOT%{_mandir}/man1/bluetooth-sendto.1
%{__rm} -r $RPM_BUILD_ROOT%{_iconsdir}/hicolor

%find_lang gnome-bluetooth2

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files libs -f gnome-bluetooth2.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README.md
%attr(755,root,root) %{_libdir}/libgnome-bluetooth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-bluetooth.so.13
%{_libdir}/girepository-1.0/GnomeBluetooth-1.0.typelib
# used from lib/pin.c
%{_datadir}/gnome-bluetooth

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-bluetooth.so
%{_includedir}/gnome-bluetooth
%{_pkgconfigdir}/gnome-bluetooth-1.0.pc
%{_datadir}/gir-1.0/GnomeBluetooth-1.0.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-bluetooth
%endif
