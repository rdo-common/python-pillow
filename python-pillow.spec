%global py2_incdir %{_includedir}/python%{python_version}
%global py3_incdir %{_includedir}/python%{python3_version}

%global name3 python3-pillow

# RHEL-7 doesn't have python 3
%if 0%{?rhel} == 7
  %global with_python3 0
%else
  %global with_python3 1
%endif

# Refer to the comment for Source0 below on how to obtain the source tarball
# The saved file has format python-imaging-Pillow-$version-$ahead-g$shortcommit.tar.gz
%global commit d1c6db88d4dee462c6bbf4e22555e3ddd410d06a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global ahead 105

# If ahead is 0, the tarball corresponds to a release version, otherwise to a git snapshot
%if %{ahead} > 0
%global snap .git%{shortcommit}
%endif

Name:           python-pillow
Version:        2.0.0
Release:        10%{?snap}%{?dist}
Summary:        Python image processing library

# License: see http://www.pythonware.com/products/pil/license.htm
License:        MIT
URL:            http://python-imaging.github.com/Pillow/

# Obtain the tarball for a certain commit via:
#  wget --content-disposition https://github.com/python-imaging/Pillow/tarball/$commit
Source0:        https://github.com/python-imaging/Pillow/tarball/%{commit}/python-imaging-Pillow-%{version}-%{ahead}-g%{shortcommit}.tar.gz

# Add s390* and ppc* archs
Patch0:         python-pillow-archs.patch
# Fix test hardcoded for little-endian
Patch1:         python-pillow_endian.patch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  tkinter
BuildRequires:  tk-devel
BuildRequires:  python-sphinx
BuildRequires:  libjpeg-devel
BuildRequires:  zlib-devel
BuildRequires:  freetype-devel
BuildRequires:  lcms-devel
BuildRequires:  sane-backends-devel
# Don't build with webp support on s390* archs
# see bug #962091
%ifnarch s390 s390x
BuildRequires:  libwebp-devel
%endif
BuildRequires:  PyQt4
BuildRequires:  numpy

%if %{with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-tkinter
BuildRequires:  python3-PyQt4
BuildRequires:  python3-numpy
%endif

Provides:       python-imaging = %{version}-%{release}
Obsoletes:      python-imaging <= 1.1.7-12

%if %{with_python3}
Provides:       python3-imaging = %{version}-%{release}
%endif

%filter_provides_in %{python_sitearch}
%filter_provides_in %{python3_sitearch}
%filter_setup

%description
Python image processing library, fork of the Python Imaging Library (PIL)

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

There are five subpackages: tk (tk interface), qt (PIL image wrapper for Qt),
sane (scanning devices interface), devel (development) and doc (documentation).


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python-devel, libjpeg-devel, zlib-devel
Provides:       python-imaging-devel = %{version}-%{release}
Obsoletes:      python-imaging-devel <= 1.1.7-12

%description devel
Development files for %{name}.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}.


%package sane
Summary:        Python module for using scanners
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       python-imaging-sane = %{version}-%{release}
Obsoletes:      python-imaging-sane <= 1.1.7-12

%description sane
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.


%package tk
Summary:        Tk interface for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       tkinter
Provides:       python-imaging-tk = %{version}-%{release}
Obsoletes:      python-imaging-tk <= 1.1.7-12

%description tk
Tk interface for %{name}.

%package qt
Summary:        PIL image wrapper for Qt
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       PyQt4
Provides:       python-imaging-qt = %{version}-%{release}

%description qt
PIL image wrapper for Qt.


%if %{with_python3}
%package -n %{name3}
Summary:        Python 3 image processing library

%description -n %{name3}
%{_description}


%package -n %{name3}-devel
Summary:        Development files for %{name3}
Group:          Development/Libraries
Requires:       %{name3}%{?_isa} = %{version}-%{release}
Requires:       python3-devel, libjpeg-devel, zlib-devel

%description -n %{name3}-devel
Development files for %{name3}.


%package -n %{name3}-doc
Summary:        Documentation for %{name3}
Group:          Documentation
Requires:       %{name3} = %{version}-%{release}
BuildArch:      noarch

%description -n %{name3}-doc
Documentation for %{name3}.


%package -n %{name3}-sane
Summary:        Python module for using scanners
Group:          System Environment/Libraries
Requires:       %{name3}%{?_isa} = %{version}-%{release}

%description -n %{name3}-sane
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.


%package -n %{name3}-tk
Summary:        Tk interface for %{name3}
Group:          System Environment/Libraries
Requires:       %{name3}%{?_isa} = %{version}-%{release}
Requires:       tkinter

%description -n %{name3}-tk
Tk interface for %{name3}.

%package -n %{name3}-qt
Summary:        PIL image wrapper for Qt
Group:          System Environment/Libraries
Obsoletes:      %{name3} <= 2.0.0-5.git93a488e8
Requires:       %{name3}%{?_isa} = %{version}-%{release}
Requires:       python3-PyQt4

%description -n %{name3}-qt
PIL image wrapper for Qt.

%endif


%prep
%setup -q -n python-imaging-Pillow-%{shortcommit}
%patch0 -p1 -b .archs
%patch1 -p1 -b .endian

%if %{with_python3}
# Create Python 3 source tree
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
# Build Python 2 modules
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

pushd Sane
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
popd

pushd docs
PYTHONPATH=$PWD/.. make html
rm -f _build/html/.buildinfo
popd

%if %{with_python3}
# Build Python 3 modules
pushd %{py3dir}
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python3}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

pushd Sane
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd

pushd docs
PYTHONPATH=$PWD/.. make html
rm -f _build/html/.buildinfo
popd
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT

# Install Python 2 modules
install -d $RPM_BUILD_ROOT/%{py2_incdir}/Imaging
install -m 644 libImaging/*.h $RPM_BUILD_ROOT/%{py2_incdir}/Imaging
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
pushd Sane
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd

%if %{with_python3}
# Install Python 3 modules
pushd %{py3dir}
install -d $RPM_BUILD_ROOT/%{py3_incdir}/Imaging
install -m 644 libImaging/*.h $RPM_BUILD_ROOT/%{py3_incdir}/Imaging
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
pushd Sane
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
popd
%endif

# The scripts are packaged in %%doc
rm -rf $RPM_BUILD_ROOT%{_bindir}


%check
# Check Python 2 modules
ln -s $PWD/Images $RPM_BUILD_ROOT%{python_sitearch}/Images
ln -s $PWD/Tests $RPM_BUILD_ROOT%{python_sitearch}/Tests
ln -s $PWD/selftest.py $RPM_BUILD_ROOT%{python_sitearch}/selftest.py
pushd $RPM_BUILD_ROOT%{python_sitearch}
%{__python} selftest.py
%{__python} Tests/run.py
popd
rm $RPM_BUILD_ROOT%{python_sitearch}/Images
rm $RPM_BUILD_ROOT%{python_sitearch}/Tests
rm $RPM_BUILD_ROOT%{python_sitearch}/selftest.py*

%if %{with_python3}
# Check Python 3 modules
pushd %{py3dir}
ln -s $PWD/Images $RPM_BUILD_ROOT%{python3_sitearch}/Images
ln -s $PWD/Tests $RPM_BUILD_ROOT%{python3_sitearch}/Tests
ln -s $PWD/selftest.py $RPM_BUILD_ROOT%{python3_sitearch}/selftest.py
pushd $RPM_BUILD_ROOT%{python3_sitearch}
%{__python3} selftest.py
%{__python3} Tests/run.py
popd
rm $RPM_BUILD_ROOT%{python3_sitearch}/Images
rm $RPM_BUILD_ROOT%{python3_sitearch}/Tests
rm $RPM_BUILD_ROOT%{python3_sitearch}/selftest.py*
popd
%endif


%files
%doc README.rst docs/HISTORY.txt COPYING
%{python_sitearch}/*
# These are in subpackages
%exclude %{python_sitearch}/*sane*
%exclude %{python_sitearch}/_imagingtk*
%exclude %{python_sitearch}/PIL/ImageTk*
%exclude %{python_sitearch}/PIL/SpiderImagePlugin*
%exclude %{python_sitearch}/PIL/ImageQt*

%files devel
%{py2_incdir}/Imaging/

%files doc
%doc Scripts Images docs/_build/html

%files sane
%doc Sane/CHANGES Sane/demo*.py Sane/sanedoc.txt
%{python_sitearch}/*sane*

%files tk
%{python_sitearch}/_imagingtk*
%{python_sitearch}/PIL/ImageTk*
%{python_sitearch}/PIL/SpiderImagePlugin*

%files qt
%{python_sitearch}/PIL/ImageQt*

%if %{with_python3}
%files -n %{name3}
%doc README.rst docs/HISTORY.txt COPYING
%{python3_sitearch}/*
# These are in subpackages
%exclude %{python3_sitearch}/*sane*
%exclude %{python3_sitearch}/_imagingtk*
%exclude %{python3_sitearch}/PIL/ImageTk*
%exclude %{python3_sitearch}/PIL/SpiderImagePlugin*
%exclude %{python3_sitearch}/PIL/ImageQt*

%files -n %{name3}-devel
%{py3_incdir}/Imaging/

%files -n %{name3}-doc
%doc Scripts Images docs/_build/html

%files -n %{name3}-sane
%doc Sane/CHANGES Sane/demo*.py Sane/sanedoc.txt
%{python3_sitearch}/*sane*

%files -n %{name3}-tk
%{python3_sitearch}/_imagingtk*
%{python3_sitearch}/PIL/ImageTk*
%{python3_sitearch}/PIL/SpiderImagePlugin*

%files -n %{name3}-qt
%{python3_sitearch}/PIL/ImageQt*

%endif

%changelog
* Mon May 13 2013 Roman Rakus <rrakus@redhat.com> - 2.0.0-10
- Build without webp support on s390* archs
  Resolves: rhbz#962059

* Sat May 11 2013 Roman Rakus <rrakus@redhat.com> - 2.0.0-9.gitd1c6db8
- Conditionaly disable build of python3 parts on RHEL system

* Wed May 08 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-8.gitd1c6db8
- Add patch to fix test failure on big-endian

* Thu Apr 25 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.0-7.gitd1c6db8
- Remove Obsoletes in the python-pillow-qt subpackage. Obsoletes isn't
  appropriate since qt support didn't exist in the previous python-pillow
  package so there's no reason to drag in python-pillow-qt when updating
  python-pillow.

* Fri Apr 19 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-6.gitd1c6db8
- Update to latest git
- python-pillow_quantization.patch now upstream
- python-pillow_endianness.patch now upstream
- Add subpackage for ImageQt module, with correct dependencies
- Add PyQt4 and numpy BR (for generating docs / running tests)

* Mon Apr 08 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-5.git93a488e
- Reenable tests on bigendian, add patches for #928927

* Sun Apr 07 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-4.git93a488e
- Update to latest git
- disable tests on bigendian (PPC*, S390*) until rhbz#928927 is fixed

* Fri Mar 22 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-3.gitde210a2
- python-pillow_tempfile.patch now upstream
- Add python3-imaging provides (bug #924867)

* Fri Mar 22 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-2.git2e88848
- Update to latest git
- Remove python-pillow-disable-test.patch, gcc is now fixed
- Add python-pillow_tempfile.patch to prevent a temporary file from getting packaged

* Tue Mar 19 2013 Sandro Mani <manisandro@gmail.com> - 2.0.0-1.git2f4207c
- Update to 2.0.0 git snapshot
- Enable python3 packages
- Add libwebp-devel BR for Pillow 2.0.0

* Wed Mar 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.8-6.20130305git
- Add ARM support

* Tue Mar 12 2013 Karsten Hopp <karsten@redhat.com> 1.7.8-5.20130305git
- add s390* and ppc* to arch detection

* Tue Mar 05 2013 Sandro Mani <manisandro@gmail.com> - 1.7.8-4.20130305git7866759
- Update to latest git snapshot
- 0001-Cast-hash-table-values-to-unsigned-long.patch now upstream
- Pillow-1.7.8-selftest.patch now upstream

* Mon Feb 25 2013 Sandro Mani <manisandro@gmail.com> - 1.7.8-3.20130210gite09ff61
- Really remove -fno-strict-aliasing
- Place comment on how to retreive source just above the Source0 line

* Mon Feb 18 2013 Sandro Mani <manisandro@gmail.com> - 1.7.8-2.20130210gite09ff61
- Rebuild without -fno-strict-aliasing
- Add patch for upstream issue #52

* Sun Feb 10 2013 Sandro Mani <manisandro@gmail.com> - 1.7.8-1.20130210gite09ff61
- Initial RPM package
