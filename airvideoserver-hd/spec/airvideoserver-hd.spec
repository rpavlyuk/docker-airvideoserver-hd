%define         _module airvideoserver-hd

%{!?svn_revision:%define svn_revision 1}

# COMPATIBILITY FIX: Jenkins job name is neccessary to make build root unique (for CentOS5 and earlier)
%{!?JOB_NAME:%define JOB_NAME standalone}

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
BuildArch:      noarch

# BuildRequires:	

Requires:	vlc	

%description
AirVideoServer HD package for CentOS Linux

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
%make_install


%files
%doc



%changelog

