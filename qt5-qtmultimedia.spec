
%global qt_module qtmultimedia

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
# only primary archs (for now), allow secondary to bootstrap
# global bootstrap 1

%if ! 0%{?bootstrap}
%ifarch %{arm} %{ix86} x86_64
%define docs 1
%endif
%endif

%if 0%{?fedora}
%global openal 1
%endif

%global gst 0.10
%if 0%{?fedora} > 20
%global gst 1.0
%endif

Summary: Qt5 - Multimedia support
Name:    qt5-%{qt_module}
Version: 5.6.2
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: http://download.qt.io/official_releases/qt/5.6/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

BuildRequires: cmake
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtdeclarative-devel >= %{version}
BuildRequires: pkgconfig(alsa)
%if "%{?gst}" == "0.10"
BuildRequires: pkgconfig(gstreamer-interfaces-0.10)
%endif
BuildRequires: pkgconfig(gstreamer-%{gst})
BuildRequires: pkgconfig(gstreamer-app-%{gst})
BuildRequires: pkgconfig(gstreamer-audio-%{gst})
BuildRequires: pkgconfig(gstreamer-base-%{gst})
BuildRequires: pkgconfig(gstreamer-pbutils-%{gst})
BuildRequires: pkgconfig(gstreamer-plugins-bad-%{gst})
BuildRequires: pkgconfig(gstreamer-video-%{gst})
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
%if 0%{?openal}
BuildRequires: pkgconfig(openal)
%endif
BuildRequires: pkgconfig(xv)

BuildRequires: qt5-qtbase-private-devel

%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

%description
The Qt Multimedia module provides a rich feature set that enables you to
easily take advantage of a platforms multimedia capabilites and hardware.
This ranges from the playback and recording of audio and video content to
the use of available devices like cameras and radios.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Requires: qt5-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
License: GFDL
Requires: %{name} = %{version}-%{release}
BuildRequires: qt5-qdoc
BuildRequires: qt5-qhelpgenerator
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} .. \
  CONFIG+=git_build \
  GST_VERSION=%{gst}

make %{?_smp_mflags}

%if 0%{?docs}
make %{?_smp_mflags} docs
%endif
popd


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LGPL_EXCEPTION.txt LICENSE.LGPL*
%{_qt5_libdir}/libQt5Multimedia.so.5*
%{_qt5_libdir}/libQt5MultimediaQuick_p.so.5*
%{_qt5_libdir}/libQt5MultimediaWidgets.so.5*
%{_qt5_libdir}/libqgsttools_p.so.1*
%if 0%{?openal}
%{_qt5_archdatadir}/qml/QtAudioEngine/
%endif
%{_qt5_archdatadir}/qml/QtMultimedia/
%{_qt5_plugindir}/audio/
%{_qt5_plugindir}/mediaservice/
%{_qt5_plugindir}/playlistformats/
%dir %{_qt5_libdir}/cmake/Qt5Multimedia/
%{_qt5_libdir}/cmake/Qt5Multimedia/Qt5Multimedia_*Plugin.cmake
%dir %{_qt5_libdir}/cmake/Qt5MultimediaWidgets/

%files devel
%{_qt5_headerdir}/QtMultimedia/
%{_qt5_headerdir}/QtMultimediaQuick_p/
%{_qt5_headerdir}/QtMultimediaWidgets/
%{_qt5_libdir}/libQt5Multimedia.so
%{_qt5_libdir}/libQt5Multimedia.prl
%{_qt5_libdir}/libQt5MultimediaQuick_p.so
%{_qt5_libdir}/libQt5MultimediaQuick_p.prl
%{_qt5_libdir}/libQt5MultimediaWidgets.so
%{_qt5_libdir}/libQt5MultimediaWidgets.prl
%{_qt5_libdir}/libqgsttools_p.so
%{_qt5_libdir}/libqgsttools_p.prl
%{_qt5_libdir}/cmake/Qt5Multimedia/Qt5MultimediaConfig*.cmake
%{_qt5_libdir}/cmake/Qt5MultimediaWidgets/Qt5MultimediaWidgetsConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Multimedia.pc
%{_qt5_libdir}/pkgconfig/Qt5MultimediaWidgets.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%if 0%{?docs}
%files doc
%license LICENSE.FDL
%{_qt5_docdir}/qtmultimedia.qch
%{_qt5_docdir}/qtmultimedia/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Wed Jan 11 2017 Jan Grulich <jgrulich@redhat.com> - 5.6.2-1
- Update to 5.6.2
  Resolves: bz#1384823

* Tue Aug 30 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.1-10
- Increase build version to have newer version than in EPEL
  Resolves: bz#1317406

* Wed Jun 08 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.1-1
- Update to 5.6.1
  Resolves: bz#1317406

* Wed Apr 13 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.0-5
- Enable documentation
  Resolves: bz#1317406

* Thu Apr 07 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.0-4
- Initial version for RHEL
  Resolves: bz#1317406

* Sun Mar 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-3
- rebuild

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-2
- rebuild

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-1
- 5.6.0 final release

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.8.rc
- Update to final RC

* Mon Feb 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.7
- Update RC release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.6.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.5.beta
- update source URL, use %%license, BR: cmake

* Mon Dec 21 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.4
- Update to final beta release

* Fri Dec 11 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-0.3
- include BR: qt5-qdoc only in -doc subpkg
- restore bootstrap macro support
- make openal support unconditional (#1069231)

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.2
- Official beta release

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 beta

* Mon Oct 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-4
- pull in upstream fixes, QTBUG-48939 in particular

* Thu Oct 22 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-3
- drop gst support on el6 (QTBUG-48939)

* Thu Oct 15 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-2
- Update to final release 5.5.1

* Tue Sep 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-1
- Update to Qt 5.5.1 RC1

* Wed Jul 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-3
- -docs: BuildRequires: qt5-qhelpgenerator, standardize bootstrapping

* Thu Jul 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-2
- tighten qtbase dep (#1233829)

* Wed Jul 1 2015 Helio Chissini de Castro <helio@kde.org> 5.5.0-1
- New final upstream release Qt 5.5.0

* Wed Jun 24 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-1
- 5.4.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-2
- rebuild (gcc5)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Thu Dec 11 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final) + backported gst1 support from dev/ branch

* Tue Nov 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.20141118.gst1
- wip/gstreamer1 snapshot (#1149885)

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.beta
- out-of-tree build, use %%qmake_qt5

* Sun Oct 19 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta

* Wed Sep 17 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.3.2-1
- 5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-1.1
- rebuild (for pulseaudio, bug #1117683)

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Mon May 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- use standard (same as qtbase) .prl sanitation

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- build -examples only if supported

* Sun Jan 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- -examples subpkg

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Sun Nov 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- bootstrap ppc

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg

* Sat Sep 07 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- ExclusiveArch: %%{ix86} x86_64 %%{arm} (to match qt5-qtdeclarative)

* Thu Aug 29 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-3
- update Source URL (and refetch tarball)
- improved summary/description

* Thu May 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- BR: qt5-qtdeclarative-devel

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

