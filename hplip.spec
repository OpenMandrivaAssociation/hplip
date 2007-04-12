# Define if you want to build the sane backend (default)
%define sane_backend		1
%{?_with_sane:			%global sane_backend 1}
%{?_without_sane:		%global sane_backend 0}

%define hpip_major		0
%define hpip_libname		%mklibname hpip %{hpip_major}

%define sane_hpaio_major		1
%define sane_hpaio_libname	%mklibname sane-hpaio %{sane_hpaio_major}

# Suppress automatically generated Requires for devel packages
%define _requires_exceptions devel\(.*\)

##### GENERAL STUFF #####

#define extraversion -rc3
%define extraversion %nil

Summary:	HP printer/all-in-one driver infrastructure
Name:		hplip
Version:	1.6.12
Release:	%mkrel 2
License:	GPL/MIT/BSD
Group:		System/Servers

%define mdv2007 %(perl -e 'print ("%release" =~ /mdv/ ? 1 : 0)')



##### SOURCE FILES #####

Source: http://heanet.dl.sourceforge.net/sourceforge/hplip/%{name}-%{version}%{extraversion}.tar.gz
# Icon for the Mandriva menu
Source1: hplip.png.bz2

##### PATCHES #####

# Let SNMP stuff really getting built
#Patch0: hplip-0.8.8.patch.bz2

# Support for HP PSC 750xi
#Patch1: hplip-0.9-HP-PSC_950xi.patch.bz2

# Fix battery level check for HP DeskJet 450
#Patch2: hplip-0.9.1-HP-DeskJet_450-Battery.patch.bz2

# Some HP PhotoSmart 7150 identify themselves as "hp photosmart 7150~"
Patch3: hplip-1.6.12-HP-PhotoSmart_7150tilde.patch

# 64-bit fixes
# NOTE: knowingly overflowing as on 32-bit platforms under certain conditions
#Patch4: hplip-0.9.4-64bit-fixes.patch.bz2

# Remove "su" from startup script
#Patch5: hplip-0.9.5-startup-script.patch.bz2

# Let the HPLIP toolbox start the browser to access the web interface
# of a LAN printer in the background, so that one can still work in
# the toolbox while the browser is open.
#Patch6: hplip-0.9.4-browser-launch.patch.bz2

# Fix full-bleed on Letter, A4 or bigger paper
#Patch7: hplip-0.9.4-letter-a4-full-bleed.patch.bz2

# Fix PML scanning regression in HPLIP 0.9.5 (official patch from HP)
#Patch8: hplip-0.9.5-pml-scannning-big-endian-pc.patch.bz2

# Assorted fixes from Debian and Ubuntu (Thanks to
# Henrique de Moraes Holschuh from Debian)
#Patch9: hplip-0.9.5-11_fix-misc-gcc-warnings.patch.bz2
#Patch10: hplip-0.9.5-13_intsign-fixes.patch.bz2
Patch11: hplip-1.6.12-14_charsign_fixes.patch
#Patch12: hplip-0.9.5-15_64bit_fixes.patch.bz2
#Patch13: hplip-0.9.5-20_fix_unitialized_var_bugs.patch.bz2
#Patch14: hplip-0.9.5-50_hp-clean_fix.patch.bz2
#Patch15: hplip-0.9.5-99_ubuntu_hplip-deroot.patch.bz2

# Official 0.9.7 bugfix patch from HP
#Patch16: hplip-0.9.7-2.patch.bz2

# Official 0.9.8 bugfix patch from HP
#Patch17: hplip-0.9.8-4.patch.bz2

# Fix problem of HP PSC 950 series printers not being correctly
# recognized and a duplex bug
#Patch18: hplip-0.9.11-2.patch.bz2

##### ADDITIONAL DEFINITIONS #####

Url:		http://hpinkjet.sourceforge.net/
%if %{sane_backend}
BuildRequires:	libsane-devel, xsane
%endif
BuildRequires:	python-devel
BuildRequires:	PyQt >= 3.13-2mdk, sip >= 4.1.1
BuildRequires:	net-snmp-devel
BuildRequires:	libusb-devel >= 0.1.8
BuildRequires:  ImageMagick
BuildRequires:  autoconf2.5
%ifarch x86_64
BuildRequires:	libcups-devel >= 1.2.0-0.5361.0mdk
%else
BuildRequires:	libcups-devel
%endif
#Conflicts: 	hpoj
Prereq:		rpm-helper
Requires:	foomatic-filters, cups, PyQt >= 3.13-2mdk, sip >= 4.1.1
Requires:	hplip-model-data hplip-hpijs
# Needed for communicating with ethernet-connected printers
Requires:	net-snmp-mibs
# Needed to generate fax cover pages
Requires:	python-reportlab
%ifarch x86_64
Conflicts:	cups < 1.2.0-0.5361.0mdk
%endif
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



##### SUB-PACKAGES #####

%package -n %{hpip_libname}
Summary: Dynamic library for the "hplip" HP printer/all-in-one drivers
Group: System/Servers

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
Group: System/Servers
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
Group: System/Servers

%description model-data
HPLIP supports most current HP printers and multifunction devices, but
there are some older models not supported. This package contains the
list of supported models. Printerdrake installs it automatically to
determine whether HPLIP has to be installed or not.

%package hpijs
Summary: HPs printer driver IJS plug-in for GhostScript
Group: System/Servers
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
Group: System/Servers
Requires: foomatic-filters, hplip-hpijs

%description hpijs-ppds

PPD files to use the HPIJS printer driver with foomatic-rip and a
printer spooler like CUPS, LPRng, PDQ, ...

%package doc
Summary:	Documentation for HPLIP
Group:		System/Servers

%description doc
This package contains documentation for the HPLIP driver.

This is the HP driver package to supply Linux support for most
Hewlett-Packard DeskJet, LaserJet, PSC, OfficeJet, and PhotoSmart
printers and all-in-one peripherals (also known as Multi-Function
Peripherals or MFPs), which can print, scan, copy, fax, and/or access
flash memory cards.



##### PREP #####

%prep
rm -rf $RPM_BUILD_DIR/%{name}-%{version}%{extraversion}
%setup -q -n %{name}-%{version}%{extraversion}
#patch0 -p1

# Support for HP PSC 750xi
#patch1 -p0

# Fix battery level check for HP DeskJet 450
#patch2 -p0

# Some HP PhotoSmart 7150 identify themselves as "hp photosmart 7150~"
%patch3 -p1 -b .hpps7150

#patch4 -p1 -b .64bit-fixes

#patch5 -p0 -b .startup

#patch6 -p0 -b .browser

#patch7 -p0 -b .fullbleed

#patch8 -p1 -b .pmlscan

#patch9 -p0 -b .11gccwarn

#patch10 -p0 -b .13intsign

%patch11 -p1 -b .14charsign

#patch12 -p0 -b .15_64bit

#patch13 -p0 -b .20uninit

#patch14 -p0 -b .50hpclean

#patch15 -p0 -b .99nonroot

#patch16 -p1 -b .hp0972

#patch17 -p1 -b .hp0984

#patch18 -p1 -b .psc950duplex

# Load menu icon
bzcat %{SOURCE1} > hplip.png

# Let configure not use /usr/lib/menu/hplip as icon directory, it is the
# place of our menu file
perl -p -i -e 's:/usr/lib/menu::g' configure.in

# Make all files in the source user-writable
chmod -R u+w .
#perl -p -i -e 's:^(\s*cp\s+fax/ppd/HP-Fax-hplip.ppd\s+prnt/hpijs/ppd/):\#$1:' Makefile.in

# "make install" gzips a directory which contains an already gzipped file,
# override the exit state of gzip
#perl -p -i -e 's/(gzip\s+-qf\s+.*)$/$1 || :/' prnt/hpijs/Makefile*

##### BUILD #####

%build
%serverbuild

#export CFLAGS="-g"
#export CXXFLAGS="-g"

autoconf-2.5x
%if !%{sane_backend}
WITHOUT_SANE="--without-sane"
%endif
#configure2_5x --enable-rpm-install $WITHOUT_SANE
%configure2_5x $WITHOUT_SANE

%make

# convert icons to required sizes
mv %{name}.png %{name}.mini.png
convert %{name}.mini.png -resize 32x32 %{name}.png
convert %{name}.mini.png -resize 48x48 %{name}.large.png

##### INSTALL #####

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/hp
mkdir -p %{buildroot}/var/run/hplip

# Let %{buildroot} also be used when C libraries for Perl are installed
#perl -p -i -e 's:(setup.py install):$1 --root=%{buildroot}:' Makefile */Makefile */*/Makefile

# Do not use the macro here, use the standard DESTDIR method as it works
# with HPLIP, in contrary to the non-standard Mandriva method
#make test-destdir DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}

# Enter directories in startup file
perl -p -i -e 's:HPIODDIR=:HPIODDIR=%{_sbindir}:' %{buildroot}%{_datadir}/%{name}/%{name}.sh
perl -p -i -e 's:HPSSDDIR=:HPSSDDIR=%{_datadir}/%{name}:' %{buildroot}%{_datadir}/%{name}/%{name}.sh

# Set priority in startup file for HPLIP to get started before CUPS
perl -p -i -e 's/chkconfig: 2345 50 10/chkconfig: 2345 14 61/' %{buildroot}%{_datadir}/%{name}/%{name}.sh

# Install configuration and startup files
mv %{buildroot}%{_datadir}/%{name}/%{name}.conf %{buildroot}%{_sysconfdir}/hp
mv %{buildroot}%{_datadir}/%{name}/%{name}.sh %{buildroot}%{_initrddir}/%{name}

# Install files which the "make install" missed to install
install -m 644 ip/hpip.h %{buildroot}%{_includedir}
install -m 644 ip/xform.h %{buildroot}%{_includedir}

# Make SANE scanner driver modules available in the right place (SANE
# only finds them in /usr/lib/sane, not in /usr/lib
%if %{sane_backend}
install -d %{buildroot}%{_libdir}/sane
(cd %{buildroot}%{_libdir}/sane/ && ln -sf ../libsane-* .)
%else
rm -rf %{buildroot}/%{_libdir}/libsane-hpaio.so.*
%endif

# Move fax PPD to be part of main HPLIP package and not of the HPIJS PPDs
#mv %{buildroot}/%{_datadir}/ppd/HP/HP-Fax*.ppd.gz %{buildroot}/%{_datadir}/cups/model/

# Move doc in sub-package
mv %{buildroot}%{_docdir}/%{name}-%{version}%{extraversion} %{buildroot}%{_docdir}/%{name}-doc-%{version}%{extraversion}

# Remove static libraries of SANE driver
rm -f %{buildroot}%{_libdir}/libsane-hpaio*.so
rm -f %{buildroot}%{_libdir}/libsane-hpaio*.a
rm -f %{buildroot}%{_libdir}/libsane-hpaio*.la
rm -f %{buildroot}%{_libdir}/sane/libsane-hpaio*.so
rm -f %{buildroot}%{_libdir}/sane/libsane-hpaio*.a
rm -f %{buildroot}%{_libdir}/sane/libsane-hpaio*.la

# Remove foomatic-rip, as Mandriva Linux already contains Foomatic
rm -f %{buildroot}%{_bindir}/foomatic-rip
rm -f %{buildroot}%{_prefix}/lib*/cups/filter/foomatic-rip

# Remove other unneeded files
rm -f %{buildroot}%{_sysconfdir}/init.d/hplip
rm -f %{buildroot}%{_sysconfdir}/sane.d/dll.conf

# install menu icons
mkdir -p %{buildroot}%{_iconsdir}/locolor/16x16/apps/
install -m 644 %{name}.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 %{name}.mini.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 %{name}.large.png -D %{buildroot}%{_liconsdir}/%{name}.png

# install menu entry
mkdir -p %{buildroot}%{_menudir}

cat <<EOF > %{buildroot}%{_menudir}/hplip
?package(hplip): needs=X11 \
section=System/Monitoring \
title="HP Printer Toolbox" \
longtitle="Maintenance and monitoring utility for HP printers" \
command="%{_bindir}/hp-toolbox" \
%if %mdv2007
xdg=true \
%endif
icon="%{name}.png"
?package(hplip): needs=X11 \
section=Office/Communications/Fax \
title="HP Sendfax" \
longtitle="Utility for sending faxes with HP's multi-function devices" \
command="%{_bindir}/hp-sendfax" \
%if %mdv2007
xdg=true \
%endif
icon="%{name}.png"
EOF

%if %mdv2007
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-hp-toolbox.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=HP Printer Toolbox
Comment=Maintenance and monitoring utility for HP printers
Exec=%{_bindir}/hp-toolbox
Icon=%{name}.png
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Configuration-Printing;Settings;HardwareSettings;X-MandrivaLinux-System-Monitoring;System;Monitor;
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-hp-sendfax.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=HP Sendfax
Comment=Utility for sending faxes with HP's multi-function devices
Exec=%{_bindir}/hp-sendfax
Icon=%{name}.png
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Office-Communications-Fax;
EOF
%endif

# Set link for easy access to the toolbox
#ln -s %{_datadir}/hplip/toolbox %{buildroot}%{_bindir}



##### PRE/POST INSTALL SCRIPTS #####

%post
# Let HPLIP daemons be automatically started at boot time
%_post_service hplip
# Menu update
%{update_menus}
# Restart CUPS to make the Fax PPD known to it
/sbin/service cups condrestart > /dev/null 2>/dev/null || :

%post -n hplip-hpijs-ppds
# Restart CUPS to make the printing PPDs known to it
/sbin/service cups condrestart > /dev/null 2>/dev/null || :

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

%preun
# Let HPLIP daemons not be automatically started at boot time any more
%_preun_service hplip

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
/sbin/service cups condrestart > /dev/null 2>/dev/null || :

%postun -n hplip-hpijs-ppds
# Restart CUPS to make the removal of the printing PPDs known to it
/sbin/service cups condrestart > /dev/null 2>/dev/null || :

# Reload the library lists when uninstalling shared libraries
%postun -n %{hpip_libname} -p /sbin/ldconfig

%if %{sane_backend}
%postun -n %{sane_hpaio_libname}
/sbin/ldconfig
%endif


##### CLEAN UP #####

%clean
rm -rf %{buildroot}


##### FILE LISTS FOR ALL BINARY PACKAGES #####

##### hplip
%files
%defattr(-,root,root)
#doc COPYING doc/*
%config(noreplace) %{_sysconfdir}/hp
%config(noreplace) %{_initrddir}/*
%{_sbindir}/hpiod
%dir /var/run/hplip/
#{_bindir}/toolbox
%{_bindir}/hp-*
%{_datadir}/hplip/[A-Za-c_]*
%{_datadir}/hplip/data/*
%exclude %{_datadir}/hplip/data/models
%{_datadir}/hplip/[e-z]*
# C libraries for Python
%{_libdir}/python*/*/*.so*
%{py_platsitedir}/*.egg-info
# CUPS backends (0700 permissions, so that CUPS 1.2 runs these backends
# as root)
%attr(0700,root,root) %{_prefix}/lib*/cups/backend/hp*
%{_datadir}/ppd/HP/fax
# menu entry
%{_iconsdir}/*.png
%{_iconsdir}/*/*.png
%{_menudir}/*
%{_datadir}/applications/*

%files doc
%defattr(-,root,root)
%doc %{_docdir}/%{name}-doc-%{version}%{extraversion}

##### %{hpip_libname}
%files -n %{hpip_libname}
%defattr(-,root,root)
%{_libdir}/libhpip*.so.*

##### %{hpip_libname}-devel
%files -n %{hpip_libname}-devel
%defattr(-,root,root)
%{_includedir}/hpip.h
%{_includedir}/xform.h
%{_libdir}/libhpip*.so
#%{_libdir}/libhpip*.a
%{_libdir}/libhpip*.la

%if %{sane_backend}

##### %{sane_hpaio_libname}
%files -n %{sane_hpaio_libname}
%defattr(-,root,root)
%{_libdir}/libsane-hpaio*.so.*
%{_libdir}/sane/libsane-hpaio*.so.*

%if 0
##### %{sane_hpaio_libname}-devel
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

##### model-data
%files model-data
%defattr(-,root,root)
%{_datadir}/hplip/data/models

##### hpijs
%files hpijs
%defattr(-,root,root)
%doc %{_defaultdocdir}/hpijs-2.*
#doc %{_defaultdocdir}/hpijs*
%{_bindir}/hpijs
# Needed for both printing and fax PPDs. They all need HPIJS, therefore
# the link is here
%{_datadir}/cups/model/foomatic-ppds
%dir %{_datadir}/ppd
%dir %{_datadir}/ppd/HP

##### hpijs-ppds
%files hpijs-ppds
%defattr(-,root,root)
%{_datadir}/ppd/HP/*.ppd*



