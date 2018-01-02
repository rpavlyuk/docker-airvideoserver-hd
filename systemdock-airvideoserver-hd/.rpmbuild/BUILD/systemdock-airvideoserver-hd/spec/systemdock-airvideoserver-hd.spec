%define		_profile airvideoserver-hd
%define         _module systemdock-%{_profile}

# SVAROG-related variables
%{!?svn_revision:%define svn_revision 1}
# COMPATIBILITY FIX: Jenkins job name is neccessary to make build root unique (for CentOS5 and earlier)
%{!?JOB_NAME:%define JOB_NAME standalone}


Name:		%{_module}
Version:	0.1
Release:	%{svn_revision}%{?dist}
Summary:	SystemDock profile to run AirVideoServerHD container as systemd service

Group:		Tools/Other
License:	GPLv3
URL:		https://github.com/rpavlyuk/docker-airvideoserver-hd
Packager:       Roman Pavlyuk <roman.pavlyuk@gmail.com>
Source:         %{_module}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)-%{JOB_NAME}
BuildArch:      noarch

Requires:	systemdock
Requires:	systemd
Requires:	docker-airvideoserver-hd

%description
SystemDock profile to run airvideoserver-hd container as systemd service

%prep
%setup -n %{_module}

%build
# Nothing

%install
%make_install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
ln -s %{_sysconfdir}/systemdock/containers.d/%{_profile}/%{_module}.service $RPM_BUILD_ROOT%{_unitdir}/%{_module}.service

%files
%doc README.md

%config(noreplace) %{_sysconfdir}/systemdock/containers.d/%{_profile}/config.yml
%{_sysconfdir}/systemdock/containers.d/%{_profile}/%{_module}.service

%{_unitdir}/%{_module}.service

%changelog

