# Define if you want to build the sane backend (default)
%define sane_backend		1
%{?_with_sane:			%global sane_backend 1}
%{?_without_sane:		%global sane_backend 0}

%define hpip_major		0
%define hpip_libname		%mklibname hpip %{hpip_major}

%define sane_hpaio_major	1
%define sane_hpaio_libname	%mklibname sane-hpaio %{sane_hpaio_major}

# Suppress automatically generated Requires for devel packages
%define _requires_exceptions devel\(.*\)

#define extraversion -RC1
%define extraversion %nil

Summary:	HP printer/all-in-one driver infrastructure
Name:		hplip
Version:	2.8.2
Release:	%mkrel 2
License:	GPL/MIT/BSD
Group:		System/Printing
Source: http://heanet.dl.sourceforge.net/sourceforge/hplip/%{name}-%{version}%{extraversion}.tar.gz
# Some HP PhotoSmart 7150 identify themselves as "hp photosmart 7150~"
Patch3: hplip-1.6.12-HP-PhotoSmart_7150tilde.patch
Patch11: hplip-2.7.6-14_charsign_fixes.patch
# Patch100: official patch
# fwang: Patch 101-108 from fedora
Patch101: hplip-2.7.6-libm.patch
Patch102: hplip-2.7.6-libsane.patch
Patch105: hplip-2.7.6-no-root-config.patch
Patch106: hplip-2.7.6-quiet-startup.patch
Patch107: hplip-2.7.6-unload-traceback.patch
Patch108: hplip-2.7.7-desktop.patch
Url:		http://hplip.sourceforge.net/
%if %{sane_backend}
BuildRequires:	libsane-devel, xsane
%endif
%py_requires -d
BuildRequires:	PyQt >= 3.13-2mdk, python-sip >= 4.1.1
BuildRequires:	net-snmp-devel
BuildRequires:	libusb-devel >= 0.1.8
BuildRequires:	ImageMagick
BuildRequires:	autoconf
BuildRequires:	libcups-devel
BuildRequires:	libjpeg-devel
BuildRequires:	python-devel
BuildRequires:	desktop-file-utils
Requires:	PyQt >= 3.13-2mdk
Requires:	cups
# For dynamic ppd generation.
Requires:	cupsddk-drivers >= 1.2.3-2mdv
Requires:	foomatic-filters
Requires:	hplip-model-data hplip-hpijs
Requires:	python-sip >= 4.1.1
# Needed for communicating with ethernet-connected printers
Requires:	net-snmp-mibs
# Needed to generate fax cover pages
Requires:	python-reportlab
%ifarch x86_64
Conflicts:	cups < 1.2.0-0.5361.0mdk
%endif
# Due to fax ppds.
Conflicts:	hplip-hpijs-ppds <= 2.8.2-1mdv
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This is the HP driver package to supply Linux support for most
Hewlett-Packard DeskJet, LaserJet, PSC, OfficeJet, and PhotoSmart
printers and all-in-one peripherals (also known as Multi-Function
Peripherals or MFPs), which can print, scan, copy, fax, and/or access
flash memory cards.

It is work in progress, but printing, scanning, memory card access,
ink/toner/battery/consumable level checking, and inkjet printer
maintenance are supported on most models, when either connected to the
USB or LAN (built-in interfaces or selected HP JetDirect models) on a
Linux workstation with CUPS printing system.

For status and consumable checking and also for inkjet maintenance
there is the graphical tool "hp-toolbox" available (Menu:
"System"/"Monitoring"/"HP Printer Toolbox").

%package -n %{hpip_libname}
Summary: Dynamic library for the "hplip" HP printer/all-in-one drivers
Group: System/Printing

%description -n %{hpip_libname}
Library needed for the "hplip" HP printer/all-in-one drivers

%package -n %{hpip_libname}-devel
Summary: Headers and links to compile against the "%{hpip_libname}" ("hplip") library
Group: Development/C
Requires: %{hpip_libname} >= %{version}-%{release}
Provides: libhpip-devel = %{version}-%{release}

%description -n %{hpip_libname}-devel
This package contains all files which one needs to compile programs using
the "%{hpip_libname}" library.

%if %{sane_backend}
%package -n %{sane_hpaio_libname}
Summary: SANE driver for scanners in HP's multi-function devices (from HPLIP)
Group: System/Printing
Requires: sane-backends
%define _requires_exceptions devel(libcrypto)\\|devel(libdl)\\|devel(libhpip)\\|devel(libm)\\|devel(libsnmp)
%endif

%if %{sane_backend}
%description -n %{sane_hpaio_libname}
SANE driver for scanners in HP's multi-function devices (from HPLIP)
%endif

%if 0
%if %{sane_backend}
%package -n %{sane_hpaio_libname}-devel
Summary: Headers and links to compile against the "%{sane_hpaio_libname}" ("sane-hpaio") library
Group: Development/C
Requires: %{sane_hpaio_libname} >= %{version}-%{release}
Provides: libsane-hpaio-devel = %{version}-%{release}
%endif

%if %{sane_backend}
%description -n %{sane_hpaio_libname}-devel
This package contains all files which one needs to compile programs using
the "%{sane_hpaio_libname}" library.
%endif
%endif

%package model-data
Summary: Data file listing the HP printer models supported by HPLIP
Group: System/Printing

%description model-data
HPLIP supports most current HP printers and multifunction devices, but
there are some older models not supported. This package contains the
list of supported models. Printerdrake installs it automatically to
determine whether HPLIP has to be installed or not.

%package hpijs
Summary: HPs printer driver IJS plug-in for GhostScript
Group: System/Printing
Requires: ghostscript
Provides: hpijs
Conflicts: printer-filters < 10.2
Conflicts: hplip <= 1.6.7-1mdv2007.0

%description hpijs
HPs printer driver IJS plug-in for GhostScript. This driver gives full
printing support for nearly all non-PostScript inkjet and laser
printers made by HP.

%package hpijs-ppds
Summary: PPD files for the HPIJS printer driver
Group: System/Printing
Requires: foomatic-filters, hplip-hpijs

%description hpijs-ppds
PPD files to use the HPIJS printer driver with foomatic-rip and a
printer spooler like CUPS, LPRng, PDQ, ...

%package doc
Summary:	Documentation for HPLIP
Group:		System/Printing

%description doc
This package contains documentation for the HPLIP driver.

This is the HP driver package to supply Linux support for most
Hewlett-Packard DeskJet, LaserJet, PSC, OfficeJet, and PhotoSmart
printers and all-in-one peripherals (also known as Multi-Function
Peripherals or MFPs), which can print, scan, copy, fax, and/or access
flash memory cards.

%prep
rm -rf $RPM_BUILD_DIR/%{name}-%{version}%{extraversion}
%setup -q -n %{name}-%{version}%{extraversion}

# Some HP PhotoSmart 7150 identify themselves as "hp photosmart 7150~"
%patch3 -p1 -b .hpps7150

%patch11 -p1 -b .14charsign

# apply fedora patches
%patch101 -p1
%patch102 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1

# fix for gentoo bug#161926, to be fixed in upstream 2.7.7
sed -i -e "s:if (!localOnly):if (1):" scan/sane/hpaio.c

# Make all files in the source user-writable
chmod -R u+w .

%build
%serverbuild

aclocal
autoconf
%if !%{sane_backend}
WITHOUT_SANE="--without-sane"
%endif
%configure2_5x $WITHOUT_SANE \
	--disable-foomatic-rip-hplip-install \
	--disable-foomatic-xml-install

%make

# convert icons to required sizes
convert data/images/print.png -resize 16x16 %{name}.mini.png
convert data/images/print.png -resize 32x32 %{name}.png
convert data/images/print.png -resize 48x48 %{name}.large.png

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/hp
mkdir -p %{buildroot}/var/run/hplip

# Do not use the macro here, use the standard DESTDIR method as it works
# with HPLIP, in contrary to the non-standard Mandriva method
#make test-destdir DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}

# Install files which the "make install" missed to install
install -m 644 ip/hpip.h %{buildroot}%{_includedir}
install -m 644 ip/xform.h %{buildroot}%{_includedir}

# Move doc in sub-package
mv %{buildroot}%{_docdir}/%{name}-%{version}%{extraversion} %{buildroot}%{_docdir}/%{name}-doc-%{version}%{extraversion}

# Remove static libraries of SANE driver
rm -f %{buildroot}%{_libdir}/sane/libsane-hpaio*.so
rm -f %{buildroot}%{_libdir}/sane/libsane-hpaio*.la
rm -f %{buildroot}%{_sysconfdir}/sane.d/dll.conf

# Remove other unneeded files
rm -f %{buildroot}%{py_platsitedir}/*.la

# install menu icons
mkdir -p %{buildroot}%{_iconsdir}/locolor/16x16/apps/
install -m 644 %{name}.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 %{name}.mini.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 %{name}.large.png -D %{buildroot}%{_liconsdir}/%{name}.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor='' \
	--dir=%{buildroot}%{_datadir}/applications \
	--remove-category='Application' \
	--remove-category='Utility' \
	--add-category='System' \
	--add-category='Settings' \
	--add-category='Printing' \
        --add-category='Qt' \
        --add-category='HardwareSettings' \
        --add-category='X-MandrivaLinux-CrossDesktop' \
	%{buildroot}%{_datadir}/applications/hplip.desktop

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-hp-sendfax.desktop << EOF
[Desktop Entry]
Name=HP Sendfax
Comment=Utility for sending faxes with HP's multi-function devices
Exec=%{_bindir}/hp-sendfax
Icon=%{name}
Terminal=false
Type=Application
Categories=TelephonyTools;Qt;Printing;Utility;X-MandrivaLinux-CrossDesktop;
EOF
#' #Fix vim's stupid syntax

%triggerin -- hplip < 2.7.7
chkconfig --del hplip

%post
# Menu update
%{update_menus}
# Restart CUPS to make the Fax PPD known to it
/sbin/service cups condrestart || :

%post -n hplip-hpijs-ppds
# Restart CUPS to make the printing PPDs known to it
/sbin/service cups condrestart || :

# Reload the library lists when installing shared libraries
%post -n %{hpip_libname} -p /sbin/ldconfig

%if %{sane_backend}
%post -n %{sane_hpaio_libname}
/sbin/ldconfig
# Add HPLIP driver to /etc/sane.d/dll.conf
if ! grep ^hpaio /etc/sane.d/dll.conf >/dev/null 2>/dev/null ; then \
	echo hpaio >> /etc/sane.d/dll.conf; \
fi
%endif

%if %{sane_backend}
%preun -n %{sane_hpaio_libname}
# Remove HPLIP driver from /etc/sane.d/dll.conf
if [ "$1" = 0 ]; then \
	if grep ^hpaio /etc/sane.d/dll.conf >/dev/null 2>/dev/null ; then \
		sed '/hpaio/d' /etc/sane.d/dll.conf > /tmp/$$; \
		cp -f /tmp/$$ /etc/sane.d/dll.conf; \
		rm -f /tmp/$$; \
	fi; \
fi
%endif

%postun
## Menu update
%{update_menus}
# Restart CUPS to make the removal of the Fax PPD known to it
/sbin/service cups condrestart || :

%postun -n hplip-hpijs-ppds
# Restart CUPS to make the removal of the printing PPDs known to it
/sbin/service cups condrestart || :

# Reload the library lists when uninstalling shared libraries
%postun -n %{hpip_libname} -p /sbin/ldconfig

%if %{sane_backend}
%postun -n %{sane_hpaio_libname}
/sbin/ldconfig
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
#doc COPYING doc/*
%config(noreplace) %{_sysconfdir}/hp
%config(noreplace) %{_sysconfdir}/udev/rules.d/55-hpmud.rules
%dir /var/run/hplip/
%{_bindir}/hp-*
%{_datadir}/hplip/[A-Za-c_]*
%{_datadir}/hplip/data/*
%exclude %{_datadir}/hplip/data/models
%{_datadir}/hplip/[e-z]*
# C libraries for Python
%{_libdir}/python*/*/*.so*
# CUPS backends (0700 permissions, so that CUPS 1.2 runs these backends
# as root)
%attr(0700,root,root) %{_prefix}/lib*/cups/backend/hp*
%{_datadir}/cups/drv/hp/hpijs.drv
%{_datadir}/ppd/HP/HP-Fax*.ppd*
# menu entry
%{_iconsdir}/*.png
%{_iconsdir}/*/*.png
%{_datadir}/applications/*

%files doc
%defattr(-,root,root)
%doc %{_docdir}/%{name}-doc-%{version}%{extraversion}

%files -n %{hpip_libname}
%defattr(-,root,root)
%{_libdir}/libhpip*.so.*
%{_libdir}/libhpmud.so.*

%files -n %{hpip_libname}-devel
%defattr(-,root,root)
%{_includedir}/hpip.h
%{_includedir}/xform.h
%{_libdir}/libhpip*.so
%{_libdir}/libhpip*.la
%{_libdir}/libhpmud.so
%{_libdir}/libhpmud.la

%if %{sane_backend}

%files -n %{sane_hpaio_libname}
%defattr(-,root,root)
%{_libdir}/sane/libsane-hpaio*.so.*

%if 0
%files -n %{sane_hpaio_libname}-devel
%defattr(-,root,root)
#%{_libdir}/libsane-hpaio*.so
#%{_libdir}/libsane-hpaio*.a
#%{_libdir}/libsane-hpaio*.la
#%{_libdir}/sane/libsane-hpaio*.so
#%{_libdir}/sane/libsane-hpaio*.a
#%{_libdir}/sane/libsane-hpaio*.la
%endif

%endif

%files model-data
%defattr(-,root,root)
%{_datadir}/hplip/data/models

%files hpijs
%defattr(-,root,root)
%{_bindir}/hpijs
# Needed for both printing and fax PPDs. They all need HPIJS, therefore
# the link is here
%dir %{_datadir}/ppd
%dir %{_datadir}/ppd/HP

%files hpijs-ppds
%defattr(-,root,root)
%{_datadir}/ppd/HP/*.ppd*
%exclude %{_datadir}/ppd/HP/HP-Fax*.ppd*
