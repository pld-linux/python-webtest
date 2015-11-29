#
# TODO
# - python3 tests broken

# Conditional build:
%bcond_without	python3	# CPython 3.x module
%bcond_without	tests	# do not perform "make test"

%define 	module	webtest
Summary:	Helper to test WSGI applications
Name:		python-%{module}
Version:	1.3.4
Release:	5
License:	MIT
Group:		Libraries/Python
URL:		http://pythonpaste.org/webtest/
BuildRequires:	rpmbuild(macros) >= 1.710
Source0:	http://pypi.python.org/packages/source/W/WebTest/WebTest-%{version}.tar.gz
# Source0-md5:	be4b448e91306f297e6e302c3ebe9540
BuildRequires:	python-WebOb
BuildRequires:	python-dtopt
BuildRequires:	python-nose
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
%if %{with python3}
BuildRequires:	python3-WebOb
BuildRequires:	python3-devel
BuildRequires:	python3-dtopt
BuildRequires:	python3-modules
BuildRequires:	python3-nose
BuildRequires:	python3-setuptools
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WebTest wraps any WSGI application and makes it easy to send test
requests to that application, without starting up an HTTP server.

This provides convenient full-stack testing of applications written
with any WSGI-compatible framework.

%package -n python3-webtest
Summary:	Helper to test WSGI applications
Group:		Libraries/Python

%description -n python3-webtest
WebTest wraps any WSGI application and makes it easy to send test
requests to that application, without starting up an HTTP server.

This provides convenient full-stack testing of applications written
with any WSGI-compatible framework.

%prep
%setup -q -n WebTest-%{version}

# Remove bundled egg info if it exists.
rm -r *.egg-info

%build
%py_build

%if %{with python3}
%py3_build
%endif

%if %{with tests}
PYTHONPATH=build-2/lib %{__python} setup.py test

%if %{with python3}
#PYTHONPATH=build-3/lib %{__python3} setup.py test
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python3}
%py3_install
%endif

%py_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/WebTest-%{version}-py*.egg-info

%if %{with python3}
%files -n python3-webtest
%defattr(644,root,root,755)
%doc docs/*
%{py3_sitescriptdir}/WebTest-%{version}-py*.egg-info
%dir %{py3_sitescriptdir}/webtest
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/__pycache__
%endif
