# Define if you want to build the sane backend (default)
%define sane_backend 1
%{?_with_sane: %global sane_backend 1}
%{?_without_sane: %global sane_backend 0}

%define major 0
%define libhpip %mklibname hpip %{major}
%define libhpipp %mklibname hpipp %{major}
%define libhpmud %mklibname hpmud %{major}
%define sanemaj 1
%define libsane %mklibname sane-hpaio %{sanemaj}
%define devname %mklibname hpip -d

# Suppress automatically generated Requires for devel packages
%define __noautoreq 'devel\(.*\)'

%define extraversion %nil
%define _disable_ld_no_undefined 1

Summary:	HP printer/all-in-one driver infrastructure
Name:		hplip
Version:	3.15.4
Release:	1
License:	GPLv2+ and MIT
Group:		System/Printing
Url:		http://hplip.sourceforge.net/
Source0:	http://garr.dl.sourceforge.net/sourceforge/hplip/%{name}-%{version}%{extraversion}.tar.gz
Source1:	hpcups-update-ppds.sh
Source2:	copy-deviceids.py
# http://www.iconfinder.com/icondetails/6393/128/fax_hardware_icon
Source3:	hp-sendfax.png
Source4:	hplip.rpmlintrc
# http://hplipopensource.com/node/367
Source5:	http://hplipopensource.com/hplip-web/smartinstall/SmartInstallDisable-Tool.run
Source6:	README.urpmi
# (doktor5000) fix linking with python and libsane
# taken from mandriva
Patch1:		hplip-3.11.3-mdv-link.patch
# (Anssi) Apply udev rules even on ACTION=="change", otherwise the permissions
# do not get applied in %%post on a new installation:
Patch2:		hplip-apply-udev-rules-on-action-change.patch

# Fedora patches
Patch101:	hplip-pstotiff-is-rubbish.patch
Patch102:	hplip-strstr-const.patch
Patch103:	hplip-ui-optional.patch
Patch104:	hplip-no-asm.patch
Patch105:	hplip-deviceIDs-drv.patch
Patch107:	hplip-deviceIDs-ppd.patch
Patch108:	hplip-retry-open.patch
Patch109:	hplip-snmp-quirks.patch
Patch111:	hplip-hpijs-marker-supply.patch
Patch112:	hplip-clear-old-state-reasons.patch
Patch114:	hplip-hpcups-sigpipe.patch
Patch115:	hplip-logdir.patch
Patch116:	hplip-bad-low-ink-warning.patch
Patch121:	hplip-ppd-ImageableArea.patch
# fedora patch not necessary. done via sed call
#Patch129: hplip-makefile-chgrp.patch
Patch131:	hplip-ipp-accessors.patch
Patch132:	hplip-IEEE-1284-4.patch
Patch133:	hplip-check.patch
Patch134:	hplip-udev-rules.patch

# Debian/Ubuntu patches
# taken from http://patch-tracker.debian.org/package/hplip/3.11.7-1
Patch201:	01_rss.dpatch
Patch203:	14_charsign_fixes.dpatch
Patch204:	85_rebuild_python_ui.dpatch
Patch206:	hplip-photosmart_b9100_support.patch
Patch207:	pjl-duplex-binding.dpatch
#hplip-pjl-duplex-binding.patch
Patch208:	mga-kde4-kdesudo-support.patch
Patch209:	hp-check-groups.dpatch
Patch215:	simple-scan-as-default.dpatch
# (doktor5000) rediff original debian patch for hplip 3.11.10
Patch217:	hplip-3.11.10-mga-remove-duplicate-entry-for-cp1700-in-drv-files.patch
Patch220:	add-lidil-two-cartridge-modes.dpatch
Patch221:	add_missing_newline_for_error_log.dpatch
Patch224:	hplip-syslog-fix-debug-messages-to-error.dpatch
Patch225:	hpfax-bug-function-used-before-importing-log.dpatch
Patch226:	hp-systray-make-menu-title-visible-in-sni-qt-indicator.dpatch
Patch227:	hp-systray-make-menu-appear-in-sni-qt-indicator-with-kde.dpatch
Patch228:	hpaio-option-duplex.diff

Patch302:	hplip-CVE-2013-4325.patch

BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	polkit
BuildRequires:	python-sip >= 1:4.16.4-1
BuildRequires:	net-snmp-devel
BuildRequires:	cups-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libgphoto2)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(udev)
%if %{sane_backend}
BuildRequires:	pkgconfig(sane-backends)
BuildRequires:	xsane
Requires(post):	hplip
%endif
Requires(post):	systemd
Requires:	cups
# For dynamic ppd generation.
Requires:	foomatic-filters
Requires:	hplip-model-data
Requires:	hplip-hpijs
Requires:	hplip-hpijs-ppds
Requires:	python-sip >= 1:4.16.4-1
# Needed for communicating with ethernet-connected printers
Requires:	net-snmp-mibs
# Needed to generate fax cover pages
Requires:	python-reportlab
# Needed since 2.8.4 for IPC
Requires:	python-dbus >= 1.2.0-11
Requires:	polkit-agent
Requires:	usermode-consoleonly
Requires:	python-gi >= 3.14.0-3
# Required by hp-scan for command line scanning
Requires:	python-imaging >= 2.5.1-3
Requires:	sane-backends-hpaio
# Needed to avoid misleading errors about network connectivity (RH bug #705843)
Requires:	wget
# (tpg) hp-check needs this
Requires:	acl
# hplip tools use internal symbols from libhplip that can change among versions
Requires:	%{libhpip} = %{EVRD}
Requires:	%{libhpipp} = %{EVRD}
# Some HP ppds are in foomatic-db and foomatic-db-hpijs (mdv bug #47415)
Suggests:	foomatic-db-hpijs
# hp-doctor requires gui modules
Requires:	hplip-gui
Requires:	gnupg

# foomatic-db-hpijs drivers are provided by hp and by this package now
# NOTE: remove the foomatic-db-hpijs deps sometime in 2010-10-?? ?
Provides:	foomatic-db-hpijs = %{version}-%{release}

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

%package -n %{libhpip}
Summary:	Dynamic library for the "hplip" HP printer/all-in-one drivers
Group:		System/Printing

%description -n %{libhpip}
Library needed for the "hplip" HP printer/all-in-one drivers

%package -n %{libhpipp}
Summary:	Dynamic library for the "hplip" HP printer/all-in-one drivers
Group:		System/Printing

%description -n %{libhpipp}
Library needed for the "hplip" HP printer/all-in-one drivers

%package -n %{libhpmud}
Summary:	Dynamic library for the "hplip" HP printer/all-in-one drivers
Group:		System/Printing
Conflicts:	%{_lib}hpip0 < 3.13.2-4

%description -n %{libhpmud}
Library needed for the "hplip" HP printer/all-in-one drivers

%package -n %{devname}
Summary:	Headers and links to compile against the "%{libhpip}" ("hplip") library
Group:		Development/C
Requires:	%{libhpip} >= %{version}-%{release}
Requires:	%{libhpipp} >= %{version}-%{release}
Requires:	%{libhpmud} >= %{version}-%{release}
Requires:	%{libsane} >= %{version}-%{release}
Provides:	libhpip-devel = %{version}-%{release}
Obsoletes:	%{_lib}hpip0-devel < 3.13.2-4

%description -n %{devname}
This package contains all files which one needs to compile programs using
the "%{libhpip}" library.

%if %{sane_backend}
%package -n %{libsane}
Summary:	SANE driver for scanners in HP's multi-function devices (from HPLIP)
Group:		System/Printing
Requires(post):	sane-backends
Provides:	sane-backends-hpaio = %{version}-%{release}
# (cjw) for system-config-printer
Provides:	libsane-hpaio

%description -n %{libsane}
SANE driver for scanners in HP's multi-function devices (from HPLIP)
%endif

%package model-data
Summary:	Data file listing the HP printer models supported by HPLIP
Group:		System/Printing

%description model-data
HPLIP supports most current HP printers and multifunction devices, but
there are some older models not supported. This package contains the
list of supported models. Printerdrake installs it automatically to
determine whether HPLIP has to be installed or not.

%package gui
Summary:	HPLIP graphical tools
Group:		System/Printing
Requires:	python-qt4-gui
Requires:	%{name} = %{version}-%{release}
Requires:	usermode

%description gui
HPLIP graphical tools.

%package hpijs
Summary:	HPs printer driver IJS plug-in for GhostScript
Group:		System/Printing
Requires:	ghostscript
Provides:	hpijs = %{EVRD}

%description hpijs
HPs printer driver IJS plug-in for GhostScript. This driver gives full
printing support for nearly all non-PostScript inkjet and laser
printers made by HP.

%package hpijs-ppds
Summary:	PPD files for the HPIJS printer driver
Group:		System/Printing
Requires:	foomatic-filters
Requires:	hplip-hpijs

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
%setup -qn %{name}-%{version}%{extraversion}

%patch2 -p1 -b .udev-rules-on-action-change

# Fedora patches

# The pstotiff filter is rubbish so replace it (launchpad #528394).
%patch101 -p1 -b .pstotiff-is-rubbish

# Fix compilation.
%patch102 -p1 -b .strstr-const

# Make utils.checkPyQtImport() look for the gui sub-package (RH bug #243273).
%patch103 -p1 -b .ui-optional

# Make sure to avoid handwritten asm.
%patch104 -p1 -b .no-asm

# Corrected several IEEE 1284 Device IDs using foomatic data.
# Color LaserJet CM1312nfi (bug #581005)
# Color LaserJet 3800 (bug #581935)
# Color LaserJet 2840 (bug #582215)
# Color LaserJet CP1518ni (bug #613689)
# Color LaserJet 2600n (bug #613712)
# Color LaserJet 2500/3700/4550/4600/4650/4700/5550/CP1515n/CP2025n
#                CP3525/CP4520 Series/CM2320nf (bug #659040)
# Color LaserJet CP2025dn (bug #651509)
# Color LaserJet CM4730 MFP (bug #658831)
# Color LaserJet CM3530 MFP (bug #659381)
# LaserJet 4050 Series/4100 Series/2100 Series/4350/5100 Series/8000 Series
#          P3005/P3010 Series/P4014/P4515 (bug #659039)
# LaserJet Professional P1606dn (bug #708472)
# LaserJet Professional M1212nf MFP (bug #742490)
# LaserJet M1536dnf MFP (bug #743915)
# LaserJet M1522nf MFP (bug #745498)
# LaserJet M1319f MFP (bug #746614)
# LaserJet M1120 MFP (bug #754139)
# LaserJet P1007 (bug #585272)
# LaserJet P1505 (bug #680951)
# LaserJet P2035 (Ubuntu #917703)
# PSC 1600 series (bug #743821)
# Officejet 6300 series (bug #689378)
# LaserJet Professional P1102w (bug #795958)
# Color LaserJet CM4540 MFP (bug #968177)
# Color LaserJet cp4005 (bug #980976)
%patch105 -p1 -b .ids

chmod +x %{SOURCE2}
mv prnt/drv/hpijs.drv.in{,.deviceIDs-drv-hpijs}
%{SOURCE2} prnt/drv/hpcups.drv.in \
           prnt/drv/hpijs.drv.in.deviceIDs-drv-hpijs \
           > prnt/drv/hpijs.drv.in

# Add Device ID for
# LaserJet 1200 (bug #577308)
# LaserJet 1320 series (bug #579920)
# LaserJet 2300 (bug #576928)
# LaserJet P2015 Series (bug #580231)
# LaserJet 4250 (bug #585499)
# Color LaserJet 2605dn (bug #583953)
# Color LaserJet 3800 (bug #581935)
# Color LaserJet 2840 (bug #582215)
# LaserJet 4050 Series/4100 Series/2100 Series/2420/4200/4300/4350/5100 Series
#          8000 Series/M3027 MFP/M3035 MFP/P3005/P3010 Series (bug #659039)
# Color LaserJet 2500/2550/2605dn/3700/4550/4600
#                4650/4700/5550/CP3525 (bug #659040)
# Color LaserJet CM4730 MFP (bug #658831)
# Color LaserJet CM3530 MFP (bug #659381)
# Designjet T770 (bug #747957)
# Color LaserJet CM4540 MFP (bug #968177)
# Color LaserJet cp4005 (bug #980976)
for ppd_file in $(grep '^diff' %{PATCH107} | cut -d " " -f 4);
do
  gunzip ${ppd_file#*/}.gz
done

%patch107 -p1 -b .deviceIDs-ppd
for ppd_file in $(grep '^diff' %{PATCH107} | cut -d " " -f 4);
do
  gzip -n ${ppd_file#*/}
done


# Retry when connecting to device fails (RH bug #532112).
%patch108 -p1 -b .retry-open

# Mark SNMP quirks in PPD for HP OfficeJet Pro 8500 (RH bug #581825).
%patch109 -p1 -b .snmp-quirks

# Fixed bogus low ink warnings from hpijs driver (RH bug #643643).
%patch111 -p1 -b .hpijs-marker-supply

# Clear old printer-state-reasons we used to manage (RH bug #510926).
%patch112 -p1 -b .clear-old-state-reasons

# Avoid busy loop in hpcups when backend has exited (RH bug #525944).
%patch114 -p1 -b .hpcups-sigpipe

%patch115 -p1 -b .logdir

# Fixed Device ID parsing code in hpijs's dj9xxvip.c (RH bug #510926).
%patch116 -p1 -b .bad-low-ink-warning

# Fix ImageableArea for Laserjet 8150/9000 (RH bug #596298).
for ppd_file in $(grep '^diff' %{PATCH121} | cut -d " " -f 4);
do
  gunzip ${ppd_file#*/}.gz
done
%patch121 -p1 -b .ImageableArea
for ppd_file in $(grep '^diff' %{PATCH121} | cut -d " " -f 4);
do
  gzip -n ${ppd_file#*/}
done

# Don't run 'chgrp lp /var/log/hp' in makefile (removes all lines with "chgrp")
sed -i '/chgrp/d' Makefile.am

sed -i.duplex-constraints \
    -e 's,\(UIConstraints.* \*Duplex\),//\1,' \
    prnt/drv/hpcups.drv.in

#patch132 -p1 -b .hplip-IEEE-1284-4

# Removed SYSFS use in udev rules and actually made them work (bug #560754).
# Move udev rules to /lib/udev/rules.d (bug #748208).
%patch134 -p1 -b .udev-rules

# Debian/Ubuntu patches

# This patch tries to make sure that black is printed with just
# the black pen, if the printer supports it
%patch201 -p1 -b .01_rss

# code cleanup related to char signedness
%patch203 -p1 -b .14_charsign

# compiling ui files to py
%patch204 -p1 -b .85_rebuild_python_ui

# Corrections on the models.dat entry for the HP PhotoSmart Pro B9100,
# especially for the correct color calibration mode.
%patch206 -p1 -b .hplip-photosmart_b9100_support

# Fixes Short-edge duplex printing if duplex is PJL-controlled
# https://bugs.launchpad.net/hplip/+bug/244295
%patch207 -p1 -b .hplip-pjl-duplex-binding

# original patch from debian, path to kdesu added for %%_libdir on x86_64
# %patch208 -p1 -b .mga-kde4-kdesudo-support

# https://bugs.launchpad.net/debian/+source/hplip/+bug/530746
%patch209 -p1 -b .hp-check-groups

# disable for now, as this changes default hplip behavior
# and change in default scanning application should be decided by a poll first
#%patch215 -p1 -b .simple-scan-as-default

#patch217 -p1 -b .mga-remove-duplicate-entry-for-cp1700-in-drv-files

%patch220 -p1 -b .add-lidil-two-cartridge-modes
# fixed by upstream
#patch224 -p1 -b .hplip-syslog-fix-debug-messages-to-error

%patch225 -p1 -b .hpfax-bug-function-used-before-importing-log

%patch226 -p1 -b .hp-systray-make-menu-title-visible-in-sni-qt-indicator

%patch227 -p1 -b .hp-systray-make-menu-appear-in-sni-qt-indicator-with-kde

%patch228 -p1 -b .hpaio-option-duplex

%patch302 -p0

sed -i.duplex-constraints \
    -e 's,\(UIConstraints.* \*Duplex\),//\1,' \
    prnt/drv/hpcups.drv.in

# Make all files in the source user-writable
chmod -R u+w .

%build
%serverbuild
#needed by patches 204 and 205
# create required files as placeholder, otherwise autoreconf fails
touch NEWS README AUTHORS ChangeLog
autoreconf -ifv

%if !%{sane_backend}
WITHOUT_SANE="--without-sane"
%endif
%configure \
	$WITHOUT_SANE \
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
	--disable-policykit \
	--with-mimedir=%{_datadir}/cups/mime PYTHON=%{__python}

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/hp

%makeinstall_std PYTHON=%{__python}

# Install files which the "make install" missed to install
install -m 644 ip/hpip.h %{buildroot}%{_includedir}
install -m 644 ip/xform.h %{buildroot}%{_includedir}

# Move doc in sub-package
mv %{buildroot}%{_docdir}/%{name}-%{version}%{extraversion} %{buildroot}%{_docdir}/%{name}-doc-%{version}%{extraversion}

# Remove static libraries of SANE driver
rm -f %{buildroot}%{_libdir}/sane/libsane-hpaio*.la
rm -f %{buildroot}%{_sysconfdir}/sane.d/dll.conf

# Remove other unneeded/unwanted files
# Remove files we don't want to package.
rm -f %{buildroot}%{_datadir}/hplip/hpaio.desc
rm -f %{buildroot}%{_datadir}/hplip/hplip-install
rm -rf %{buildroot}%{_datadir}/hplip/install.*
rm -f %{buildroot}%{_datadir}/hplip/uninstall.*
rm -f %{buildroot}%{_bindir}/hp-uninstall
rm -f %{buildroot}%{_datadir}/hplip/upgrade.*
rm -f %{buildroot}%{_bindir}/hp-upgrade
rm -f %{buildroot}%{_bindir}/hp-config_usb_printer
rm -f %{buildroot}%{_unitdir}/hplip-printer@.service
rm -f %{buildroot}%{_datadir}/hplip/config_usb_printer.*
rm -f %{buildroot}%{_datadir}/hplip/hpijs.drv.in.template
rm -f %{buildroot}%{_datadir}/cups/mime/pstotiff.types
rm -f %{buildroot}%{_datadir}/hplip/fax/pstotiff*
rm -f %{buildroot}%{_cups_serverbin}/filter/hpcac

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor='' \
	--dir=%{buildroot}%{_datadir}/applications \
	--remove-category='Application' \
	--remove-category='Utility' \
	--add-category='System' \
	--add-category='Settings' \
	--add-category='Printing' \
	--add-category='Qt' \
	--add-category='HardwareSettings' \
	--remove-key='Version' \
	%{buildroot}%{_datadir}/applications/hplip.desktop

# Create /run/hplip
mkdir -p %{buildroot}/run/hplip

# install /usr/lib/tmpfiles.d/hplip.conf (bug #1015831)
mkdir -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/hplip.conf <<EOF
# See tmpfiles.d(5) for details

d /run/hplip 0775 root lp -
EOF

# install menu icons
for N in 16 32 48 64; do convert %{SOURCE3} -resize ${N}x${N} $N.png; done
install -D -m 0644 16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/hp-sendfax.png
install -D -m 0644 32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/hp-sendfax.png
install -D -m 0644 48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/hp-sendfax.png
install -D -m 0644 64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/hp-sendfax.png
install -D -m 0644 %{SOURCE3} %{buildroot}%{_iconsdir}/hicolor/128x128/apps/hp-sendfax.png

# (cg) Correct the udev rules dir
mkdir -p %{buildroot}/lib
mv %{buildroot}%{_sysconfdir}/udev %{buildroot}/lib/

# Regenerate hpcups PPDs on upgrade if necessary (bug #579355).
install -p -m755 %{SOURCE1} %{buildroot}%{_bindir}/hpcups-update-ppds

# A tool disable smart install feature in HP printer(s) from linux
# HP Smart Install is a service running on firmware which makes printer to appear
# as "Mass Storage Devices" when connected via USB cable. This is to install the
# minimal printer software from flash memory of printer. This service needs to be
# disabled on linux in order to have the device function as a printer.
install -p -m755 %{SOURCE5} %{buildroot}%{_bindir}/SmartInstallDisable-Tool.run
mkdir -p %{buildroot}%{_docdir}/%{name}
install -p -m755 %{SOURCE6} %{buildroot}%{_docdir}/%{name}

# Make sure pyc files are generated, otherwise we can get
# difficult to debug problems
pushd %{buildroot}%{_datadir}/%{name}
%{__python} -m compileall .
popd

# create empty /var/lib/hp/hplip.state to fix hp-plugin installation (mga#5395)
mkdir -p %{buildroot}%{_localstatedir}/lib/hp/
touch %{buildroot}%{_localstatedir}/lib/hp/hplip.state

# Create an empty plugins directory to make sure it gets the right
mkdir -p %{buildroot}%{_datadir}/hplip/prnt/plugins

# create empty log directory so that it can be owned
mkdir -p %{buildroot}%{_localstatedir}/log/hp/tmp

mkdir -p %{buildroot}%{_unitdir}
mv -f %{buildroot}/usr/lib/systemd/system/hplip-printer@.service %{buildroot}%{_unitdir}/hplip-printer@.service

# Images in docdir should not be executable (bug #440552).
find doc/images -type f -exec chmod 644 {} \;

#sed -e 's/0664/0666/' -i %{buildroot}/lib/udev/rules.d/56-hpmud.rules
#sed -e 's/ATTR/#ATTR/' -i %{buildroot}/lib/udev/rules.d/56-hpmud.rules
#sed -e 's/ATTR/SYSFS/' -i %{buildroot}/lib/udev/rules.d/56-hpmud.rules

# The systray applet doesn't work properly (displays icon as a
# window), so don't ship the launcher yet.
# rm -f %{buildroot}%{_sysconfdir}/xdg/autostart/hplip-systray.desktop

#We do not need hal
rm -f %{buildroot}%{_datadir}/hal/fdi/preprobe/10osvendor/20-hplip-devices.fdi

#Add rules for all hp printers
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03f0", GROUP="lp", MODE:="666"' >> %{buildroot}/lib/udev/rules.d/56-hpmud.rules

# consolehelper config
#

mkdir -p %{buildroot}%{_sbindir}

# - console user, no password
for pak in hp-setup hp-plugin hp-diagnose_plugin; do
		mv %{buildroot}%{_bindir}/$pak %{buildroot}%{_sbindir}/$pak
        ln -sf %{_bindir}/consolehelper %{buildroot}%{_bindir}/$pak
        mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps/
        cat > %{buildroot}%{_sysconfdir}/security/console.apps/$pak <<EOF
USER=root
PROGRAM=%{_sbindir}/$pak
FALLBACK=false
SESSION=true
EOF
        mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
		cat > %{buildroot}%{_sysconfdir}/pam.d/$pak  <<EOF
#%PAM-1.0
auth		include		config-util-user
account		include		config-util-user
session		include		config-util-user
EOF
done

%post -n hplip-hpijs-ppds
# Restart CUPS to make the printing PPDs known to it
/bin/systemctl try-restart org.cups.cupsd.socket ||:
/bin/systemctl try-restart org.cups.cupsd.service ||:

%post -n hplip-hpijs
%{_bindir}/hpcups-update-ppds &>/dev/null ||:

%post -n hplip-model-data
/sbin/udevadm trigger --subsystem-match=usb --attr-match=idVendor=03f0
# ensure permissions are ready when installation completes
/sbin/udevadm settle --timeout=15
:

%if %{sane_backend}
%post -n %{libsane}

# Add HPLIP driver to /etc/sane.d/dll.conf
if ! grep ^hpaio /etc/sane.d/dll.conf >/dev/null 2>/dev/null ; then \
	echo hpaio >> /etc/sane.d/dll.conf; \
fi
%endif

%if %{sane_backend}
%preun -n %{libsane}
# Remove HPLIP driver from /etc/sane.d/dll.conf
if [ "$1" = 0 ]; then \
	if grep ^hpaio /etc/sane.d/dll.conf >/dev/null 2>/dev/null ; then \
		sed '/hpaio/d' /etc/sane.d/dll.conf > /tmp/$$; \
		cp -f /tmp/$$ /etc/sane.d/dll.conf; \
		rm -f /tmp/$$; \
	fi; \
fi
%endif

# Restart CUPS to make the removal of the Fax PPD known to it
/bin/systemctl restart org.cups.cupsd.socket ||:
/bin/systemctl restart org.cups.cupsd.service ||:

%postun -n hplip-hpijs-ppds
# Restart CUPS to make the removal of the printing PPDs known to it
/bin/systemctl restart org.cups.cupsd.socket ||:
/bin/systemctl restart org.cups.cupsd.service ||:

%files
%config(noreplace) %{_sysconfdir}/hp
%dir %{_localstatedir}/lib/hp/
%{_bindir}/hp-align
%{_bindir}/hp-clean
%{_bindir}/hp-colorcal
%{_bindir}/hp-devicesettings
%{_bindir}/hp-diagnose_plugin
%{_bindir}/hp-diagnose_queues
%{_bindir}/hp-doctor
%{_datadir}/hplip/doctor.py*
%{_bindir}/hp-fab
%{_bindir}/hp-faxsetup
%{_bindir}/hp-firmware
%{_bindir}/hp-info
%{_bindir}/hp-levels
%{_bindir}/hp-linefeedcal
%{_bindir}/hp-logcapture
%{_bindir}/hp-makecopies
%{_bindir}/hp-makeuri
%{_bindir}/hp-pkservice
%{_bindir}/hp-plugin
%{_bindir}/hp-pqdiag
%{_bindir}/hp-printsettings
%{_bindir}/hp-probe
%{_bindir}/hp-query
%{_bindir}/hp-scan
%{_bindir}/hp-sendfax
%{_bindir}/hp-setup
%{_bindir}/hp-testpage
%{_bindir}/hp-timedate
%{_bindir}/hp-unload
%{_bindir}/hp-wificonfig

%{_sbindir}/hp-diagnose_plugin
%{_sbindir}/hp-setup
%{_sbindir}/hp-plugin

%{_sysconfdir}/pam.d/hp-diagnose_plugin
%{_sysconfdir}/pam.d/hp-plugin
%{_sysconfdir}/pam.d/hp-setup
%{_sysconfdir}/security/console.apps/hp-diagnose_plugin
%{_sysconfdir}/security/console.apps/hp-plugin
%{_sysconfdir}/security/console.apps/hp-setup

# A tool to disable Smart Install
%{_bindir}/SmartInstallDisable-Tool.run

%exclude %{_datadir}/hplip/data/models
# C libraries for Python
%{_libdir}/python*/*/*.so*
# CUPS backends (0755 permissions, so that CUPS 1.2 runs these backends
# as lp user)
# Note: this must be /usr/lib not %{_libdir}, since that's the
# CUPS serverbin directory.
%attr(0755,root,root) %{_prefix}/lib/cups/backend/hp*
%{_prefix}/lib/cups/filter/hpcups
%{_prefix}/lib/cups/filter/hpcupsfax
%{_prefix}/lib/cups/filter/hpps
%{_prefix}/lib/cups/filter/pstotiff
%{_datadir}/ppd/HP/HP-Fax*.ppd*
%{_datadir}/cups/drv/hp/hpcups.drv
# Files
%dir %{_datadir}/hplip
%{_datadir}/hplip/align.py*
%{_datadir}/hplip/check-plugin.py*
%{_datadir}/hplip/clean.py*
%{_datadir}/hplip/colorcal.py*
#{_datadir}/hplip/config_usb_printer.py*
%{_datadir}/hplip/devicesettings.py*
%{_datadir}/hplip/diagnose_plugin.py*
%{_datadir}/hplip/diagnose_queues.py*
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
%{_datadir}/hplip/logcapture.py*
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
#%{_datadir}/hplip/uninstall.py*
%{_datadir}/hplip/unload.py*
#%{_datadir}/hplip/upgrade.py*
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
#{_datadir}/polkit-1/actions/com.hp.hplip.policy
#{_datadir}/dbus-1/system-services/com.hp.hplip.service
%{_localstatedir}/lib/hp/hplip.state
%{_docdir}/%{name}/README.urpmi
#config(noreplace) %{_sysconfdir}/dbus-1/system.d/com.hp.hplip.conf
%dir %attr(0775,root,lp) /run/hplip
%{_tmpfilesdir}/hplip.conf
%{_unitdir}/hplip-printer@.service
%{_datadir}/hplip/hplip_clean.sh
%{_datadir}/cups/mime/pstotiff.convs
%dir %{_datadir}/hplip/__pycache__
%{_datadir}/hplip/__pycache__/*.pyc

%files doc
%doc %{_docdir}/%{name}-doc-%{version}%{extraversion}

%files -n %{libhpip}
%{_libdir}/libhpip.so.%{major}*

%files -n %{libhpmud}
%{_libdir}/libhpmud.so.%{major}*

%files -n %{libhpipp}
%{_libdir}/libhpipp.so.%{major}*

%files -n %{devname}
%{_includedir}/hpip.h
%{_includedir}/xform.h
%{_libdir}/libhpip.so
%{_libdir}/libhpipp.so
%{_libdir}/libhpmud.so
%if %{sane_backend}
%{_libdir}/sane/libsane-hpaio.so

%files -n %{libsane}
%{_libdir}/sane/libsane-hpaio.so.%{sanemaj}*
%endif

%files model-data
/lib/udev/rules.d/*.rules
%{_datadir}/hplip/data/models

%files gui
%{_bindir}/hp-check
%{_bindir}/hp-print
%{_bindir}/hp-systray
%{_bindir}/hp-toolbox
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/hp-sendfax.png
%{_sysconfdir}/xdg/autostart/hplip-systray.desktop
# Files
%{_datadir}/hplip/check.py*
%{_datadir}/hplip/print.py*
%{_datadir}/hplip/systray.py*
%{_datadir}/hplip/toolbox.py*
# Directories
%{_datadir}/hplip/data/images
%{_datadir}/hplip/ui4

%files hpijs
%{_bindir}/hpijs
# Needed for both printing and fax PPDs. They all need HPIJS, therefore
# the link is here
%dir %{_datadir}/ppd
%dir %{_datadir}/ppd/HP
#{_datadir}/cups/drv/hp/hpijs.drv
%{_bindir}/hpcups-update-ppds

%files hpijs-ppds
%{_datadir}/ppd/HP/apollo*.ppd*
%{_datadir}/ppd/HP/hp-*.ppd*
