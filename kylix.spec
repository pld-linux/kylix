# TODO:
# - more subpackages: -bcb -delphi -bcb-ide -delphi-ide -doc
Summary:	Kylix 3 Open Edition
Summary(pl.UTF-8):	Kylix 3 - Wydanie otwarte
Name:		kylix
Version:	3
Release:	0.3
License:	non-distributable
Group:		X11/Development/Tools
Source0:	ftp://ftpd.borland.com/download/kylix/k3/%{name}%{version}_open.tar.gz
# NoSource0-md5:	83124b00249754ef0ff02569345fc5ae
Source1:	%{name}%{version}_open.response
Source2:	%{name}%{version}_open.wrapper
Source3:	%{name}%{version}_open.dro
Source4:	%{name}path
Patch0:		%{name}3_open-setup.patch
NoSource:	0
URL:		http://www.borland.com/kylix/open/
BuildRequires:	sed >= 4.0
BuildRequires:	symlinks
#BuildRequires:	compat-libstdc++-2.9
Requires:	%{name}-libs = %{version}-%{release}
Provides:	libbortoken.so.6.9
Provides:	libdcc.so.6.9
Provides:	libilinkintf.so.6.9
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/kylix
%define		_libexecdir	%{_libdir}/kylix
%define		_includedir	%{_prefix}/include/kylix
%define		_datadir	%{_prefix}/share/kylix

%description
Borland Kylix 3 Enterprise delivers an integrated C++ and Delphi
language solution for developing database, GUI, and Web applications
for Linux which are cross-platform ready for Windows.

%description -l pl.UTF-8
Borland Kylix 3 Enterprise dostarcza zintegrowane środowisko dla
języków C++ i Delphi do tworzenia aplikacji bazodanowych, graficznych
i WWW dla Linuksa, gotowych do przeniesienia na Windows.

%package libs
Summary:	Kylix libraries
Summary(pl.UTF-8):	Biblioteki Kyliksa
# not redistributable due packaged bplrtl.so
#License:	redistributable
Group:		Development/Libraries
Provides:	libborunwind.so

%description libs
Kylix libraries.

%description libs -l pl.UTF-8
Biblioteki Kyliksa.

%prep
%setup -q -n %{name}%{version}_open
%patch -P0 -p1

install -D %{SOURCE4} bin/kylixpath
./setup.data/bin/x86/setup -i `pwd`/root -m -n -a || {
: You should disable ./builder logging if you get errors like:
:  Standard input is not a terminal!
:  No UI drivers available
exit 1
}
cd root

# convert links to relative
symlinks -csvr .
# second run will make the relative links short
symlinks -csvr .

sed -i -e "s,$(pwd),%{_datadir}," \
	bin/kylixpath \
	bin/libborcrtl.so \
	bin/registerkylix \
	bin/startbcb \
	bin/startdelphi \
	bin/startkylix \
	help/hyperhelp.sh \
	shortcuts/gnome/hyperhelp.desktop \
	shortcuts/gnome/registerkylix.desktop \
	shortcuts/gnome/startbcb.desktop \
	shortcuts/gnome/startdelphi.desktop \
	shortcuts/kde/hyperhelp.desktop \
	shortcuts/kde/registerkylix.desktop \
	shortcuts/kde/startbcb.desktop \
	shortcuts/kde/startdelphi.desktop \
	uninstall

# ldconfig should create proper links, remove and keep backup in links.tar
#(cd bin; find -type l |xargs tar --remove-files -cf ../links.tar)

# making it easier to install
mv lib data
mkdir -p lib privlib
mv bin/{bpl,lib}*.so.* lib
mv bin/lib*qt*.so lib
mv bin/lib*borland*.so lib
mv bin/libborstl.so lib
mv bin/libborunwind.so lib
mv bin/*.so* privlib
mv data/*.a privlib

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_libdir},%{_bindir},%{_sysconfdir},%{_includedir}} \
	$RPM_BUILD_ROOT{%{_libexecdir}/{lib,bin},%{_desktopdir},%{_examplesdir}/%{name}-%{version}}

cd root
cp -a bin/* $RPM_BUILD_ROOT%{_libexecdir}/bin
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}
cp -a privlib/* $RPM_BUILD_ROOT%{_libexecdir}
cp -a shortcuts/gnome/* $RPM_BUILD_ROOT%{_desktopdir}
cp -a source $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a data/* $RPM_BUILD_ROOT%{_libexecdir}/lib
cp -a include/* $RPM_BUILD_ROOT%{_includedir}
cp -a help images documentation objrepos $RPM_BUILD_ROOT%{_datadir}
cp -a *.xpm oe.slip $RPM_BUILD_ROOT%{_datadir}

install -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/delphi69dro.conf
install -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/bcb69dro.conf

# bad soname, package .so file
#ln -s $(cd $RPM_BUILD_ROOT%{_libdir}; echo libborunwind.so.*.*) $RPM_BUILD_ROOT%{_libdir}/libborunwind.so

# TODO ~/.borland/ files?

# not sure about these
%if 0
# Create dcc.cfg file
cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/kylix/dcc.conf
--msgcatalog=%{_kylixdata}/bin
-u/%{_kylixdata}/lib
-o/%{_kylixdata}/bin
EOF

# Create bcc.cfg file
libgcc_fname=`%{__cc} -print-libgcc-file-name`
libgcc_dir=`dirname $libgcc_fname`

cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/kylix/bccrc
-I"%{_kylixdata}/include/stlport":"%{_kylixdata}/include":"%{_kylixdata}/include/vcl":"%{_includedir}"
-L"%{_kylixdata}/lib/obj":"%{_kylixdata}/lib":"%{_kylixdata}/lib/release":"%{_libdir}":"/lib":"/usr/X11R6/lib":"%{_kylixdata}/bin":"$libgcc_dir"
EOF

# Create ilinkrc.cfg file
cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/kylix/ilinkrc
-L"%{_kylixdata}/lib/obj":"%{_kylixdata}/lib":"%{_kylixdata}/lib/release":"%{_libdir}":"/lib":"/usr/X11R6/lib":"%{_kylixdata}/bin"
EOF

ln -sf %{_sysconfdir}/kylix/borlandrc.conf $RPM_BUILD_ROOT/usr/local/etc
%endif

# wrapper
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/bc++
#ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/bc++.msg
#ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/bcpp.msg
ln -sf bc++ $RPM_BUILD_ROOT%{_bindir}/dcc
#ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/hyperhelp
#ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/kreg
#ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/bcb
#ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/delphi
#ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/bcblin
#ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/ilink
#ln -sf %{_kylixdata}/bin/ilink.msg $RPM_BUILD_ROOT%{_bindir}/ilink.msg

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc DEPLOY INSTALL PREINSTALL README
%doc license.txt privacy.txt
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%{_desktopdir}/*.desktop
%attr(755,root,root) %{_bindir}/*

%attr(755,root,root) %{_libdir}/bplHelpViewers.so.*.*.*
%attr(755,root,root) %{_libdir}/bplbcbclxide.so.*.*.*
%attr(755,root,root) %{_libdir}/bplbcbide.so.*.*.*
%attr(755,root,root) %{_libdir}/bplclxdesigner.so.*.*.*
%attr(755,root,root) %{_libdir}/bplcoreide.so.*.*.*
%attr(755,root,root) %{_libdir}/bpldelphiclxide.so.*.*.*
%attr(755,root,root) %{_libdir}/bpldelphide.so.*.*.*
%attr(755,root,root) %{_libdir}/bpldesigndgm.so.*.*.*
%attr(755,root,root) %{_libdir}/bpldesignhooks.so.*.*.*
%attr(755,root,root) %{_libdir}/bpldesignide.so.*.*.*
%attr(755,root,root) %{_libdir}/bplvcl.so.*.*.*
%attr(755,root,root) %{_libdir}/bplvclex.so.*.*.*
%attr(755,root,root) %{_libdir}/bplvclide.so.*.*.*
%attr(755,root,root) %{_libdir}/libadvapi32.borland.so.*.*
%attr(755,root,root) %{_libdir}/libboredit.so.*.*.*
%attr(755,root,root) %{_libdir}/libborkbd.so.*.*.*
%attr(755,root,root) %{_libdir}/libbortoken.so.*.*.*
%attr(755,root,root) %{_libdir}/libbortoken.so.*.*
%attr(755,root,root) %{_libdir}/libcomctl32.borland.so.*.*
%attr(755,root,root) %{_libdir}/libcomdlg32.borland.so.*.*
%attr(755,root,root) %{_libdir}/libdbk.so.1.9
%attr(755,root,root) %{_libdir}/libdcc.so.*.*.*
%attr(755,root,root) %{_libdir}/libdcc.so.*.*
%attr(755,root,root) %{_libdir}/libgdi32.borland.so.*.*
%attr(755,root,root) %{_libdir}/libibmdom.so.1
%attr(755,root,root) %{_libdir}/libilinkintf.so.*.*.*
%attr(755,root,root) %{_libdir}/libilinkintf.so.*.*
%attr(755,root,root) %{_libdir}/libimm32.borland.so.*.*
%attr(755,root,root) %{_libdir}/libkernel32.borland.so.*.*
%attr(755,root,root) %{_libdir}/liblz32.borland.so.*.*
%attr(755,root,root) %{_libdir}/libmpr.borland.so.*.*
%attr(755,root,root) %{_libdir}/libole32.borland.so.*.*
%attr(755,root,root) %{_libdir}/liboleaut32.borland.so.*.*
%attr(755,root,root) %{_libdir}/libolecli32.borland.so.*.*
%attr(755,root,root) %{_libdir}/liboledlg.borland.so.*.*
%attr(755,root,root) %{_libdir}/libolepro32.borland.so.*.*
%attr(755,root,root) %{_libdir}/libolesvr32.borland.so.*.*
%attr(755,root,root) %{_libdir}/librpcrt4.borland.so.*.*
%attr(755,root,root) %{_libdir}/libshell32.borland.so.*.*
%attr(755,root,root) %{_libdir}/libshlwapi.borland.so.*.*
%attr(755,root,root) %{_libdir}/libuser32.borland.so.*.*
%attr(755,root,root) %{_libdir}/libversion.borland.so.*.*
%attr(755,root,root) %{_libdir}/libwine.borland.so.*.*
%attr(755,root,root) %{_libdir}/libwine_unicode.borland.so.*.*
%attr(755,root,root) %{_libdir}/libwineoss.drv.borland.so.*.*
%attr(755,root,root) %{_libdir}/libwineps.borland.so.*.*
%attr(755,root,root) %{_libdir}/libwininet.borland.so.*.*
%attr(755,root,root) %{_libdir}/libwinmm.borland.so.*.*
%attr(755,root,root) %{_libdir}/libwinspool.drv.borland.so.*.*
%attr(755,root,root) %{_libdir}/libx11drv.borland.so.*.*
%attr(755,root,root) %{_libdir}/libxmlide.so.*.*.*

%dir %{_libexecdir}
%dir %{_libexecdir}/bin
%attr(755,root,root) %{_libexecdir}/bin/*
%{_libexecdir}/lib
%{_libexecdir}/*.a
%{_libexecdir}/comp32p.so
%attr(755,root,root) %{_libexecdir}/dclmlwiz.so.*.*.*
%attr(755,root,root) %{_libexecdir}/dclstd.so.*.*.*
%attr(755,root,root) %{_libexecdir}/dcluser.so.*.*.*
%{_libexecdir}/ilink.so
%{_libexecdir}/libborcrtl.so
%{_libexecdir}/libtextform.so
%{_libexecdir}/libxerces-*.so
%{_libexecdir}/winhelp.so

%{_datadir}
%{_examplesdir}/*
%{_includedir}

%if 0
# unfinished
/usr/local/etc/*
%{_kylixdata}/lib

%dir %{_kylixdata}
%dir %{_kylixdata}/bin
%dir %{_kylixdata}/help
%dir %{_kylixdata}/help/bin
%attr(755,root,root) %{_kylixdata}/help/bin/*
%attr(755,root,root) %{_kylixdata}/help/hyperhelp.sh
%dir %{_kylixdata}/help/lib
%attr(755,root,root) %{_kylixdata}/help/lib/*.so
%{_kylixdata}/help/lib/locale
%{_kylixdata}/help/*.cnt
%{_kylixdata}/help/*.fts
%{_kylixdata}/help/*.hlp
%{_kylixdata}/help/*.txt
%{_kylixdata}/help/*.als
%{_kylixdata}/help/*.ftg
%{_kylixdata}/help/.hyperhelprc
%{_kylixdata}/help/app-defaults
%{_kylixdata}/help/stlport
%{_kylixdata}/help/xprinter

%attr(755,root,root) %{_kylixdata}/bin/kylixpath
%attr(755,root,root) %{_kylixdata}/bin/bc++
%attr(755,root,root) %{_kylixdata}/bin/bc++.msg
%attr(755,root,root) %{_kylixdata}/bin/bcpp
%attr(755,root,root) %{_kylixdata}/bin/bcpp.msg
%attr(755,root,root) %{_kylixdata}/bin/bpr2mak
%attr(755,root,root) %{_kylixdata}/bin/dcc
%attr(755,root,root) %{_kylixdata}/bin/ilink
%attr(755,root,root) %{_kylixdata}/bin/ilink.msg
%attr(755,root,root) %{_kylixdata}/bin/ilink.so
%attr(755,root,root) %{_kylixdata}/bin/libilinkintf*.so*
%attr(755,root,root) %{_kylixdata}/bin/kreg
%attr(755,root,root) %{_kylixdata}/bin/resbind
%attr(755,root,root) %{_kylixdata}/bin/bcblin
%attr(755,root,root) %{_kylixdata}/bin/convert
%attr(755,root,root) %{_kylixdata}/bin/delphi
%attr(755,root,root) %{_kylixdata}/bin/transdlg
%attr(755,root,root) %{_kylixdata}/bin/wineserver

%{_kylixdata}/bin/HTMLlat1.ent
%{_kylixdata}/bin/HTMLspecial.ent
%{_kylixdata}/bin/HTMLsymbol.ent
%{_kylixdata}/bin/bcb.dci
%{_kylixdata}/bin/bcb69dmt
%{_kylixdata}/bin/countrylist.txt
%{_kylixdata}/bin/default.gmk
%{_kylixdata}/bin/deflib.gmk
%{_kylixdata}/bin/delphi.dci
%{_kylixdata}/bin/delphi69dmt
%{_kylixdata}/bin/delphi69upg
%{_kylixdata}/bin/denmark.dem
%{_kylixdata}/bin/france.dem
%{_kylixdata}/bin/germany.dem
%{_kylixdata}/bin/incfiles.dat
%{_kylixdata}/bin/italy.dem
%{_kylixdata}/bin/japan.dem
%{_kylixdata}/bin/korea.dem
%{_kylixdata}/bin/netherld.dem
%{_kylixdata}/bin/norway.dem
%{_kylixdata}/bin/phone.txt
%{_kylixdata}/bin/spain.dem
%{_kylixdata}/bin/statelist.txt
%{_kylixdata}/bin/sweden.dem
%{_kylixdata}/bin/taiwan.dem
%{_kylixdata}/bin/uk.dem
%{_kylixdata}/bin/us.dem
%{_kylixdata}/bin/version.txt
%endif

%files libs
%defattr(644,root,root,755)
# according to DEPLOY
# 2.5.1 GPL-Licensed Packages
#%attr(755,root,root) %{_libdir}/bplbaseclx.so.*.*.*
%attr(755,root,root) %{_libdir}/bplvisualclx.so.*.*.*
%attr(755,root,root) %{_libdir}/libqt.so.*.*.*
%attr(755,root,root) %{_libdir}/libqtintf-*.*.*-qt*.so*
%attr(755,root,root) %{_libdir}/libborqt-*.*.*-qt*.so*
%attr(755,root,root) %{_libdir}/libborunwind.so.*.*
%{_libdir}/libborunwind.so.6
%{_libdir}/libborunwind.so
# 2.5.2 Other packages (not Borland Protected nor Dual-Licensed)
%attr(755,root,root) %{_libdir}/libborstl.so.*.*
%attr(755,root,root) %{_libdir}/libborcrtl.so.*.*

# this one was not mentioned in DEPLOY file but IMVHO it ought to be...
# and this makes the package not redistributable
%attr(755,root,root) %{_libdir}/bplrtl.so.*.*.*
