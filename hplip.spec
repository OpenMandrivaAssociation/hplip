# Define if you want to build the sane backend (default)
%define sane_backend 1
%{?_with_sane: %global sane_backend 1}
%{?_without_sane: %global sane_backend 0}

%define major 0
%define libhpip %mklibname hpip %{major}
%define libhpmud %mklibname hpmud %{major}
%define sanemaj 1
%define libsane %mklibname sane-hpaio %{sanemaj}
%define devname %mklibname hpip -d

# Suppress automatically generated Requires for devel packages
%define __noautoreq 'devel\(.*\)'

%define extraversion %nil

Summary:	HP printer/all-in-one driver infrastructure
Name:		hplip
Version:	3.13.8
Release:	2
License:	GPLv2+ and MIT
Group:		System/Printing
Url:		http://hplip.sourceforge.net/
Source0:	http://garr.dl.sourceforge.net/sourceforge/hplip/%{name}-%{version}%{extraversion}.tar.gz
Source1:	hpcups-update-ppds.sh
Source2:	%{name}-tmpfiles.conf
# http://www.iconfinder.com/icondetails/6393/128/fax_hardware_icon
Source3:	hp-sendfax.png
Source4:	hplip.rpmlintrc
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
Patch106:	hplip-mucks-with-spooldir.patch
Patch108:	hplip-retry-open.patch
Patch109:	hplip-snmp-quirks.patch
Patch110:	hplip-discovery-method.patch
Patch111:	hplip-hpijs-marker-supply.patch
Patch112:	hplip-clear-old-state-reasons.patch
Patch113:	hplip-systray-dbus-exception.patch
Patch114:	hplip-hpcups-sigpipe.patch
Patch115:	hplip-logdir.patch
Patch116:	hplip-bad-low-ink-warning.patch
Patch118:	hplip-skip-blank-lines.patch
Patch119:	hplip-dbglog-newline.patch
Patch121:	hplip-ppd-ImageableArea.patch
Patch122:	hplip-raw_deviceID-traceback.patch
Patch123:	hplip-UnicodeDecodeError.patch
Patch124:	hplip-3.12.9-addprinter.patch
Patch125:	hplip-dbus-exception.patch
Patch126:	hplip-notification-exception.patch
Patch127:	hplip-CVE-2010-4267.patch
Patch128:	hplip-wifisetup.patch
# fedora patch not necessary. done via sed call
#Patch129: hplip-makefile-chgrp.patch
Patch130:	hplip-hpaio-localonly.patch
Patch131:	hplip-ipp-accessors.patch
Patch132: hplip-IEEE-1284-4.patch
Patch133: hplip-check.patch

# Debian/Ubuntu patches
# taken from http://patch-tracker.debian.org/package/hplip/3.11.7-1
Patch201:	01_rss.dpatch
Patch202:	10_shebang_fixes.dpatch
Patch203:	14_charsign_fixes.dpatch
Patch204:	85_rebuild_python_ui.dpatch
Patch205:	87_move_documentation.dpatch
Patch206:	hplip-photosmart_b9100_support.patch
Patch207:	pjl-duplex-binding.dpatch
#hplip-pjl-duplex-binding.patch
Patch208:	mga-kde4-kdesudo-support.dpatch
Patch209:	hp-check-groups.dpatch
#Patch210:	hp-check_debian.dpatch
Patch211:	hp-setup-prompt-for-custom-PPD.dpatch
Patch213:	hp-mkuri-take-into-account-already-installed-plugin-also-for-exit-value.dpatch
#Patch214:	ubuntu-hp-mkuri-notification-text.dpatch
Patch215:	simple-scan-as-default.dpatch
Patch216:	make-commafy-correctly-work-with-python-2.dpatch
# (doktor5000) rediff original debian patch for hplip 3.11.10
Patch217:	hplip-3.11.10-mga-remove-duplicate-entry-for-cp1700-in-drv-files.patch
Patch219:	try_libhpmud.so.0.dpatch
Patch220:	add-lidil-two-cartridge-modes.dpatch
Patch221:	add_missing_newline_for_error_log.dpatch
Patch224:	hplip-syslog-fix-debug-messages-to-error.dpatch
Patch225:	hpfax-bug-function-used-before-importing-log.dpatch
Patch226:	hp-systray-make-menu-title-visible-in-sni-qt-indicator.dpatch
Patch227:	hp-systray-make-menu-appear-in-sni-qt-indicator-with-kde.dpatch
Patch228:	hpaio-option-duplex.diff

Patch301: fix-uninitialized-variables.patch

BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	polkit
BuildRequires:	python-sip >= 4.1.1
BuildRequires:	net-snmp-devel
BuildRequires:	cups-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libgphoto2)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(python)
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
Requires:	python-sip >= 4.1.1
# Needed for communicating with ethernet-connected printers
Requires:	net-snmp-mibs
# Needed to generate fax cover pages
Requires:	python-reportlab
# Needed since 2.8.4 for IPC
Requires:	python-dbus
Requires:	polkit-agent
Requires:	usermode-consoleonly
Requires:	python-gobject
# Required by hp-scan for command line scanning
Requires:	python-imaging
Requires:	sane-backends-hpaio
# Needed to avoid misleading errors about network connectivity (RH bug #705843)
Requires:	wget
# (tpg) hp-check needs this
Requires:	acl
# hplip tools use internal symbols from libhplip that can change among versions
Requires:	%{libhpip} = %{version}
%py_requires -d
# Some HP ppds are in foomatic-db and foomatic-db-hpijs (mdv bug #47415)
Suggests:	foomatic-db-hpijs

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
Suggests:	sane-backends
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

%patch2 -p1 -b .udev~

# Fedora patches

# The pstotiff filter is rubbish so replace it (launchpad #528394).
%patch101 -p1 -b .pstotiff-is-rubbish

# Fix compilation.
%patch102 -p1 -b .strstr-const

# Make utils.checkPyQtImport() look for the gui sub-package (RH bug #243273).
%patch103 -p1 -b .ui-optional

# Make sure to avoid handwritten asm.
%patch104 -p1 -b .no-asm

# Stopped hpcups pointlessly trying to read spool files
# directly (RH bug #552572).
%patch106 -p1 -b .mucks-with-spooldir

# Retry when connecting to device fails (RH bug #532112).
%patch108 -p1 -b .retry-open

# Mark SNMP quirks in PPD for HP OfficeJet Pro 8500 (RH bug #581825).
%patch109 -p1 -b .snmp-quirks

# Fixed hp-setup traceback when discovery page is skipped (RH bug #523685).
%patch110 -p1 -b .discovery-method

# Fixed bogus low ink warnings from hpijs driver (RH bug #643643).
%patch111 -p1 -b .hpijs-marker-supply

# Clear old printer-state-reasons we used to manage (RH bug #510926).
%patch112 -p1 -b .clear-old-state-reasons

%patch113 -p1 -b .systray-dbus-exception

# Avoid busy loop in hpcups when backend has exited (RH bug #525944).
%patch114 -p1 -b .hpcups-sigpipe

#patch115 -p1 -b .logdir

# Fixed Device ID parsing code in hpijs's dj9xxvip.c (RH bug #510926).
%patch116 -p1 -b .bad-low-ink-warning

# Hpcups (ljcolor) was putting black lines where should be blank lines (RH bug #579461).
%patch118 -p1 -b .skip-blank-lines

# Added missing newline to string argument in dbglog() call (RH bug #585275).
#patch119 -p1 -b .dbglog-newline

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

# Fixed traceback on error condition in device.py (RH bug #628125).
%patch122 -p1 -b .raw_deviceID-traceback

# Avoid UnicodeDecodeError in printsettingstoolbox.py (RH bug #645739).
%patch123 -p1 -b .UnicodeDecodeError

# Call cupsSetUser in cupsext's addPrinter method before connecting so
# that we can get an authentication callback (RH bug #538352).
%patch124 -p1 -b .addprinter

# Catch D-Bus exceptions in fax dialog (RH bug #645316).
%patch125 -p1 -b .dbus-exception

# Catch GError exception when notification showing failed (RH bug #665577).
#patch126 -p1 -b .notification-exception

# Applied patch to fix CVE-2010-4267, remote stack overflow
# vulnerability (RH bug #670252).
#patch127 -p1 -b .CVE-2010-4267

# Avoid KeyError in ui4/wifisetupdialog.py (RH bug #680939).
%patch128 -p1 -b .wifisetup

# Don't run 'chgrp lp /var/log/hp' in makefile (removes all lines with "chgrp")
sed -i '/chgrp/d' Makefile.am

# Pay attention to the SANE localOnly flag in hpaio (RH bug #743593).
%patch130 -p1 -b .hpaio-localonly

sed -i.duplex-constraints \
    -e 's,\(UIConstraints.* \*Duplex\),//\1,' \
    prnt/drv/hpcups.drv.in

#patch131 -p1 -b .ipp-accessors
#patch132 -p1 -b .hplip-IEEE-1284-4
#patch133 -p1 -b .check

# Debian/Ubuntu patches

# This patch tries to make sure that black is printed with just
# the black pen, if the printer supports it
%patch201 -p1 -b .01_rss

# shebang fixes
%patch202 -p1 -b .10_shebang_fixes

# code cleanup related to char signedness
%patch203 -p1 -b .14_charsign

# compiling ui files to py
%patch204 -p1 -b .85_rebuild_python_ui

# place html documentation under hplip-doc/HTML/
%patch205 -p1 -b .87_move_documentation

# Corrections on the models.dat entry for the HP PhotoSmart Pro B9100,
# especially for the correct color calibration mode.
%patch206 -p1 -b .hplip-photosmart_b9100_support

# Fixes Short-edge duplex printing if duplex is PJL-controlled
# https://bugs.launchpad.net/hplip/+bug/244295
%patch207 -p1 -b .hplip-pjl-duplex-binding

# original patch from debian, path to kdesu added for %%_libdir on x86_64
%patch208 -p1 -b .mga-kde4-kdesudo-support

# https://bugs.launchpad.net/debian/+source/hplip/+bug/530746
%patch209 -p1 -b .hp-check-groups

%patch211 -p1 -b .hp-setup-prompt-for-custom-PPDs

%patch213 -p1 -b .hp-mkuri-take-into-account-already-installed-plugin-also-for-exit-value

# disable for now, as this changes default hplip behavior
# and change in default scanning application should be decided by a poll first
#%patch215 -p1 -b .simple-scan-as-default

%patch216 -p1 -b .make-commafy-correctly-work-with-python-2

#patch217 -p1 -b .mga-remove-duplicate-entry-for-cp1700-in-drv-files

# dlopen libhpmud.so.0 instead of libhpmud.so, in order not to depend on
# devel package (http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=548379)
# obsoletes hplip-3.9.8-dlopen-libhpmud.patch, newer & extended version
%patch219 -p1 -b .try_libhpmud.so.0

%patch220 -p1 -b .add-lidil-two-cartridge-modes
# fixed by upstream
#patch224 -p1 -b .hplip-syslog-fix-debug-messages-to-error

%patch225 -p1 -b .hpfax-bug-function-used-before-importing-log

%patch226 -p1 -b .hp-systray-make-menu-title-visible-in-sni-qt-indicator

%patch227 -p1 -b .hp-systray-make-menu-appear-in-sni-qt-indicator-with-kde

%patch228 -p1 -b .hpaio-option-duplex

%patch301 -p0 -b .fix-uninitialized-variables

# Use filter foomatic-rip instead of foomatic-rip-hplip (fix from Mandriva)
for PPDGZ in ppd/hpijs/*.ppd.gz
do
mv -T "$PPDGZ" "$PPDGZ.old"
zcat "$PPDGZ.old" | sed -e 's/foomatic-rip-hplip/foomatic-rip/' | gzip -c > "$PPDGZ"
rm -f "$PPDGZ.old"
done

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
%configure2_5x \
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
	--enable-policykit \
	--with-mimedir=%{_datadir}/cups/mime

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/hp

%makeinstall_std

# Install files which the "make install" missed to install
install -m 644 ip/hpip.h %{buildroot}%{_includedir}
install -m 644 ip/xform.h %{buildroot}%{_includedir}

# Move doc in sub-package
mv %{buildroot}%{_docdir}/%{name}-%{version}%{extraversion} %{buildroot}%{_docdir}/%{name}-doc-%{version}%{extraversion}

# Remove static libraries of SANE driver
rm -f %{buildroot}%{_libdir}/sane/libsane-hpaio*.la
rm -f %{buildroot}%{_sysconfdir}/sane.d/dll.conf

# Remove other unneeded/unwanted files
rm -f %{buildroot}%{py_platsitedir}/*.la
rm -f %{buildroot}%{_datadir}/hplip/uninstall.*
rm -f %{buildroot}%{_bindir}/hp-uninstall
rm -f %{buildroot}%{_datadir}/hplip/upgrade.*
rm -f %{buildroot}%{_bindir}/hp-upgrade
rm -f %{buildroot}%{_bindir}/hp-config_usb_printer
rm -f %{buildroot}%{_datadir}/hplip/config_usb_printer.*
rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{python_sitearch}/*.la
rm -rf %{buildroot}%{_libdir}/sane/*.la

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

cat > %{buildroot}%{_datadir}/applications/%{_vendor}-hp-sendfax.desktop << EOF
[Desktop Entry]
Name=HP Sendfax
Comment=Utility for sending faxes with HPs multi-function devices
Exec=%{_bindir}/hp-sendfax
Icon=hp-sendfax
Terminal=false
Type=Application
Categories=TelephonyTools;Qt;Printing;Utility;
EOF

install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

# install menu icons
for N in 16 32 48 64; do convert %{SOURCE3} -resize ${N}x${N} $N.png; done
install -D -m 0644 16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/hp-sendfax.png
install -D -m 0644 32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/hp-sendfax.png
install -D -m 0644 48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/hp-sendfax.png
install -D -m 0644 64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/hp-sendfax.png
install -D -m 0644 %{SOURCE3} %{buildroot}%{_iconsdir}/hicolor/128x128/apps/hp-sendfax.png

# switched to udev, no need for hal information
rm -rf  %{buildroot}%{_datadir}/hal/fdi

# Regenerate hpcups PPDs on upgrade if necessary (bug #579355).
install -p -m755 %{SOURCE1} %{buildroot}%{_bindir}/hpcups-update-ppds

# Fedora pstotiff
rm -f %{buildroot}%{_sysconfdir}/cups/pstotiff.types
rm -f %{buildroot}%{_datadir}/cups/mime/pstotiff.types
rm -f %{buildroot}%{_datadir}/hplip/fax/pstotiff*
rm -f %{buildroot}%{_prefix}/lib/cups/filter/hpcac

# bork?
install -d %{buildroot}%{_sysconfdir}/cups
cp -p %{buildroot}%{_datadir}/cups/mime/pstotiff.convs %{buildroot}%{_sysconfdir}/cups/pstotiff.convs

# set up consolehelper
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/hp-setup %{buildroot}%{_sbindir}/hp-setup
ln -s consolehelper %{buildroot}%{_bindir}/hp-setup

# Make sure pyc files are generated, otherwise we can get
# difficult to debug problems
pushd %{buildroot}%{_datadir}/%{name}
python -m compileall .
popd

mkdir -p %{buildroot}%{_localstatedir}/lib/hp/
touch %{buildroot}%{_localstatedir}/lib/hp/hplip.state

mkdir -p %{buildroot}%{_unitdir}
mv -f %{buildroot}/usr/lib/systemd/system/hplip-printer@.service %{buildroot}%{_unitdir}/hplip-printer@.service

%triggerin -- hplip < 2.7.7
chkconfig --del hplip

# Restart CUPS to make the Fax PPD known to it
if [ -f /etc/init.d/cups ]; then
	/sbin/service cups condrestart || :
fi

%post
%tmpfiles_create %{name}

%post -n hplip-hpijs-ppds
# Restart CUPS to make the printing PPDs known to it
if [ -f /etc/init.d/cups ]; then
	/sbin/service cups condrestart || :
fi

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
if [ -f /etc/init.d/cups ]; then
	/sbin/service cups condrestart || :
fi

%postun -n hplip-hpijs-ppds
# Restart CUPS to make the removal of the printing PPDs known to it
if [ -f /etc/init.d/cups ]; then
	/sbin/service cups condrestart || :
fi

%files
%config(noreplace) %{_sysconfdir}/hp
%dir %{_localstatedir}/lib/hp/
%{_bindir}/hp-align
%{_bindir}/hp-clean
%{_bindir}/hp-colorcal
#%{_bindir}/hp-config_usb_printer
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
#%{_bindir}/hp-uninstall
%{_bindir}/hp-unload
#%{_bindir}/hp-upgrade
%{_bindir}/hp-wificonfig

%exclude %{_datadir}/hplip/data/models
# C libraries for Python
%{_libdir}/python*/*/*.so*
# CUPS backends (0755 permissions, so that CUPS 1.2 runs these backends
# as lp user)
# Note: this must be /usr/lib not %{_libdir}, since that's the
# CUPS serverbin directory.
%attr(0755,root,root) %{_prefix}/lib/cups/backend/hp*
%{_prefix}/lib/cups/filter/hplipjs
%{_prefix}/lib/cups/filter/hpcups
%{_prefix}/lib/cups/filter/hpcupsfax
%{_prefix}/lib/cups/filter/hpps
%{_prefix}/lib/cups/filter/pstotiff
%{_datadir}/cups/mime/pstotiff.convs
%config(noreplace) %{_sysconfdir}/cups/pstotiff.convs
%{_datadir}/ppd/HP/HP-Fax*.ppd*
%{_datadir}/cups/drv/hp/hpcups.drv
# Files
%dir %{_datadir}/hplip
%{_datadir}/hplip/align.py*
%{_datadir}/hplip/check-plugin.py*
%{_datadir}/hplip/clean.py*
%{_datadir}/hplip/colorcal.py*
#%{_datadir}/hplip/config_usb_printer.py*
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
%{_datadir}/polkit-1/actions/com.hp.hplip.policy
%{_datadir}/dbus-1/system-services/com.hp.hplip.service
%{_localstatedir}/lib/hp/hplip.state
%dir %attr(0774,root,lp) %{_localstatedir}/log/hp
%dir %attr(1774,root,lp) %{_localstatedir}/log/hp/tmp
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/com.hp.hplip.conf
#%{_sysconfdir}/cron.daily/hplip_cron
%{_sysconfdir}/tmpfiles.d/hplip.conf
%{_unitdir}/hplip-printer@.service
%{_datadir}/hplip/hplip_clean.sh

%files doc
%doc %{_docdir}/%{name}-doc-%{version}%{extraversion}

%files -n %{libhpip}
%{_libdir}/libhpip.so.%{major}*

%files -n %{libhpmud}
%{_libdir}/libhpmud.so.%{major}*

%files -n %{devname}
%{_includedir}/hpip.h
%{_includedir}/xform.h
%{_libdir}/libhpip.so
%{_libdir}/libhpmud.so
%if %{sane_backend}
%{_libdir}/sane/libsane-hpaio.so

%files -n %{libsane}
%{_libdir}/sane/libsane-hpaio.so.%{sanemaj}*
%endif

%files model-data
%{_sysconfdir}/udev/rules.d/*.rules
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
%{_bindir}/hpcups-update-ppds

%files hpijs-ppds
%{_datadir}/ppd/HP/apollo*.ppd*
%{_datadir}/ppd/HP/hp-*.ppd*

