#TODO:
# - kde applnk to help system does not work (have $RPM_BUILD_ROOT path inside)
# - more subpackages: -bcb -delphi -bcb-ide -delphi-ide -doc
# - spec cleanup required...

Summary:	Kylix 3 Open Edition
Summary(pl):	Kylix 3 - Wydanie otwarte
Name:		kylix3_open
Version:	1.0
Release:	5
License:	non-distributable
Group:		X11/Development/Tools
Source0:	ftp://ftpd.borland.com/download/kylix/k3/%{name}.tar.gz
Source1:	%{name}.response
Source2:	%{name}.wrapper
Source3:	%{name}.dro
Patch0:		%{name}-setup.patch
NoSource:	0
URL:		http://www.borland.com/kylix/open/
Requires:	%{name}-libs = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_kylixdata	/usr/share/kylix3_open

%description
Kylix.

%description -l pl
Kylix.

%package libs
Summary:	Kylix libraries
Summary(pl):	Biblioteki Kyliksa
Group:		Development/Libraries
License:	redistributable

%description libs
Kylix libraries.

%description libs -l pl
Biblioteki Kyliksa.

%prep
%setup -q -n %{name}
install %{SOURCE1} .
%patch0 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT/home/bin
install -d $RPM_BUILD_ROOT%{_datadir}/doc/kylix3_open-1.0
install -d $RPM_BUILD_ROOT%{_kylixdata}
install -d $RPM_BUILD_ROOT/usr/local/etc
install -d $RPM_BUILD_ROOT%{_sysconfdir}/kylix
install -d $RPM_BUILD_ROOT%{_applnkdir}/Development/Kylix

cat %{SOURCE1} | sed "s:@INSTALL@:$RPM_BUILD_ROOT%{_kylixdata}:" | sed "s~@SYMLINKS@~$RPM_BUILD_ROOT/home/bin~" > response

./setup.sh -m -a -n < response
#cat setup.data/main.sh | sed s:~:$RPM_BUILD_ROOT/home: | sed s:\$SETUP_INSTALLPATH:$RPM_BUILD_ROOT%{_kylixdata}:g > ./main.sh
cat setup.data/main.sh | sed s:~:$RPM_BUILD_ROOT/home: | sed s:\$inimerge.*:: > ./main.sh
chmod +x ./main.sh
./main.sh

# FIXME:
#cp -r $RPM_BUILD_ROOT%{_kylixdata}/documentation $RPM_BUILD_ROOT/usr/share/doc/kylix3_open-1.0
#ln -s $RPM_BUILD_ROOT%{_kylixdata}/documentation $RPM_BUILD_ROOT/usr/share/doc/kylix3_open-1.0

oldpath=`pwd`
cd $RPM_BUILD_ROOT%{_kylixdata}/help/app-defaults/
rm ja_JP.eucjp
# FIXME: I don't know how to add symlinks to rpm
#ln -s ja_JP.eucJP ja_JP.eucjp

cd $RPM_BUILD_ROOT%{_kylixdata}/help/lib/locale/
rm ja_JP.eucjp
# FIXME: I don't know how to add symlinks to rpm
#ln -s ja_JP.eucJP ja_JP.eucjp

# libraries
# Create bin/libborcrtl.so file - this one is unneded - i think so... (pascalek)
#cat << EOF > $RPM_BUILD_ROOT%{_libdir}/libborcrtl.so
#GROUP ( %{_kylixdata}/lib/libborcrtl.so.1.0 %{_kylixdata}/lib/libborcrtl_nonshared.a )
#EOF
#??? chmod a+x $RPM_BUILD_ROOT%{_kylixdata}/bin/libborcrtl.so

mv $RPM_BUILD_ROOT%{_kylixdata}/bin/*.so.* $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_kylixdata}/bin/*.so $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_libdir}/*ilink*.so* $RPM_BUILD_ROOT%{_kylixdata}/bin

cd $RPM_BUILD_ROOT%{_libdir}
#cd $RPM_BUILD_ROOT%{_kylixdata}/bin

for k in *6.9.0* ; do k2=`echo $k | sed s/6.9.0\$/6.9/` ; if ! [ -f $k2 ] ; then ln -s $k $k2 ; fi ; done
ln -sf libborqt-6.9.0-qt2.3.so libborqt-6.9-qt2.3.so
ln -sf libqtintf-6.9.0-qt2.3.so libqtintf-6.9-qt2.3.so
ln -sf libdbk.so.1.9 libdbk.so.1
ln -sf libqt.so.2.3.0 libqt.so.2
ln -sf librpcrt4.borland.so.1.0 librpcrt4.borland.so
ln -sf libadvapi32.borland.so.1.0 libadvapi32.borland.so
ln -sf libwine_unicode.borland.so.1.0 libwine_unicode.borland.so
ln -sf libborcrtl.so.1.0 libborcrtl.so.1
ln -sf libborstl.so.1.0 libborstl.so
ln -sf libcomctl32.borland.so.1.0 libcomctl32.borland.so
ln -sf libcomdlg32.borland.so.1.0 libcomdlg32.borland.so
ln -sf libgdi32.borland.so.1.0 libgdi32.borland.so
ln -sf libimm32.borland.so.1.0 libimm32.borland.so
ln -sf liblz32.borland.so.1.0 liblz32.borland.so
ln -sf libmpr.borland.so.1.0 libmpr.borland.so
ln -sf libole32.borland.so.1.0 libole32.borland.so
ln -sf liboleaut32.borland.so.1.0 liboleaut32.borland.so
ln -sf libolecli32.borland.so.1.0 libolecli32.borland.so
ln -sf liboledlg.borland.so.1.0 liboledlg.borland.so
ln -sf libolepro32.borland.so.1.0 libolepro32.borland.so
ln -sf libolesvr32.borland.so.1.0 libolesvr32.borland.so
ln -sf libshell32.borland.so.1.0 libshell32.borland.so
ln -sf libuser32.borland.so.1.0 libuser32.borland.so
ln -sf libversion.borland.so.1.0 libversion.borland.so
ln -sf libwine.borland.so.1.0 libwine.borland.so
ln -sf libwineoss.drv.borland.so.1.0 libwineoss.drv.borland.so
ln -sf libwinmm.borland.so.1.0 libwinmm.borland.so
ln -sf libwinspool.drv.borland.so.1.0 libwinspool.drv.borland.so
ln -sf libx11drv.borland.so.1.0 libx11drv.borland.so
ln -sf libwininet.borland.so.1.0 libwininet.borland.so
ln -sf libkernel32.borland.so.1.0 libkernel32.borland.so
ln -sf libwineps.borland.so.1.0 libwineps.borland.so
ln -sf libshlwapi.borland.so.1.0 libshlwapi.borland.so
ln -sf libborunwind.so.6.0 libborunwind.so.6

# /etc directory
cd $oldpath

cp -p $RPM_BUILD_ROOT/home/.borland/.borlandrc $RPM_BUILD_ROOT%{_sysconfdir}/kylix/borlandrc.conf
cp $RPM_BUILD_ROOT%{_kylixdata}/bin/delphi69upg $RPM_BUILD_ROOT%{_sysconfdir}/kylix/delphi69upg.conf
cp $RPM_BUILD_ROOT%{_kylixdata}/bin/delphi.dci $RPM_BUILD_ROOT%{_sysconfdir}/kylix/delphi69dci.conf
cp $RPM_BUILD_ROOT%{_kylixdata}/bin/bcb.dci $RPM_BUILD_ROOT%{_sysconfdir}/kylix/bcb69dci.conf
cp $RPM_BUILD_ROOT%{_kylixdata}/bin/delphi69dmt $RPM_BUILD_ROOT%{_sysconfdir}/kylix/delphi69dmt.conf
cp $RPM_BUILD_ROOT%{_kylixdata}/bin/bcb69dmt $RPM_BUILD_ROOT%{_sysconfdir}/kylix/bcb69dmt.conf
cp $RPM_BUILD_ROOT%{_kylixdata}/bin/incfiles.dat $RPM_BUILD_ROOT%{_sysconfdir}/kylix/incfilesdat.conf

cat %{SOURCE3} > $RPM_BUILD_ROOT%{_sysconfdir}/kylix/delphi69dro.conf
cat %{SOURCE3} > $RPM_BUILD_ROOT%{_sysconfdir}/kylix/bcb69dro.conf

mv $RPM_BUILD_ROOT%{_kylixdata}/bin/dbkexe* $RPM_BUILD_ROOT%{_libdir}

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

# wrapper
cat %{SOURCE2}> $RPM_BUILD_ROOT%{_bindir}/bc++
ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/bc++.msg
ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/bcpp.msg
ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/dcc
ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/hyperhelp
ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/kreg
ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/bcb
ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/delphi
ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/bcblin
ln -sf %{_bindir}/bc++ $RPM_BUILD_ROOT%{_bindir}/ilink
ln -sf %{_kylixdata}/bin/ilink.msg $RPM_BUILD_ROOT%{_bindir}/ilink.msg


# kylixpath
cat > $RPM_BUILD_ROOT%{_kylixdata}/bin/kylixpath <<EOF
#!/bin/bash

prepath=%{_kylixdata}
if  [ -n "\$1" ]; then
    prepath=\$1
fi
kylixpath=\$prepath/
has_slash=\`expr "\$kylixpath" : '\(.*//\)'\`
if [ -n "\$has_slash" ]
then
   kylixpath=\$prepath
else
   kylixpath=\$prepath/
fi
b=bin
l=lib
h=help
hl=help/lib

path_found=
for kpath in \$kylixpath/\$h \$kylixpath/\$l \$kylixpath/\$b; do
   for ppath in \`echo \$PATH | sed s/:/\ /g\`; do
      if [ "\$kpath" = "\$ppath" ]; then
         path_found="Y"
      fi
   done
   if [ -z "\$path_found" ]; then
      PATH="\$kpath:\$PATH"
   fi
done

locale=\${LC_ALL:-\${LC_CTYPE:-\${LANG:-"C"}}}
path_found=
for kpath in \$kylixpath/\$hl \$kylixpath/\$hl/locale/\$locale \$kylixpath/\$b; do
   for ppath in \`echo \$LD_LIBRARY_PATH | sed s/:/\ /g\`; do
      if [ "\$kpath" = "\$ppath" ]; then
         path_found="Y"
      fi
   done
   if [ -z "\$path_found" ]; then
      LD_LIBRARY_PATH="\$kpath:\$LD_LIBRARY_PATH"
   fi
done

XPPATH="\$kylixpath/\$h/xprinter"

HHHOME="\$kylixpath/\$h"

XAPPLRESDIR="\$kylixpath/\$h/app-defaults"

NLSPATH="\$kylixpath/\$hl/locale/%L/%N.cat"

export PATH
export LD_LIBRARY_PATH
export XPPATH
export HHHOME
export XAPPLRESDIR
export NLSPATH
#echo "PATH $PATH_SET_TO"
#echo "\$PATH"
#echo ""
#echo "LD_LIBRARY_PATH $PATH_SET_TO"
#echo "\$LD_LIBRARY_PATH"
#echo ""
#echo "XPPATH $PATH_SET_TO"
#echo "\$XPPATH"
#echo ""
#echo "HHHOME $PATH_SET_TO"
#echo "\$HHHOME"
#echo ""
#echo "XAPPLRESDIR $PATH_SET_TO"
#echo "\$XAPPLRESDIR"
#echo ""
#echo "NLSPATH $PATH_SET_TO"
#echo "\$NLSPATH"

EOF

cp -f $RPM_BUILD_ROOT%{_kylixdata}/shortcuts/gnome/* $RPM_BUILD_ROOT%{_applnkdir}/Development/Kylix
cat > $RPM_BUILD_ROOT%{_applnkdir}/Development/Kylix/.directory << EOF
[Desktop Entry]
Name=Kylix
Name[pl]=Kylix
Comment=Kylix
Comment[pl]=Kylix
#Icon=
Type=Directory
EOF

oldpath=`pwd`
cd $RPM_BUILD_ROOT%{_applnkdir}/Development/Kylix

for k in *.desktop
do
  cat $k | sed "s+$RPM_BUILD_ROOT++" > tmp
  cat tmp | sed "s:%{_kylixdata}/bin/registerkylix:%{_bindir}/kreg:" > $k
  cat $k | sed "s:%{_kylixdata}/bin/startbcb:%{_bindir}/bcblin:" > tmp
  cat tmp | sed "s:%{_kylixdata}/bin/startdelphi:%{_bindir}/delphi:" > $k
done

cd $oldpath

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README

%attr(755,root,root) %{_libdir}/bpl[Hcd]*.so*
%attr(755,root,root) %{_libdir}/bplbcb*.so*
%attr(755,root,root) %{_libdir}/bplvcl*.so*
%attr(755,root,root) %{_libdir}/comp32p*.so*
%attr(755,root,root) %{_libdir}/dcl*.so*
%attr(755,root,root) %{_libdir}/lib[acdgiklmorstuwx]*.so*
%attr(755,root,root) %{_libdir}/libboredit*.so*
%attr(755,root,root) %{_libdir}/libborkbd*.so*
%attr(755,root,root) %{_libdir}/libbortoken*.so*
%attr(755,root,root) %{_libdir}/libversion*.so*
%attr(755,root,root) %{_libdir}/winhelp*.so*
%attr(755,root,root) %{_libdir}/dbkexe*

%config(noreplace) %{_sysconfdir}/kylix/*
/usr/local/etc
%{_applnkdir}/Development/Kylix

%attr(755,root,root) %{_bindir}/*

%{_kylixdata}/*.xpm
%{_kylixdata}/*.slip
%{_kylixdata}/*.txt
%{_kylixdata}/DEPLOY
%{_kylixdata}/INSTALL
%{_kylixdata}/PREINSTALL
%{_kylixdata}/source
%{_kylixdata}/shortcuts
%{_kylixdata}/objrepos
%{_kylixdata}/include
%{_kylixdata}/images
%{_kylixdata}/examples
%{_kylixdata}/documentation
%{_kylixdata}/lib

%dir %{_kylixdata}/help/
%dir %{_kylixdata}/help/bin
%dir %{_kylixdata}/help/lib
%attr(755,root,root) %{_kylixdata}/help/bin/*
%attr(755,root,root) %{_kylixdata}/help/hyperhelp.sh
%attr(755,root,root) %{_kylixdata}/help/lib/*.so
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
%{_kylixdata}/help/lib/locale

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

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/bplvisualclx.so*
%attr(755,root,root) %{_libdir}/libqt.so*
%attr(755,root,root) %{_libdir}/libqtintf-*
%attr(755,root,root) %{_libdir}/libborqt-*
%attr(755,root,root) %{_libdir}/libborunwind.so*
%attr(755,root,root) %{_libdir}/libborstl.so*
%attr(755,root,root) %{_libdir}/libborcrtl.so*

#this one was not mentioned in DEPLOY file
#but IMVHO it ought to be...
%attr(755,root,root) %{_libdir}/bplrtl.so*

#and this one was :)
#%attr(755,root,root) %{_libdir}/bplbaseclx.so*
