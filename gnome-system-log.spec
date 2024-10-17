%define _disable_rebuild_configure 1
%define url_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	GNOME System log utility
Name:		gnome-system-log
Version:	3.9.90
Release:	8
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		https://www.gnome.org
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(glib-2.0) >= 2.31.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0.0
Requires:	usermode-consoleonly
Conflicts:	gnome-utils < 1:3.3.1

%description
Gnome System log utility.

%prep
%setup -q

%build
%configure \
	--disable-schemas-compile
%make_build

%install
%make_install

# make gnome-system-log use consolehelper until it starts using polkit
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
cat <<EOF > %{buildroot}%{_sysconfdir}/pam.d/gnome-system-log
#%%PAM-1.0
auth		include		system-auth
account		include		system-auth
session		include		system-auth
EOF

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat <<EOF > %{buildroot}%{_sysconfdir}/security/console.apps/gnome-system-log
USER=root
PROGRAM=/usr/sbin/gnome-system-log
SESSION=true
FALLBACK=true
EOF


%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc NEWS
%{_sysconfdir}/pam.d/gnome-system-log
%{_sysconfdir}/security/console.apps/gnome-system-log
%{_bindir}/*
%{_datadir}/GConf/gsettings/logview.convert
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-system-log.gschema.xml
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/logview.png
%{_iconsdir}/HighContrast/*/apps/logview.png
%{_mandir}/man1/%{name}.1.*

