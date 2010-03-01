###### Predefinitions #####
%define name		corsixth
%define oname		CorsixTH
%define revision	493
%define version		0.1
%define release		%mkrel 0.svn%{revision}.1

##### Header #####
Summary:	Open source clone of Theme Hospital
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}-svn%{revision}.tar.lzma
Source1:	config.txt
Source2:	%{oname}-16.png
Source3:	%{oname}-32.png
Source4:	%{oname}-64.png
License:	MIT
Group:		Games/Strategy
URL:		http://code.google.com/p/corsix-th/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

BuildRequires:	cmake 
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	lua-devel
Requires:	SDL lua

# use this until SDL_mixer is fixed for correct provides... # Supp
%ifarch x86_64
Requires:	lib64SDL_mixer1.2_0
%else
Requires:	libSDL_mixer1.2_0
%endif

##### Description #####
%description
This project aims to reimplement the game engine of Theme Hospital, and 
be able to load the original game data files. This means that you will 
need a purchased copy of Theme Hospital, or a copy of the demo, in order 
to use CorsixTH. Put those files found in directory which contains a file 
called HOSPITAL.EXE, sub-directories called DATA, LEVELS, and QDATA, and so 
on under /usr/share/games/CorsixTH/th-files directory. After most of the 
original engine has been reimplemented in open source code, the project will 
serve as a base from which extensions to the original game can be made just 
like OpenTTD. 

!! Please be aware that this is BETA release so many features are still missing 
or WIP. Game configuration can be adjusted by changing values in 
/usr/share/games/CorsixTH/config.txt file !! 

##### setup, build, install #####
%prep
%setup -q -c
cp %{SOURCE1} %{oname}/

%build
%cmake .. -DCMAKE_INSTALL_PREFIX=%{_gamesdatadir}
%make

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}

mkdir %{buildroot}/%{_gamesbindir}
mv %{buildroot}/%{_gamesdatadir}/%{oname}/%{oname} %{buildroot}/%{_gamesbindir}/
mkdir %{buildroot}/%{_gamesdatadir}/%{oname}/th-files/

mkdir -p %{buildroot}/%{_iconsdir}/hicolor/{16x16,32x32,64x64,scalable}/apps
install -m 644 %{SOURCE2} %buildroot%_iconsdir/hicolor/16x16/apps/%{oname}.png
install -m 644 %{SOURCE3} %buildroot%_iconsdir/hicolor/32x32/apps/%{oname}.png
install -m 644 %{SOURCE4} %buildroot%_iconsdir/hicolor/64x64/apps/%{oname}.png

mkdir -p %{buildroot}/%{_datadir}/applications
cat > %{buildroot}/%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=CorsixTH
Comment=Open source clone of Theme Hospital game
Exec=%{_gamesbindir}/%{oname}
Path=%{_gamesdatadir}/%{oname}
Icon=%{oname}
Terminal=false
Type=Application
Categories=Game;StrategyGame;
EOF

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%endif

##### Files #####
%files
%defattr(-,root,root)
%{_gamesbindir}/%{oname}
%dir %{_gamesdatadir}/%{oname}
%{_gamesdatadir}/%{oname}/*
%_iconsdir/hicolor/*/apps/%{oname}.*
%{_datadir}/applications/mandriva-%{name}.desktop

