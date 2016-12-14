%define         _module docker-airvideoserver-hd

%{!?svn_revision:%define svn_revision 1}

# COMPATIBILITY FIX: Jenkins job name is neccessary to make build root unique (for CentOS5 and earlier)
%{!?JOB_NAME:%define JOB_NAME standalone}

Name:           docker-airvideoserver-hd
Version:        2.2.3
Release:        %{svn_revision}%{?dist}
Summary:        Docker container wrapper for AirVideoServer HD

Group:          Multimedia/Servers
License:        Other/Proprietary
URL:            http://www.inmethod.com/airvideohd/index.html
Packager:       Roman Pavlyuk <roman.pavlyuk@gmail.com>
Source:         %{_module}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)-%{JOB_NAME}
BuildArch:      noarch

Requires:	docker

Conflicts:	airvideoserver-hd

%description
AirVideoServer HD Docker container control service for CentOS/Fedora Linux family

%prep
%setup -n %{_module}

%build
# Nothing to do

%install
# Create build directory
rm -rf "$RPM_BUILD_ROOT"
mkdir -p "$RPM_BUILD_ROOT"

mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/%{_module}/data
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/%{_module}/converted
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/%{_module}/logs

mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
cp -a src/*.service $RPM_BUILD_ROOT/%{_unitdir}

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{_module}
cp -a src/Server.properties $RPM_BUILD_ROOT/%{_sysconfdir}/%{_module}

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp -a src/docker-airvideoserver-hd $RPM_BUILD_ROOT/%{_bindir}/docker-airvideoserver-hd

%files
%doc

%config(noreplace) %{_sysconfdir}/%{_module}/Server.properties

%attr(0755,root,root) %{_bindir}/docker-airvideoserver-hd

%{_unitdir}/*.service

%attr(0777, -, -) %{_sharedstatedir}/%{_module}/data
%attr(0777, -, -) %{_sharedstatedir}/%{_module}/converted
%attr(0777, -, -) %{_sharedstatedir}/%{_module}/logs


