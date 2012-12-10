%define oname CorsixTH

Summary:	Open source clone of Theme Hospital
Name:		corsixth
Version:	0.11
Release:	1
License:	MIT
Group:		Games/Strategy
URL:		http://code.google.com/p/corsix-th/
Source0:	http://corsix-th.googlecode.com/files/%{oname}-%{version}-Source.tar.gz
BuildRequires:	cmake
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	lua5.1-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	icoutils
Requires:	TiMidity++

%description
This project aims to reimplement the game engine of Theme Hospital, and 
be able to load the original game data files. This means that you will 
need a purchased copy of Theme Hospital in order to enjoy CorsixTH. 

%prep
%setup -q -n %{oname}-%{version}-Source

%build
%cmake -DCMAKE_INSTALL_PREFIX=%{_gamesdatadir}/
%make

%install
%makeinstall_std -C build

mkdir %{buildroot}%{_gamesbindir}
cat > %{buildroot}%{_gamesbindir}/%{oname} << EOF
#!/bin/bash
%{_gamesdatadir}/%{oname}/%{oname}
EOF

mkdir -p %{buildroot}%{_gamesdatadir}/%{oname}/th-files/

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{32x32,128x128}/apps

icotool -x %{oname}/%{oname}.ico
mv %{oname}*32x32*.png %{oname}.png
install -m 644 %{oname}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{oname}.png
mv %{oname}*128x128*.png %{oname}.png
install -m 644 %{oname}.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{oname}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=CorsixTH
Comment=Open source clone of Theme Hospital game
Exec=%{oname}
Path=%{_gamesdatadir}/%{oname}
Icon=%{oname}
Terminal=false
Type=Application
Categories=Game;StrategyGame;
EOF

%files
%attr(755, root, root) %{_gamesbindir}/%{oname}
%dir %{_gamesdatadir}/%{oname}
%{_gamesdatadir}/%{oname}/*
%{_iconsdir}/hicolor/*/apps/%{oname}.*
%{_datadir}/applications/%{name}.desktop

