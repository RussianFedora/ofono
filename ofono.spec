Name:           ofono
Version:        0.44
Release:        1%{?dist}
Summary:        oFono - Open Source Telephony

Group:          System Environment/Daemons
License:        GPLv2
URL:            http://ofono.org/
Source0:        http://www.kernel.org/pub/linux/network/ofono/ofono-0.44.tar.bz2
Source1:	%{name}.initscript
Source2:	%{name}.sysconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  glib-devel dbus-devel libudev-devel >= 143 bluez-libs-devel >= 4.30
#Requires:       

%description
oFono - Open Source Telephony. which provides an oFono stack for interfacing mobile telephony devices.

%package devel
Summary:	Development files for oFono
Group:		Development/Libraries
Requires:	glib-devel dbus-devel libudev-devel>=143 bluez-libs-devel>=4.30 %{name} = %{version}-%{release}

%description devel
Headers and pkconfig for oFono

%package test-tools
Summary:	Test tools for oFono
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description test-tools
Test tools for oFono

%prep
%setup -q

%build
%configure --enable-threads --enable-test
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %{?fedora}<15
install -D -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initddir}/%{name}
install -D -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%config %{_sysconfdir}/dbus-1/system.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/phonesim.conf

%if %{?fedora}<15
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initddir}/%{name}
%endif

/lib/systemd/system/%{name}.service
/lib/udev/rules.d/97-ofono.rules
%dir %{_localstatedir}/lib/%{name}
%{_sbindir}/%{name}d
%{_mandir}/man8/%{name}d.8.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/%{name}.pc

%files test-tools
%defattr(-,root,root,-)
%{_libdir}/%{name}/test/*

%changelog
* Tue Mar 15 2011 Alexei Panov <elemc AT atisserv DOT ru> - 0.44-1
- initial build
