%global optflags %{optflags} -Wno-return-type
%global optflags %{optflags} -I%(python -c "from distutils.sysconfig import get_python_inc; print (get_python_inc());")
# Define if you want to build the sane backend (default)
%define sane_backend 1
%{?_with_sane: %global sane_backend 1}
%{?_without_sane: %global sane_backend 0}

%define major 0
%define oldlibhpip %mklibname hpip 0
%define oldlibhpipp %mklibname hpipp 0
%define oldlibhpmud %mklibname hpmud 0
%define oldlibhpdiscovery %mklibname hpdiscovery 0
%define libhpip %mklibname hpip
%define libhpipp %mklibname hpipp
%define libhpmud %mklibname hpmud
%define libhpdiscovery %mklibname hpdiscovery
%define sanemaj 1
%define oldlibsane %mklibname sane-hpaio 1
%define libsane %mklibname sane-hpaio
%define devname %mklibname hpip -d

# Suppress automatically generated Requires for devel packages
%global __requires_exclude	devel\\\(.*\\\)

# we don't want to provide private python extension libs
%global __provides_exclude	%{python3_sitearch}/.*\\.so$

%define extraversion %nil
%define _disable_ld_no_undefined 1

Summary:	HP printer/all-in-one driver infrastructure
Name:		hplip
Version:	3.25.2
Release:	1
License:	GPLv2+ and MIT
Group:		System/Printing
Url:		https://developers.hp.com/hp-linux-imaging-and-printing
Source0:	https://downloads.sourceforge.net/project/hplip/hplip/%{version}/hplip-%{version}.tar.gz
Source1:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hpcups-update-ppds.sh
Source2:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/copy-deviceids.py
# http://www.iconfinder.com/icondetails/6393/128/fax_hardware_icon
Source3:	hp-sendfax.png
Source4:	hplip.rpmlintrc
# http://hplipopensource.com/node/367
Source5:	http://hplipopensource.com/hplip-web/smartinstall/SmartInstallDisable-Tool.run
Source6:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hp-laserjet_cp_1025nw.ppd.gz
Source7:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hp-laserjet_professional_p_1102w.ppd.gz

# (Anssi) Apply udev rules even on ACTION=="change", otherwise the permissions
# do not get applied in %%post on a new installation:
Patch2:		hplip-apply-udev-rules-on-action-change.patch
Patch3:		hplip-cups-2.2.patch
Patch4:		hplip-3.15.4-hp_ipp.patch
#Patch5:		hplip-3.22.6-formatstrings.patch
Patch6:		hplip-3.31.10-fix-scan-icon-openmandriva.patch

# Fedora patches
Patch100:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-pstotiff-is-rubbish.patch
Patch101:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-strstr-const.patch
Patch102:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-ui-optional.patch
Patch103:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-no-asm.patch
Patch104:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-deviceIDs-drv.patch
Patch105:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-udev-rules.patch
Patch106:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-retry-open.patch
Patch107:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-snmp-quirks.patch
Patch108:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-hpijs-marker-supply.patch
Patch109:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-clear-old-state-reasons.patch
Patch110:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-hpcups-sigpipe.patch
Patch111:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-logdir.patch
Patch112:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-bad-low-ink-warning.patch
Patch113:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-deviceIDs-ppd.patch
Patch114:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-ppd-ImageableArea.patch
Patch115:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-scan-tmp.patch
Patch116:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-log-stderr.patch
Patch117:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-avahi-parsing.patch
Patch118:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-dj990c-margin.patch
Patch119:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-strncpy.patch
Patch120:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-no-write-bytecode.patch
Patch121:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-silence-ioerror.patch
Patch122:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-sourceoption.patch
Patch123:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-noernie.patch
Patch124:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-appdata.patch
Patch125:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-check-cups.patch
Patch126:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-typo.patch
Patch127:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-use-binary-str.patch
Patch128:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-error-print.patch
Patch129:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-hpfax-importerror-print.patch
Patch130:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-wifisetup.patch
Patch131:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-keyserver.patch
Patch132:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/0026-Call-QMessageBox-constructors-of-PyQT5-with-the-corr.patch
Patch133:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/0025-Remove-all-ImageProcessor-functionality-which-is-clo.patch
Patch134:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/0027-Fixed-incomplete-removal-of-hp-toolbox-features-whic.patch
Patch135:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-add-ppd-crash.patch
Patch136:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-missing-links.patch
Patch137:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-hplj-3052.patch
Patch138:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-hpmud-string-parse.patch
Patch139:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-m278-m281-needs-plugin.patch
Patch140:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-hpcups-crash.patch
Patch141:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-covscan.patch
Patch142:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-logging-segfault.patch
Patch143:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-systray-blockerror.patch
Patch144:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-missing-drivers.patch
Patch145:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-model-mismatch.patch
Patch146:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-unicodeerror.patch
Patch147:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-fix-Wreturn-type-warning.patch
Patch148:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-configure-python.patch
Patch149:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-dialog-infinite-loop.patch
Patch150:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-find-driver.patch
Patch151:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-clean-ldl.patch
Patch152:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-revert-plugins.patch
#Patch153:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-check-userperms.patch
Patch154:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-fab-import.patch
Patch155:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-hpsetup-noscanjets.patch
Patch156:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-hpfirmware-timeout.patch
Patch157:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-gpgdir-perms.patch
Patch158:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-plugin-udevissues.patch
Patch160:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-no-libhpmud-libm-warnings.patch
Patch161:	https://src.fedoraproject.org/rpms/hplip/raw/rawhide/f/hplip-fedora-gui.patch

# Debian/Ubuntu patches
# taken from http://patch-tracker.debian.org/package/hplip/3.11.7-1
Patch201:	01_rss.dpatch
Patch203:	14_charsign_fixes.dpatch
#Patch204:	hplip-3.15.11-rebuild_python_ui.patch
Patch207:	pjl-duplex-binding.dpatch
#hplip-pjl-duplex-binding.patch
Patch209:	hplip-3.15.11-mga-plasma-delay-startup.patch
Patch215:	simple-scan-as-default.dpatch
Patch220:	add-lidil-two-cartridge-modes.dpatch
Patch226:	hp-systray-make-menu-title-visible-in-sni-qt-indicator.dpatch
Patch227:	hp-systray-make-menu-appear-in-sni-qt-indicator-with-kde.dpatch
Patch228:	hpaio-option-duplex.diff
# (tpg) https://issues.openmandriva.org/show_bug.cgi?id=1223
Patch229:	process-events-for-systray.patch
Patch302:	hplip-CVE-2013-4325.patch
Patch303:	hplip-3.17.11-hp-systray-dont-start-in-KDE.patch
Patch304:	hplip-3.18.12-clang7.patch
#Patch305:	hplip-3.20.11-authtype.patch

# OMV
Patch400:	hplip-3.22.10-python-3.11.patch
Patch401:	hplip-3.22.10-distrorecognition.patch
Patch402:	hplip-3.23.3-clang16.patch
Patch403:	hplip-DESTDIR.patch

BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	polkit
BuildRequires:	python-sip >= 4.16.4-1
BuildRequires:	net-snmp-devel
BuildRequires:	cups-devel
# For ppdc
BuildRequires:	cups-common cups
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(avahi-core)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(libgphoto2)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	polkit-1-devel
%if %{sane_backend}
BuildRequires:	pkgconfig(sane-backends)
BuildRequires:	xsane
Requires(post):	hplip
%endif
Requires(post):	systemd
Requires(post):	cups
# For dynamic ppd generation.
Requires:	foomatic-filters
Requires:	hplip-model-data
Requires:	hplip-hpijs
Requires:	hplip-hpijs-ppds
Requires:	python-sip-qt5 
# Needed for communicating with ethernet-connected printers
Requires:	net-snmp-mibs
# Needed to generate fax cover pages
Requires:	python-reportlab
# Needed since 2.8.4 for IPC
Requires:	python-dbus >= 1.2.0-11
Requires:	polkit-agent
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
%rename %{oldlibhpip}

%description -n %{libhpip}
Library needed for the "hplip" HP printer/all-in-one drivers

%package -n %{libhpipp}
Summary:	Dynamic library for the "hplip" HP printer/all-in-one drivers
Group:		System/Printing
%rename %{oldlibhpipp}

%description -n %{libhpipp}
Library needed for the "hplip" HP printer/all-in-one drivers

%package -n %{libhpmud}
Summary:	Dynamic library for the "hplip" HP printer/all-in-one drivers
Group:		System/Printing
Conflicts:	%{_lib}hpip0 < 3.13.2-4
%rename %{oldlibhpmud}

%description -n %{libhpmud}
Library needed for the "hplip" HP printer/all-in-one drivers

%package -n %{libhpdiscovery}
Summary:        Dynamic library for the "hplip" HP printer/all-in-one drivers
Group:          System/Printing
%rename %{oldlibhpdiscovery}

%description -n %{libhpdiscovery}
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
%rename %{oldlibsane}

%description -n %{libsane}
SANE driver for scanners in HP's multi-function devices (from HPLIP)
%endif

%package model-data
Summary:	Data file listing the HP printer models supported by HPLIP
Group:		System/Printing
Requires(post):	systemd

%description model-data
HPLIP supports most current HP printers and multifunction devices, but
there are some older models not supported. This package contains the
list of supported models. Printerdrake installs it automatically to
determine whether HPLIP has to be installed or not.

%package gui
Summary:	HPLIP graphical tools
Group:		System/Printing
Requires:	python-qt5-gui
Requires:	python-qt5-widgets
Requires:	python-qt5-dbus
Requires:	python3dist(distro)
Requires:	%{name} = %{version}-%{release}

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

# Some patches touch compressed PPDs -- since binary patches
# are ugly, let's uncompress them first...
for i in prnt/*/*.gz; do
	PPDS="$PPDS ${i/.gz/}"
	gunzip $i
done

%autopatch -p1

# Recompress the PPDs now that we're done modifying them
gzip -9 ${PPDS}

sed -i.duplex-constraints \
    -e 's,\(UIConstraints.* \*Duplex\),//\1,' \
    prnt/drv/hpcups.drv.in

chmod +x %{SOURCE2}
mv prnt/drv/hpijs.drv.in{,.deviceIDs-drv-hpijs}
%{SOURCE2} prnt/drv/hpcups.drv.in \
           prnt/drv/hpijs.drv.in.deviceIDs-drv-hpijs \
           > prnt/drv/hpijs.drv.in

cp -a %{S:6} %{S:7} ppd/hpcups

# Don't run 'chgrp lp /var/log/hp' in makefile (removes all lines with "chgrp")
sed -i '/chgrp/d' Makefile.am

chmod -R u+w .

%build
%serverbuild
#needed by patches 204 and 205
# create required files as placeholder, otherwise autoreconf fails
touch NEWS README AUTHORS ChangeLog
sed -i 's|^AM_INIT_AUTOMAKE|AM_INIT_AUTOMAKE([foreign])|g' configure.in
autoreconf -ifv

%if !%{sane_backend}
WITHOUT_SANE="--without-sane"
%endif
#export CC=gcc
#export CXX=g++
%configure \
	$WITHOUT_SANE \
	--disable-foomatic-rip-hplip-install \
	--enable-foomatic-drv-install \
	--disable-imageProcessor-build \
	--enable-scan-build \
	--enable-gui-build \
	--enable-fax-build \
	--enable-pp-build \
	--enable-qt5 --disable-qt4 --disable-qt3 \
	--enable-hpcups-install \
	--enable-cups-drv-install \
	--enable-cups-ppd-install \
	--enable-hpijs-install \
	--disable-imageProcessor-build \
	--enable-policykit \
	--with-mimedir=%{_datadir}/cups/mime PYTHON=%{__python}

%make_build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/hp

%make_install PYTHON=%{__python}

mkdir -p %{buildroot}/run/hplip
mkdir -p %{buildroot}%{_sharedstatedir}/hp
mkdir -p %{buildroot}%{_tmpfilesdir}
echo 'd /run/hplip 0775 root lp -' >%{buildroot}%{_tmpfilesdir}/hplip.conf

# Install files which the "make install" missed to install
install -m 644 ip/hpip.h %{buildroot}%{_includedir}
install -m 644 ip/xform.h %{buildroot}%{_includedir}

# Move docs to sub-package
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
	--set-icon=%{_iconsdir}/hicolor/32x32/apps/hp-sendfax.png \
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

# Regenerate hpcups PPDs on upgrade if necessary (bug #579355).
install -p -m755 %{SOURCE1} %{buildroot}%{_bindir}/hpcups-update-ppds

# A tool disable smart install feature in HP printer(s) from linux
# HP Smart Install is a service running on firmware which makes printer to appear
# as "Mass Storage Devices" when connected via USB cable. This is to install the
# minimal printer software from flash memory of printer. This service needs to be
# disabled on linux in order to have the device function as a printer.
install -p -m755 %{SOURCE5} %{buildroot}%{_bindir}/SmartInstallDisable-Tool.run
mkdir -p %{buildroot}%{_docdir}/%{name}

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

# Images in docdir should not be executable (bug #440552).
find doc/images -type f -exec chmod 644 {} \;

# The systray applet doesn't work properly (displays icon as a
# window), so don't ship the launcher yet.
# rm -f %{buildroot}%{_sysconfdir}/xdg/autostart/hplip-systray.desktop

#We do not need hal
rm -f %{buildroot}%{_datadir}/hal/fdi/preprobe/10osvendor/20-hplip-devices.fdi

#Add rules for all hp printers
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03f0", GROUP="lp", MODE:="666"' >> %{buildroot}%{_prefix}/lib/udev/rules.d/56-hpmud.rules

%post -n hplip-hpijs-ppds
# Restart CUPS to make the printing PPDs known to it
/bin/systemctl try-restart cups.socket ||:
/bin/systemctl try-restart cups.service ||:

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
/bin/systemctl restart cups.socket ||:
/bin/systemctl restart cups.service ||:

%postun -n hplip-hpijs-ppds
# Restart CUPS to make the removal of the printing PPDs known to it
/bin/systemctl restart cups.socket ||:
/bin/systemctl restart cups.service ||:

%files
%config(noreplace) %{_sysconfdir}/hp
%dir %{_localstatedir}/lib/hp/
%{_sysconfdir}/dbus-1/system.d/com.hp.hplip.conf
%{_datadir}/dbus-1/system-services/com.hp.hplip.service
%{_datadir}/polkit-1/actions/com.hp.hplip.policy
%{_bindir}/hp-uiscan
%{_bindir}/hp-align
%{_bindir}/hp-clean
%{_bindir}/hp-colorcal
%{_bindir}/hp-devicesettings
%{_bindir}/hp-diagnose_plugin
%{_bindir}/hp-diagnose_queues
%{_bindir}/hp-doctor
%{_datadir}/hplip/dat2drv
%{_datadir}/hplip/doctor.py*
%{_datadir}/hplip/locatedriver
%{_datadir}/hplip/uiscan.py
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
%{_prefix}/lib/cups/filter/hpcdmfax
%{_datadir}/ipp-usb/quirks/HPLIP.conf
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
%{_localstatedir}/lib/hp/hplip.state
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

%files -n %{libhpdiscovery}
%{_libdir}/libhpdiscovery.so.%{major}*

%files -n %{devname}
%{_includedir}/hpip.h
%{_includedir}/xform.h
%{_libdir}/libhpip.so
%{_libdir}/libhpipp.so
%{_libdir}/libhpmud.so
%{_libdir}/libhpdiscovery.so
%if %{sane_backend}
%{_libdir}/sane/libsane-hpaio.so

%files -n %{libsane}
%{_libdir}/sane/libsane-hpaio.so.%{sanemaj}*
%endif

%files model-data
#dir %attr(0755,root,lp) /run/hplip
%{_tmpfilesdir}/hplip.conf
%{_udevrulesdir}/*.rules
%{_datadir}/hplip/data/models
%{_datadir}/cups/drv/hp

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
%{_datadir}/hplip/ui5

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
