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
Version:	3.9.12
Release:	%mkrel 2
License:	GPLv2+ and MIT
Group:		System/Printing
Source: http://heanet.dl.sourceforge.net/sourceforge/hplip/%{name}-%{version}%{extraversion}.tar.gz
# Taken from Fedora, ensures correct permissions on devices
Source1: hplip.fdi
# dlopen libhpmud.so.0 instad of libhpmud.so, in order not to depend on
# devel package (http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=548379)
Patch0:	hplip-3.9.8-dlopen-libhpmud.patch

# Fedora patches
Patch102: hplip-strstr-const.patch
Patch103: hplip-ui-optional.patch
Patch104: hplip-no-asm.patch
Patch110: hplip-discovery-method.patch
Patch111: hplip-device-reconnected.patch
Patch114: hplip-hpcups-sigpipe.patch

# Debian/Ubuntu patches
Patch202: hplip-hpinfo-query-without-cups-queue.patch
Patch203: hplip-pjl-duplex-binding.patch
Patch204: hplip-photosmart_b9100_support.patch
Patch205: hplip-rebuild_python_ui.patch
Patch206: hplip-rss.patch
Patch207: hplip-2.7.6-14_charsign_fixes.patch
Patch208: 10_shebang_fixes.dpatch
Patch210: 87_move_documentation.dpatch
Patch211: hp-check_debian.dpatch
Patch212: delayed-hp-systray-start.dpatch


Url:		http://hplip.sourceforge.net/
%if %{sane_backend}
BuildRequires:	libsane-devel, xsane
%endif
%py_requires -d
BuildRequires:	python-sip >= 4.1.1
BuildRequires:	net-snmp-devel
BuildRequires:	libusb-devel >= 0.1.8
BuildRequires:	imagemagick
BuildRequires:	autoconf
BuildRequires:	libcups-devel
BuildRequires:	libjpeg-devel
BuildRequires:	python-devel
BuildRequires:	desktop-file-utils
BuildRequires:	libdbus-devel
BuildRequires:	udev-devel
BuildRequires:	polkit
BuildRequires:	gphoto2-devel
Requires:	cups
# For dynamic ppd generation.
Requires:	cupsddk-drivers >= 1.2.3-2mdv
Requires:	foomatic-filters
Requires:	hplip-model-data hplip-hpijs
Requires:	hplip-hpijs-ppds
Requires:	python-sip >= 4.1.1
# Needed for communicating with ethernet-connected printers
Requires:	net-snmp-mibs
# Needed to generate fax cover pages
Requires:	python-reportlab
# Needed since 2.8.4 for IPC
Requires:	python-dbus
Requires:	polkit-agent
Requires:	usermode-consoleonly
# Required by hp-scan for command line scanning
Suggests:	python-imaging
# Some HP ppds are in foomatic-db and foomatic-db-hpijs (bug #47415)
Suggests:	foomatic-db-hpijs

%ifarch x86_64
Conflicts:	cups < 1.2.0-0.5361.0mdk
%endif
# Due to fax ppds.
Conflicts:	hplip-hpijs-ppds <= 2.8.2-1mdv
# foomatic-db-hpijs drivers are provided by hp and by this package now
# NOTE: remove the foomatic-db-hpijs deps sometime in 2010-10-?? ?
Provides:	foomatic-db-hpijs = %{version}-%{release}
Obsoletes:	foomatic-db-hpijs
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

%package gui
Summary: HPLIP graphical tools
Group: System/Printing
Requires:python-qt4-gui
Requires: %{name} = %{version}-%{release}
Requires: usermode
Conflicts: hplip < 2.8.12-4

%description gui
HPLIP graphical tools.


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

%patch0 -p1 -b .dlopen

# Fedora patches
# Fix compilation.
%patch102 -p1 -b .strstr-const

# Make utils.checkPyQtImport() look for the gui sub-package (RH bug #243273).
%patch103 -p1 -b .ui-optional

# Make sure to avoid handwritten asm.
%patch104 -p1 -b .no-asm

# Fixed hp-setup traceback when discovery page is skipped (RH bug #523685).
%patch110 -p1 -b .discovery-method

# Give up trying to print a job to a reconnected device (RH bug #515481).
%patch111 -p1 -b .device-reconnected

# Avoid busy loop in hpcups when backend has exited (RH bug #525944).
%patch114 -p1 -b .hpcups-sigpipe

# Debian/Ubuntu patches

# Allow hp-info to query URIs for which there is no CUPS queue
# (Launchpad bug #329220)
%patch202 -p1 -b .query

# FixsShort-edge duplex printing if duplex is PJL-controlled
# https://bugs.launchpad.net/hplip/+bug/244295
%patch203 -p1 -b .pjl-duplex

# Corrections on the models.dat entry for the HP PhotoSmart Pro B9100,
# especially for the correct color calibration mode.
%patch204 -p1 -b .b9100

# compiling ui files to py
%patch205 -p1 -b .rebuildui

# This patch tries to make sure that black is printed with just
# the black pen, if the printer supports it
%patch206 -p1 -b .rss

# code cleanup related to char signedness
%patch207 -p1 -b .14charsign

# shebang fixes
%patch208 -p1

# place html documentation under hplip-doc/HTML/
%patch210 -p1

# Check for hpaio module in /etc/sane.d/dll.d/hplip too
%patch211 -p1

# Delay start-up of notification utility
%patch212 -p1

# Make all files in the source user-writable
chmod -R u+w .

%build
%serverbuild
#needed by patch205
libtoolize --copy --force
aclocal --force
autoconf -f
#needed by patches 205 and 210
automake -f --foreign

%if !%{sane_backend}
WITHOUT_SANE="--without-sane"
%endif
%configure2_5x $WITHOUT_SANE \
	--disable-foomatic-rip-hplip-install \
	--enable-scan-build \
	--enable-gui-build \
	--enable-fax-build \
	--enable-pp-build \
	--enable-qt4 --disable-qt3 \
	--enable-hpcups-install \
	--enable-cups-drv-install \
	--enable-cups-ppd-install \
	--enable-hpijs-install \
	--enable-udev-acl-rules \
	--enable-policykit

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

# convert icons to required sizes
#convert data/images/print.png -resize 16x16 %{name}.mini.png
#convert data/images/print.png -resize 32x32 %{name}.png
#convert data/images/print.png -resize 48x48 %{name}.large.png

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
#mkdir -p %{buildroot}%{_iconsdir}/locolor/16x16/apps/
#install -m 644 %{name}.png -D %{buildroot}%{_iconsdir}/%{name}.png
#install -m 644 %{name}.mini.png -D %{buildroot}%{_miconsdir}/%{name}.png
#install -m 644 %{name}.large.png -D %{buildroot}%{_liconsdir}/%{name}.png

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
	--remove-key='Version' \
        %{buildroot}%{_datadir}/applications/hplip.desktop

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-hp-sendfax.desktop << EOF
[Desktop Entry]
Name=HP Sendfax
Comment=Utility for sending faxes with HP's multi-function devices
Exec=%{_bindir}/hp-sendfax
Icon=%{_datadir}/%{name}/data/images/32x32/fax_machine.png
Terminal=false
Type=Application
Categories=TelephonyTools;Qt;Printing;Utility;X-MandrivaLinux-CrossDesktop;
EOF
#' #Fix vim's stupid syntax

rm -f %{buildroot}%{_sysconfdir}/xdg/autostart/hplip-systray.desktop

# switched to udev, no need for hal information
rm -rf %{buildroot}%{_datadir}/hal/fdi

# set up consolehelper
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/hp-setup %{buildroot}%{_sbindir}/hp-setup
ln -s consolehelper %{buildroot}%{_bindir}/hp-setup

# Make sure pyc files are generated, otherwise we can get
# difficult to debug problems
pushd %{buildroot}%{_datadir}/%{name}
python -m compileall .
popd

%triggerin -- hplip < 2.7.7
chkconfig --del hplip

%post
%if %mdkversion < 200900
%{update_menus}
%endif
# Restart CUPS to make the Fax PPD known to it
if [ -f /etc/init.d/cups ]; then
	/sbin/service cups condrestart || :
fi

%post -n hplip-hpijs-ppds
# Restart CUPS to make the printing PPDs known to it
if [ -f /etc/init.d/cups ]; then
	/sbin/service cups condrestart || :
fi

%post -n hplip-model-data
/sbin/udevadm trigger --subsystem-match=usb --attr-match=idVendor=03f0

%if %mdkversion < 200900
%post -n %{hpip_libname} -p /sbin/ldconfig
%endif

%if %{sane_backend}
%post -n %{sane_hpaio_libname}
%if %mdkversion < 200900
/sbin/ldconfig
%endif
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
%if %mdkversion < 200900
%{update_menus}
%endif
# Restart CUPS to make the removal of the Fax PPD known to it
if [ -f /etc/init.d/cups ]; then
	/sbin/service cups condrestart || :
fi

%postun -n hplip-hpijs-ppds
# Restart CUPS to make the removal of the printing PPDs known to it
if [ -f /etc/init.d/cups ]; then
	/sbin/service cups condrestart || :
fi

%if %mdkversion < 200900
%postun -n %{hpip_libname} -p /sbin/ldconfig
%endif

%if %{sane_backend}
%postun -n %{sane_hpaio_libname}
%if %mdkversion < 200900
/sbin/ldconfig
%endif
%endif


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
#doc COPYING doc/*
%config(noreplace) %{_sysconfdir}/hp
%dir /var/run/hplip/
%{_bindir}/hp-align
%{_bindir}/hp-clean
%{_bindir}/hp-colorcal
%{_bindir}/hp-devicesettings
%{_bindir}/hp-fab
%{_bindir}/hp-faxsetup
%{_bindir}/hp-firmware
%{_bindir}/hp-info
%{_bindir}/hp-levels
%{_bindir}/hp-linefeedcal
%{_bindir}/hp-makecopies
%{_bindir}/hp-makeuri
%{_bindir}/hp-mkuri
%{_bindir}/hp-pkservice
%{_bindir}/hp-plugin
%{_bindir}/hp-pqdiag
%{_bindir}/hp-printsettings
%{_bindir}/hp-probe
%{_bindir}/hp-query
%{_bindir}/hp-scan
%{_bindir}/hp-sendfax
%{_bindir}/hp-setup
%{_sbindir}/hp-setup
%{_bindir}/hp-testpage
%{_bindir}/hp-timedate
%{_bindir}/hp-unload
%{_bindir}/hp-wificonfig

%exclude %{_datadir}/hplip/data/models
# C libraries for Python
%{_libdir}/python*/*/*.so*
# CUPS backends (0700 permissions, so that CUPS 1.2 runs these backends
# as root)
# Note: this must be /usr/lib not %{_libdir}, since that's the
# CUPS serverbin directory.
%attr(0700,root,root) %{_prefix}/lib/cups/backend/hp*
%{_prefix}/lib/cups/filter/hplipjs
%{_prefix}/lib/cups/filter/hpcac
%{_prefix}/lib/cups/filter/hpcups
%{_prefix}/lib/cups/filter/hpcupsfax
%{_datadir}/ppd/HP/HP-Fax*.ppd*
%{_datadir}/cups/drv/hp/hpcups.drv
# Files
%dir %{_datadir}/hplip
%{_datadir}/hplip/align.py*
%{_datadir}/hplip/clean.py*
%{_datadir}/hplip/colorcal.py*
%{_datadir}/hplip/devicesettings.py*
%{_datadir}/hplip/fab.py*
%{_datadir}/hplip/fax
%{_datadir}/hplip/faxsetup.py*
%{_datadir}/hplip/firmware.py*
%{_datadir}/hplip/hpdio.py*
%{_datadir}/hplip/hpssd*
%{_datadir}/hplip/info.py*
%{_datadir}/hplip/__init__.py*
%{_datadir}/hplip/levels.py*
%{_datadir}/hplip/linefeedcal.py*
%{_datadir}/hplip/makecopies.py*
%{_datadir}/hplip/makeuri.py*
%{_datadir}/hplip/pkservice.py*
%{_datadir}/hplip/plugin.py*
%{_datadir}/hplip/pqdiag.py*
%{_datadir}/hplip/printsettings.py*
%{_datadir}/hplip/probe.py*
%{_datadir}/hplip/query.py*
%{_datadir}/hplip/scan.py*
%{_datadir}/hplip/sendfax.py*
%{_datadir}/hplip/setup.py*
%{_datadir}/hplip/testpage.py*
%{_datadir}/hplip/timedate.py*
%{_datadir}/hplip/unload.py*
%{_datadir}/hplip/wificonfig.py*
# Directories
%{_datadir}/hplip/base
%{_datadir}/hplip/copier
%dir %{_datadir}/hplip/data
%{_datadir}/hplip/data/ldl
%{_datadir}/hplip/data/localization
%{_datadir}/hplip/data/models
%{_datadir}/hplip/data/pcl
%{_datadir}/hplip/data/ps
%{_datadir}/hplip/installer
%{_datadir}/hplip/pcard
%{_datadir}/hplip/prnt
%{_datadir}/hplip/scan
%{_datadir}/polkit-1/actions/com.hp.hplip.policy
%{_datadir}/dbus-1/system-services/com.hp.hplip.service
%{_localstatedir}/lib/hp/hplip.state
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/com.hp.hplip.conf

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
%{_sysconfdir}/udev/rules.d/*.rules
%{_datadir}/hplip/data/models

%files gui
%{_bindir}/hp-check
%{_bindir}/hp-print
%{_bindir}/hp-systray
%{_bindir}/hp-toolbox
%{_datadir}/applications/*.desktop
# Files
%{_datadir}/hplip/check.py*
%{_datadir}/hplip/print.py*
%{_datadir}/hplip/systray.py*
%{_datadir}/hplip/toolbox.py*
# Directories
%{_datadir}/hplip/data/images
%{_datadir}/hplip/ui4

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
