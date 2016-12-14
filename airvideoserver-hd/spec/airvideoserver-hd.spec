%global __os_install_post %{nil}

%define         _module airvideoserver-hd

%{!?svn_revision:%define svn_revision 1}

# COMPATIBILITY FIX: Jenkins job name is neccessary to make build root unique (for CentOS5 and earlier)
%{!?JOB_NAME:%define JOB_NAME standalone}

%global debug_package %{nil}

Name:		airvideoserver-hd
Version:	2.2.3
Release:	%{svn_revision}%{?dist}
Summary:	AirVideoServer HD

Group:		Multimedia/Servers
License:	Other/Proprietary
URL:		http://www.inmethod.com/airvideohd/index.html
Packager:       Roman Pavlyuk <roman.pavlyuk@gmail.com>
Source:         %{_module}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)-%{JOB_NAME}
#BuildArch:      noarch

%define         pkg_dist AirVideoServerHD-%{version}.tar.bz2
%define		pkg_user airvideo
%define		pkg_group %{pkg_user}

AutoReqProv: no

# BuildRequires:	

Requires(pre): shadow-utils

Requires:	vlc	

%description
AirVideoServer HD package for CentOS Linux

%prep
%setup -n %{_module}
pushd ./src
tar xfj %{pkg_dist}
popd

%build
# patch start script 
perl -pi -e 's|.*\.\/AirVideoServerHD.*|\%{_libexecdir}\/%{_module}\/AirVideoServerHD\ --config\=\%{_sysconfdir}\/%{_module}\/Server.properties|gi' src/start.sh

# patch the config file
perl -pi -e 's|.*logsPath.*|logsPath = \%{_localstatedir}\/log\/%{_module}|gi' src/Server.properties
perl -pi -e 's|.*applicationDataPath.*|applicationDataPath = \%{_sharedstatedir}\/%{_module}\/data|gi' src/Server.properties
perl -pi -e 's|.*conversionFolderPath.*|conversionFolderPath = \%{_sharedstatedir}\/%{_module}\/converted|gi' src/Server.properties

%ifarch x86_64
perl -pi -e 's|^VLCLibraryPath.*|VLCLibraryPath = \/usr\/lib64\/|gi' src/Server.properties
%endif

%install
# Create build directory
rm -rf "$RPM_BUILD_ROOT"
mkdir -p "$RPM_BUILD_ROOT"

mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/%{_module}
cp -a src/Resources $RPM_BUILD_ROOT%{_libexecdir}/%{_module}
cp -a src/AirVideoServerHD $RPM_BUILD_ROOT%{_libexecdir}/%{_module}

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp -a src/start.sh $RPM_BUILD_ROOT/%{_bindir}/airvideoserver-hd

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{_module}
cp -a src/Server.properties $RPM_BUILD_ROOT/%{_sysconfdir}/%{_module}

mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
cp -a src/*.service $RPM_BUILD_ROOT/%{_unitdir}

mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/%{_module}/data
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/%{_module}/converted
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/%{_module}/logs

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log
ln -s %{_sharedstatedir}/%{_module}/logs $RPM_BUILD_ROOT%{_localstatedir}/log/%{_module}

%files
%doc src/OpenSource.txt

%{_libexecdir}/%{_module}/Resources
%attr(0755,root,root) %{_libexecdir}/%{_module}/AirVideoServerHD
%attr(0755,root,root) %{_bindir}/airvideoserver-hd

%config(noreplace) %{_sysconfdir}/%{_module}/Server.properties

%{_unitdir}/*.service

%attr(0755,%{pkg_user},%{pkg_group}) %{_sharedstatedir}/%{_module}/data
%attr(0755,%{pkg_user},%{pkg_group}) %{_sharedstatedir}/%{_module}/converted

%attr(0755,%{pkg_user},%{pkg_group}) %{_sharedstatedir}/%{_module}/logs
%attr(0755,%{pkg_user},%{pkg_group}) %{_localstatedir}/log/%{_module}

%pre
getent group %{pkg_group} >/dev/null || groupadd -r %{pkg_group}
getent passwd %{pkg_user} >/dev/null || \
    useradd -r -g %{pkg_group} -d %{_sharedstatedir}/%{_module} -s /sbin/nologin \
    -c "AirVideoServer HD account" %{pkg_user}
exit 0

%changelog

