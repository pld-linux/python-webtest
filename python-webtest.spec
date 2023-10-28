#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	webtest
Summary:	Helper to test WSGI applications
Summary(pl.UTF-8):	Moduł pomocniczy do testowania aplikacji WSGI
Name:		python-%{module}
# keep 2.x here for python2 support
Version:	2.0.35
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/webtest/
Source0:	https://files.pythonhosted.org/packages/source/W/WebTest/WebTest-%{version}.tar.gz
# Source0-md5:	a5d027ffa0991fdf20e305c62bd37791
Patch0:		%{name}-deps.patch
URL:		http://webtest.pythonpaste.org/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PasteDeploy
BuildRequires:	python-WSGIProxy2
BuildRequires:	python-WebOb >= 1.2
BuildRequires:	python-bs4
BuildRequires:	python-dtopt
BuildRequires:	python-lxml
BuildRequires:	python-mock
BuildRequires:	python-nose
BuildRequires:	python-pyquery
BuildRequires:	python-six
BuildRequires:	python-waitress >= 0.8.5
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PasteDeploy
BuildRequires:	python3-WSGIProxy2
BuildRequires:	python3-WebOb >= 1.2
BuildRequires:	python3-bs4
BuildRequires:	python3-dtopt
BuildRequires:	python3-nose >= 1.3.1
BuildRequires:	python3-pyquery
BuildRequires:	python3-six
BuildRequires:	python3-waitress >= 0.8.5
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-docutils
BuildRequires:	python-pylons-sphinx-themes >= 1.0.8
BuildRequires:	sphinx-pdg-2 >= 1.8.1
%endif
Requires:	python-modules >= 1:2.7
Obsoletes:	python-WebTest < 1.4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WebTest wraps any WSGI application and makes it easy to send test
requests to that application, without starting up an HTTP server.

This provides convenient full-stack testing of applications written
with any WSGI-compatible framework.

%description -l pl.UTF-8
WebTest obudowuje dowolną aplikację WSGI i ułatwia wysyłanie do niej
testowych żądań bez uruchamiania serwera HTTP.

Daje to wygodne, oparte o pełny stos testowanie aplikacji napisanych
przy użyciu dowolnego szkieletu zgodnego z WSGI.

%package -n python3-webtest
Summary:	Helper to test WSGI applications
Summary(pl.UTF-8):	Moduł pomocniczy do testowania aplikacji WSGI
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-webtest
WebTest wraps any WSGI application and makes it easy to send test
requests to that application, without starting up an HTTP server.

This provides convenient full-stack testing of applications written
with any WSGI-compatible framework.

%description -n python3-webtest -l pl.UTF-8
WebTest obudowuje dowolną aplikację WSGI i ułatwia wysyłanie do niej
testowych żądań bez uruchamiania serwera HTTP.

Daje to wygodne, oparte o pełny stos testowanie aplikacji napisanych
przy użyciu dowolnego szkieletu zgodnego z WSGI.

%package apidocs
Summary:	API documentation for Python WebTest module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona WebTest
Group:		Documentation

%description apidocs
API documentation for Python WebTest module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona WebTest.

%prep
%setup -q -n WebTest-%{version}
%patch0 -p1

# Remove bundled egg info
%{__rm} -r *.egg-info

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst license.rst
%{py_sitescriptdir}/webtest
%{py_sitescriptdir}/WebTest-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-webtest
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst license.rst
%{py3_sitescriptdir}/webtest
%{py3_sitescriptdir}/WebTest-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
