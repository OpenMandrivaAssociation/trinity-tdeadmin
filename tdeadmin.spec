%bcond clang 1
%bcond lilo 0
%bcond consolehelper 1

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 3

%define tde_pkg tdeadmin
%define tde_prefix /opt/trinity

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# Avoids relinking, which breaks consolehelper
%define dont_relink 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Summary:	Administrative tools for TDE
Version:	%{tde_version}
Release:	%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Group:		System/GUI/Other
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/core/%{tarball_name}-%{version}%{?preversion:~%{preversion}}.tar.xz
Source1:		kuser.pam
Source2:		kuser.pamd
Source5:		kpackagerc
Source6:		ksysvrc
Source7:		kuserrc

BuildSystem:    cmake

BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DPKGCONFIG_INSTALL_DIR=%{tde_prefix}/%{_lib}/pkgconfig
BuildOption:    -DBUILD_ALL=ON -DBUILD_DOC=ON -DBUILD_KCRON=ON 
BuildOption:    -DBUILD_KDAT=ON -DBUILD_KNETWORKCONF=ON -DBUILD_KPACKAGE=ON
BuildOption:    -DBUILD_KSYSV=ON -DBUILD_KUSER=ON -DBUILD_LILO_CONFIG=ON
BuildOption:    -DBUILD_SECPOLICY=ON -DBUILD_TDEFILE_PLUGINS=ON 
BuildOption:    -DKU_USERPRIVATEGROUP=false 
BuildOption:    -DKU_HOMEDIR_PERM="0700"
BuildOption:    -DKU_HOMETEMPLATE="/home/%U"
BuildOption:    -DKU_MAILBOX_GID="0"
BuildOption:    -DKU_MAILBOX_PERM="0660"
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

Obsoletes:		trinity-kdeadmin < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-kdeadmin = %{?epoch:%{epoch}:}%{version}-%{release}

BuildRequires:	trinity-arts-devel >= %{tde_epoch}:1.5.10
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}

BuildRequires:	trinity-tde-cmake >= %{tde_version}
BuildRequires:	libtool
BuildRequires:	fdupes

%{!?with_clang:BuildRequires:	gcc-c++}

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

# RPM support
BuildRequires: pkgconfig(rpm)

# PAM support
BuildRequires: pkgconfig(pam)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)

# LILO support
%{?with_lilo:BuildRequires:	lilo}

Requires: trinity-kcron = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: trinity-kdat = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-kfile-plugins = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: trinity-knetworkconf = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: trinity-kpackage = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: trinity-ksysv = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: trinity-kuser = %{?epoch:%{epoch}:}%{version}-%{release}
%if %{with lilo}
Requires: trinity-lilo-config = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Obsoletes: trinity-lilo-config < %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description
The tdeadmin package includes administrative tools for the Trinity Desktop
Environment (TDE) including:
kcron, kdat, knetworkconf, kpackage, ksysv, kuser.

%files
%defattr(-,root,root,-)

##########

%package -n trinity-kcron
Summary:	The Trinity crontab editor
Group:		System/GUI/Other

%description -n trinity-kcron
KCron is an application for scheduling programs to run in the background.
It is a graphical user interface to cron, the UNIX system scheduler.

%files -n trinity-kcron
%defattr(-,root,root,-)
%{tde_prefix}/bin/kcron
%{tde_prefix}/share/applications/tde/kcron.desktop
%{tde_prefix}/share/apps/kcron/
%{tde_prefix}/share/icons/hicolor/*/apps/kcron.png
%{tde_prefix}/share/doc/tde/HTML/en/kcron/

##########

%package -n trinity-kdat
Summary:	A Trinity tape backup tool
Group:		System/GUI/Other

%description -n trinity-kdat
KDat is a tar-based tape archiver. It is designed to work with multiple
archives on a single tape.

Main features are:
* Simple graphical interface to local filesystem and tape contents.
* Multiple archives on the same physical tape.
* Complete index of archives and files is stored on local hard disk.
* Selective restore of files from an archive.
* Backup profiles for frequently used backups.

%files -n trinity-kdat
%defattr(-,root,root,-)
%doc rpmdocs/kdat/*
%{tde_prefix}/bin/kdat
%{tde_prefix}/share/applications/tde/kdat.desktop
%{tde_prefix}/share/apps/kdat/
%{tde_prefix}/share/icons/hicolor/*/apps/kdat.png
%{tde_prefix}/share/icons/locolor/*/apps/kdat.png
%{tde_prefix}/share/doc/tde/HTML/en/kdat/

##########

%package kfile-plugins
Summary:	Trinity file metainfo plugins for deb and rpm files
Group:		System/GUI/Other

%description kfile-plugins
This package contains the Trinity File metainfo plugins for deb and rpm
package files.

%files kfile-plugins
%defattr(-,root,root,-)
%{tde_prefix}/%{_lib}/trinity/tdefile_deb.la
%{tde_prefix}/%{_lib}/trinity/tdefile_deb.so
%{tde_prefix}/%{_lib}/trinity/tdefile_rpm.la
%{tde_prefix}/%{_lib}/trinity/tdefile_rpm.so
%{tde_prefix}/share/services/tdefile_deb.desktop
%{tde_prefix}/share/services/tdefile_rpm.desktop

##########

%package -n trinity-knetworkconf
Summary:	Trinity network configuration tool
Group:		System/GUI/Other

%description -n trinity-knetworkconf
This is a TDE control center module to configure TCP/IP settings.  It
can be used to manage network devices and settings for each device.

%files -n trinity-knetworkconf
%defattr(-,root,root,-)
%doc rpmdocs/knetworkconf/*
%{tde_prefix}/share/icons/hicolor/*/apps/knetworkconf.png
%{tde_prefix}/share/icons/hicolor/22x22/actions/network_disconnected_wlan.png
%{tde_prefix}/share/icons/hicolor/22x22/actions/network_connected_lan_knc.png
%{tde_prefix}/share/icons/hicolor/22x22/actions/network_disconnected_lan.png
%{tde_prefix}/share/icons/hicolor/22x22/actions/network_traffic_wlan.png
%{tde_prefix}/share/apps/knetworkconf/
%{tde_prefix}/share/applications/tde/kcm_knetworkconfmodule.desktop
%{tde_prefix}/%{_lib}/trinity/kcm_knetworkconfmodule.so
%{tde_prefix}/%{_lib}/trinity/kcm_knetworkconfmodule.la
%{tde_prefix}/share/doc/tde/HTML/en/knetworkconf/

##########

%package -n trinity-kpackage
Summary:	Trinity package management tool
Group:		System/GUI/Other

%description -n trinity-kpackage
This is a frontend to both .rpm and .deb package formats. It allows you
to view currently installed packages, browse available packages, and
install/remove them.

%files -n trinity-kpackage
%defattr(-,root,root,-)
%doc rpmdocs/kpackage/*
%{tde_prefix}/bin/kpackage
%{tde_prefix}/share/applications/tde/kpackage.desktop
%{tde_prefix}/share/apps/kpackage/
%config(noreplace) %{_sysconfdir}/trinity/kpackagerc
%{tde_prefix}/share/icons/hicolor/*/apps/kpackage.png
%{tde_prefix}/share/doc/tde/HTML/en/kpackage/

##########

%package -n trinity-ksysv
Summary:	Trinity SysV-style init configuration editor
Group:		System/GUI/Other

%description -n trinity-ksysv
This program allows you to edit your start and stop scripts using a
drag and drop GUI.

%files -n trinity-ksysv
%defattr(-,root,root,-)
%doc rpmdocs/ksysv/*
%{tde_prefix}/bin/ksysv
%{tde_prefix}/share/applications/tde/ksysv.desktop
%{tde_prefix}/share/apps/ksysv/
%config(noreplace) %{_sysconfdir}/trinity/ksysvrc
%{tde_prefix}/share/icons/hicolor/*/apps/ksysv.png
%{tde_prefix}/share/mimelnk/application/x-ksysv.desktop
%{tde_prefix}/share/mimelnk/text/x-ksysv-log.desktop
%{tde_prefix}/share/doc/tde/HTML/en/ksysv/

##########

%package -n trinity-kuser
Summary:	Trinity user/group administration tool
Group:		System/GUI/Other

%if %{with consolehelper}
# package 'usermode' provides '/usr/bin/consolehelper-gtk'
Requires:	usermode
%endif

%description -n trinity-kuser
A user/group administration tool for TDE.

%files -n trinity-kuser
%defattr(-,root,root,-)
%doc rpmdocs/kuser/*
%{tde_prefix}/bin/kuser
%{tde_prefix}/share/applications/tde/kuser.desktop
%{tde_prefix}/share/apps/kuser/
%config(noreplace) %{_sysconfdir}/trinity/kuserrc
%{tde_prefix}/share/config.kcfg/kuser.kcfg
%{tde_prefix}/share/icons/hicolor/*/apps/kuser.png
%{tde_prefix}/share/doc/tde/HTML/en/kuser/

%if %{with consolehelper}
%{tde_prefix}/sbin/kuser
%{_sbindir}/kuser
%config(noreplace) /etc/pam.d/kuser
%config(noreplace) /etc/security/console.apps/kuser
%endif

##########

%if %{with lilo}
%package -n trinity-lilo-config
Summary:	Trinity frontend for lilo configuration
Group:		System/GUI/Other
Requires:	trinity-kcontrol
Requires:	trinity-tdebase-bin
#Requires:	lilo

%description -n trinity-lilo-config
lilo-config is a TDE based frontend to the lilo boot manager configuration.
It runs out of the Trinity Control Center.

If you want to use the menu entry to launch lilo-config, you need to install
tdebase-bin since it uses the tdesu command to gain root privileges.

%files -n trinity-lilo-config
%defattr(-,root,root,-)
%{tde_prefix}/%{_lib}/trinity/kcm_lilo.la
%{tde_prefix}/%{_lib}/trinity/kcm_lilo.so
%{tde_prefix}/share/applications/tde/lilo.desktop
%{tde_prefix}/share/doc/tde/HTML/en/lilo-config/

%post -n trinity-lilo-config
touch /etc/lilo.conf
%endif


%conf -p
unset QTDIR QTLIB QTINC
export PATH="%{tde_prefix}/bin:${PATH}"


%install -a
comps="kcron kdat knetworkconf kpackage ksysv kuser"
%__mkdir_p	%{buildroot}%{tde_prefix}/share/config \
			%{buildroot}%{_sysconfdir}/security/console.apps \
			%{buildroot}%{_sysconfdir}/pam.d \
			%{buildroot}%{tde_prefix}/sbin \
			%{buildroot}%{_sbindir}

%__mkdir_p "%{buildroot}%{_sysconfdir}/trinity/"
%__install -p -m644 %{SOURCE5} %{SOURCE6} %{SOURCE7} "%{buildroot}%{_sysconfdir}/trinity/"

%if %{with consolehelper}
# Run kuser through consolehelper
%__install -p -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/security/console.apps/kuser
%__install -p -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/kuser
%__mv %{buildroot}%{tde_prefix}/bin/kuser %{buildroot}%{tde_prefix}/sbin
%__ln_s %{_bindir}/consolehelper %{buildroot}%{tde_prefix}/bin/kuser
%if "%{tde_prefix}" != "/usr"
%__ln_s %{tde_prefix}/sbin/kuser %{?buildroot}%{_sbindir}/kuser
%endif
%endif

# rpmdocs
for dir in $comps ; do
  for file in AUTHORS ChangeLog README TODO ; do
    test -s  "$dir/$file" && install -p -m644 -D "$dir/$file" "rpmdocs/$dir/$file"
  done
done

# The following files are not installed in any binary package.
# This is deliberate.

# - This file serves no purpose that we can see, and conflicts
#   with GNOME system tools, so be sure to leave it out.
%__rm -f %{?buildroot}%{tde_prefix}/%{_lib}/pkgconfig/*.pc

# Extract from changelog:
# tdeadmin (4:3.5.5-2) unstable; urgency=low
#  +++ Changes by Ana Beatriz Guerrero Lopez:
#  * Removed useless program secpolicy. (Closes: #399426)
%__rm -f %{?buildroot}%{tde_prefix}/bin/secpolicy

# Remove lilo related files, if unwanted.
%if %{without lilo}
%__rm -rf %{?buildroot}%{tde_prefix}/share/doc/tde/HTML/en/lilo-config/
%__rm -f %{?buildroot}%{tde_prefix}/%{_lib}/trinity/kcm_lilo.la
%__rm -f %{?buildroot}%{tde_prefix}/%{_lib}/trinity/kcm_lilo.so
%__rm -f %{?buildroot}%{tde_prefix}/share/applications/tde/lilo.desktop
%endif

# Links duplicate files
%fdupes "%{?buildroot}%{tde_prefix}/share"

