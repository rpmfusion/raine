Name:           raine
Version:        0.50.11
Release:        7%{?dist}
Summary:        Arcade emulator focused on Taito and Jaleco games hardware
Group:          Applications/Emulators
License:        GPL+ and Distributable
URL:            http://www.rainemu.com
Source0:        http://www.rainemu.com/html/archive/raines-%{version}.tar.bz2
Source1:        %{name}.desktop
Patch0:         %{name}-0.50.11-makefile.patch
Patch1:         %{name}-0.50.3-fixdatadirloc.patch
Patch2:         %{name}-0.50.3-fixcustomcursor.patch
Patch3:         %{name}-0.50.11-incdirfix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  desktop-file-utils
BuildRequires:  libpng-devel
BuildRequires:  nasm
BuildRequires:  SDL_image-devel
BuildRequires:  SDL_ttf-devel
BuildRequires:  zlib-devel
Requires:       hicolor-icon-theme
# Only compiles on x86 due to extensive x86 assembly.
# There should be a {ix86} instead of i386 in the ExclusiveArch line but
# that would make plague build the package for athlon, i386, i586 and i686 :-/
%if 0%{?fedora} >= 11
ExclusiveArch:  i586
%else
ExclusiveArch:  i386
%endif


%description
Raine emulates some M68000, M68020, Z80 and M68705 arcade games and is mainly
focused on Taito and Jaleco games hardware. Raine can emulate many nice games
now, including new additions from Cave and other companies.


%prep
%setup -qn %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# Fix encoding
iconv -f iso8859-1 debian/changelog -t utf8 > changelog

# Fix permissions for debuginfo RPM
chmod -x */*.c \
         */*.cpp \
         */*.h \
         */*/*.c \
         */*/*.h \
         */*/*.cpp \
         */*/*/*.c \
         */*/*/*.h \
         */*/*/*.cpp


%build
make %{?_smp_mflags} RPMFLAGS="%{optflags} -fno-strict-aliasing"


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -pm0644 %{name}.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps

desktop-file-install --vendor dribble \
                     --dir %{buildroot}%{_datadir}/applications \
                     %{SOURCE1}


%clean
rm -rf %{buildroot}


%post
# Set SELinux type (requires executable stack & data segment)
semanage fcontext -a -t unconfined_execmem_exec_t '%{_bindir}/%{name}' 2>/dev/null || :
restorecon '%{_bindir}/%{name}' 2>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
# Undo SELinux changes on removal
if [ $1 -eq 0 ]; then
    semanage fcontext -d -t unconfined_execmem_exec_t '%{_bindir}/%{name}' 2>/dev/null || :
fi
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%doc changelog


%changelog
* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.50.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Julian Sikorski <belegdol@fedoraproject.org> - 0.50.11-6
- Fedora 11 is i586, not i386

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.50.11-5
- rebuild for new F11 features

* Sat Oct 25 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.50.11-4
- use i386 instead of ix86 for ExcludeArch

* Tue Oct 07 2008 Xavier Lamien <lxtnow[at]gmail.com> - 0.50.11-3
- Update patch against new release.

* Sun Sep 14 2008 Xavier Lamien <lxtnow[at]gmail.com> - 0.50.11-2
- Update files and rebuild for RPM fusion.

* Tue Mar 25 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.50.11-1
- Upgrade to 0.50.11
- Dropped changes/* and now include the general changelog
- Added patch to include assembler dirs, otherwise compilation fails

* Tue Jan 08 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.50.6-1
- Upgrade to 0.50.6
- Updated selinux %%post/%%postun entries

* Sat Jul 07 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.50.5-1
- Upgrade to 0.50.5
- Minor spec changes due to new guidelines
- Dropped explicit support for Fedora Core 5

* Sun May 06 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.50.4-1
- Upgrade to 0.50.4

* Sat Mar 17 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.50.3-2
- Changed .desktop category to Game;Emulator;
- "Fixed" encoding on changes-antiriad.txt

* Sun Feb 25 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.50.3-1
- Upgrade to 0.50.3
- Updated all patches for new version
- Added patch for building with older SDL supplied with FC5
- Dropped allegro-devel buildrequire. Now only uses SDL
- Added patch to fix loading of the custom cursor

* Mon Oct 23 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.43.4-4
- Drop svgalib support (Dribble BZ #45)

* Sat Oct 21 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.43.4-3
- Fix source permissions for debuginfo rpm

* Wed Oct 18 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.43.4-2
- Dropped zlib-devel buildrequire, implied by libpng-devel
- Added hicolor-icon-theme require
- Swapped excludearch tags for exclusivearch tags
- Added SELinux context changes due to executable stack & data segment

* Fri Oct 06 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.43.4-1
- Initial Release
