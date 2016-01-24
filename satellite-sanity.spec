%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:          satellite-sanity
Version:       REPLACE_ME_WITH_VERSION
Release:       1%{?dist}
Summary:       Red Hat Satellite health check
License:       GPLv3
Group:         Applications/Internet
URL:           https://github.com/SatelliteQE/satellite-sanity
Source0:       https://github.com/SatelliteQE/satellite-sanity/archive/%{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
BuildRequires: python
BuildRequires: python-devel
BuildRequires: python-setuptools
Requires:      python
Requires:      python-dateutil


%description
Red Hat Satellite health check tool


%prep
%setup -qc


%build
pushd %{name}-%{version}
%{__python} setup.py build
popd


%install
rm -rf %{buildroot}
pushd %{name}-%{version}
%{__python2} setup.py install --skip-build --root %{buildroot}
rm -f %{buildroot}%{python2_sitelib}/satellite_sanity/rules/example_fails.*
mkdir -p %{buildroot}%{_bindir}/
cp -p satellite-sanity %{buildroot}%{_bindir}/
popd


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python2_sitelib}/*egg-info
%{python2_sitelib}/satellite_sanity
%{_bindir}/satellite-sanity


%changelog
* Wed Dec 09 2015 Jan Hutar <jhutar@redhat.com> 0.1.1-1
- Let's try to build in COPR

* Wed Dec 09 2015 Jan Hutar <jhutar@redhat.com> 0.1-1
- Init
