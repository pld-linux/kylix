Summary:	Kylix 3 Open Edition
Name:		kylix3_open
Version:	1.0
Release:	3
License:	non-distributable
Group:		X11/Development/Tools
Source0:	ftp://ftpd.borland.com/download/kylix/k3/%{name}.tar.gz
Source1:	%{name}.response
Source2:	%{name}.wrapper
Source3:	%{name}.dro
Patch0:		%{name}-setup.patch
URL:		http://www.borland.com/kylix/kylix3open.shtml
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kylix

%description -l pl
Kylix

%prep
%setup -q -n %{name}
install %{SOURCE1} .
%patch0 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/lib
install -d $RPM_BUILD_ROOT/usr/bin
install -d $RPM_BUILD_ROOT/home/bin
install -d $RPM_BUILD_ROOT/usr/share/doc/kylix3_open-1.0
install -d $RPM_BUILD_ROOT/usr/share/kylix3_open
install -d $RPM_BUILD_ROOT/usr/local/etc
install -d $RPM_BUILD_ROOT/etc/kylix
install -d $RPM_BUILD_ROOT/usr/X11R6/share/applnk/Development/Kylix

cat %{SOURCE1} | sed "s~@INSTALL@~$RPM_BUILD_ROOT/usr/share/kylix3_open~" | sed "s~@SYMLINKS@~$RPM_BUILD_ROOT/home/bin~" > response

./setup.sh -m -a -n < response
#cat setup.data/main.sh | sed s%~%$RPM_BUILD_ROOT/home% | sed s%\$SETUP_INSTALLPATH%$RPM_BUILD_ROOT/usr/share/kylix3_open%g > ./main.sh
cat setup.data/main.sh | sed s%~%$RPM_BUILD_ROOT/home% | sed s~\$inimerge.*~~ > ./main.sh
chmod +x ./main.sh
./main.sh

# FIXME:
#cp -r $RPM_BUILD_ROOT/usr/share/kylix3_open/documentation $RPM_BUILD_ROOT/usr/share/doc/kylix3_open-1.0
#ln -s $RPM_BUILD_ROOT/usr/share/kylix3_open/documentation $RPM_BUILD_ROOT/usr/share/doc/kylix3_open-1.0

oldpath=`pwd`
cd $RPM_BUILD_ROOT/usr/share/kylix3_open/help/app-defaults/
rm ja_JP.eucjp
# FIXME: I don't know how to add symlinks to rpm
#ln -s ja_JP.eucJP ja_JP.eucjp

cd $RPM_BUILD_ROOT/usr/share/kylix3_open/help/lib/locale/
rm ja_JP.eucjp
# FIXME: I don't know how to add symlinks to rpm
#ln -s ja_JP.eucJP ja_JP.eucjp

# libraries
# Create bin/libborcrtl.so file
cat << EOF > $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/libborcrtl.so
GROUP ( $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/libborcrtl.so.1 $RPM_BUILD_ROOT/usr/share/kylix3_open/lib/libborcrtl_nonshared.a )
EOF
chmod a+x $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/libborcrtl.so

mv $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/*.so.* $RPM_BUILD_ROOT/usr/lib
mv $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/*.so $RPM_BUILD_ROOT/usr/lib
cd $RPM_BUILD_ROOT/usr/lib
#cd $RPM_BUILD_ROOT/usr/share/kylix3_open/bin

for k in *6.9.0* ; do k2=`echo $k | sed s/6.9.0\$/6.9/` ; if ! [ -f $k2 ] ; then ln -s $k $k2 ; fi ; done
ln -sf libdbk.so.1.9 libdbk.so.1
ln -sf libqt.so.2.3.0 libqt.so.2
ln -sf libborunwind.so.6.0 libborunwind.so.6
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
ln -sf libborunwind.so.6 libborunwind.so


# /etc directory
cd $oldpath

cp -p $RPM_BUILD_ROOT/home/.borland/.borlandrc $RPM_BUILD_ROOT/etc/kylix/borlandrc.conf
cp $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/delphi69upg $RPM_BUILD_ROOT/etc/kylix/delphi69upg.conf
cp $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/delphi.dci $RPM_BUILD_ROOT/etc/kylix/delphi69dci.conf
cp $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/bcb.dci $RPM_BUILD_ROOT/etc/kylix/bcb69dci.conf
cp $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/delphi69dmt $RPM_BUILD_ROOT/etc/kylix/delphi69dmt.conf
cp $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/bcb69dmt $RPM_BUILD_ROOT/etc/kylix/bcb69dmt.conf
cp $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/incfiles.dat $RPM_BUILD_ROOT/etc/kylix/incfilesdat.conf

cat %{SOURCE3} > $RPM_BUILD_ROOT/etc/kylix/delphi69dro.conf
cat %{SOURCE3} > $RPM_BUILD_ROOT/etc/kylix/bcb69dro.conf


# Create dcc.cfg file
cat <<EOF > $RPM_BUILD_ROOT/etc/kylix/dcc.conf
--msgcatalog=/usr/share/kylix3_open/bin
-u/usr/share/kylix3_open/lib
-o/usr/share/kylix3_open/bin
EOF

# Create bcc.cfg file

libgcc_fname=`gcc -print-libgcc-file-name`
libgcc_dir=`dirname $libgcc_fname`

cat << EOF > $RPM_BUILD_ROOT/etc/kylix/bccrc
-I"/usr/share/kylix3_open/include/stlport":"/usr/share/kylix3_open/include":"/usr/share/kylix3_open/include/vcl":"/usr/include"
-L"/usr/share/kylix3_open/lib/obj":"/usr/share/kylix3_open/lib":"/usr/share/kylix3_open/lib/release":"/usr/lib":"/lib":"/usr/X11R6/lib":"/usr/share/kylix3_open/bin":"$libgcc_dir"
EOF

# Create ilinkrc.cfg file
cat << EOF > $RPM_BUILD_ROOT/etc/kylix/ilinkrc
-L"/usr/share/kylix3_open/lib/obj":"/usr/share/kylix3_open/lib":"/usr/share/kylix3_open/lib/release":"/usr/lib":"/lib":"/usr/X11R6/lib":"/usr/share/kylix3_open/bin"
EOF


ln -sf /etc/kylix/borlandrc.conf $RPM_BUILD_ROOT/usr/local/etc

# wrapper
cat %{SOURCE2}> $RPM_BUILD_ROOT/usr/bin/bc++
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/bc++.msg
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/bcpp.msg 
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/dcc
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/hyperhelp
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/ilink.msg
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/kreg
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/bcb
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/delphi
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/bcblin


# kylixpath
cat > $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/kylixpath <<EOF
#!/bin/bash

prepath=/usr/share/kylix3_open
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
for kpath in \$kylixpath\$h \$kylixpath\$l \$kylixpath\$b; do
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
for kpath in \$kylixpath\$hl \$kylixpath\$hl/locale/\$locale \$kylixpath\$b; do
   for ppath in \`echo \$LD_LIBRARY_PATH | sed s/:/\ /g\`; do
      if [ "\$kpath" = "\$ppath" ]; then
         path_found="Y"
      fi
   done
   if [ -z "\$path_found" ]; then
      LD_LIBRARY_PATH="\$kpath:\$LD_LIBRARY_PATH"
   fi
done

XPPATH="\$kylixpath\$h/xprinter"

HHHOME="\$kylixpath\$h"

XAPPLRESDIR="\$kylixpath\$h/app-defaults"

NLSPATH="\$kylixpath\$hl/locale/%L/%N.cat"

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

cp -f $RPM_BUILD_ROOT/usr/share/kylix3_open/shortcuts/gnome/* $RPM_BUILD_ROOT/usr/X11R6/share/applnk/Development/Kylix
cat > $RPM_BUILD_ROOT/usr/X11R6/share/applnk/Development/Kylix/.directory << EOF
[Desktop Entry]
Name=Kylix
Name[pl]=Kylix
Comment=Kylix
Comment[pl]=Kylix
#Icon=
Type=Directory
EOF

oldpath=`pwd`
cd $RPM_BUILD_ROOT/usr/X11R6/share/applnk/Development/Kylix

for k in *.desktop
do
  cat $k | sed "s+$RPM_BUILD_ROOT++" > tmp
  mv tmp $k
  cat $k | sed "s%/usr/share/kylix3_open/bin/registerkylix%/usr/bin/kreg%" > tmp
  mv tmp $k
  cat $k | sed "s%/usr/share/kylix3_open/bin/startbcb%/usr/bin/bcblin%" > tmp
  mv tmp $k
  cat $k | sed "s%/usr/share/kylix3_open/bin/startdelphi%/usr/bin/delphi%" > tmp
  mv tmp $k
done

cd $oldpath

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%preun

%post
/sbin/ldconfig

%postun



%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) /usr/lib/*.so*
#%attr(755,root,root) /usr/share/kylix3_open/bin/*.so*

%config(noreplace) /etc/kylix/*
/usr/local/etc
/usr/X11R6/share/applnk/Development/Kylix

%attr(755,root,root) /usr/bin/*

/usr/share/kylix3_open/*.xpm
/usr/share/kylix3_open/*.slip
/usr/share/kylix3_open/*.txt
/usr/share/kylix3_open/DEPLOY
/usr/share/kylix3_open/INSTALL
/usr/share/kylix3_open/PREINSTALL


/usr/share/kylix3_open/source
/usr/share/kylix3_open/shortcuts
/usr/share/kylix3_open/objrepos
/usr/share/kylix3_open/lib
/usr/share/kylix3_open/include
/usr/share/kylix3_open/images
/usr/share/kylix3_open/examples
/usr/share/kylix3_open/documentation
# FIXME
/usr/share/kylix3_open/help

%attr(755,root,root) /usr/share/kylix3_open/bin/kylixpath
%attr(755,root,root) /usr/share/kylix3_open/bin/bc++
%attr(755,root,root) /usr/share/kylix3_open/bin/bc++.msg
%attr(755,root,root) /usr/share/kylix3_open/bin/bcpp
%attr(755,root,root) /usr/share/kylix3_open/bin/bcpp.msg
%attr(755,root,root) /usr/share/kylix3_open/bin/bpr2mak
%attr(755,root,root) /usr/share/kylix3_open/bin/dbkexe-1.9
%attr(755,root,root) /usr/share/kylix3_open/bin/dcc
%attr(755,root,root) /usr/share/kylix3_open/bin/ilink
%attr(755,root,root) /usr/share/kylix3_open/bin/ilink.msg
%attr(755,root,root) /usr/share/kylix3_open/bin/kreg
%attr(755,root,root) /usr/share/kylix3_open/bin/resbind
%attr(755,root,root) /usr/share/kylix3_open/bin/bcblin
%attr(755,root,root) /usr/share/kylix3_open/bin/convert
%attr(755,root,root) /usr/share/kylix3_open/bin/delphi
%attr(755,root,root) /usr/share/kylix3_open/bin/transdlg
%attr(755,root,root) /usr/share/kylix3_open/bin/wineserver


%attr(644,root,root) /usr/share/kylix3_open/bin/HTMLlat1.ent
%attr(644,root,root) /usr/share/kylix3_open/bin/HTMLspecial.ent
%attr(644,root,root) /usr/share/kylix3_open/bin/HTMLsymbol.ent
%attr(644,root,root) /usr/share/kylix3_open/bin/bcb.dci
%attr(644,root,root) /usr/share/kylix3_open/bin/bcb69dmt
%attr(644,root,root) /usr/share/kylix3_open/bin/countrylist.txt
%attr(644,root,root) /usr/share/kylix3_open/bin/default.gmk
%attr(644,root,root) /usr/share/kylix3_open/bin/deflib.gmk
%attr(644,root,root) /usr/share/kylix3_open/bin/delphi.dci
%attr(644,root,root) /usr/share/kylix3_open/bin/delphi69dmt
%attr(644,root,root) /usr/share/kylix3_open/bin/delphi69upg
%attr(644,root,root) /usr/share/kylix3_open/bin/denmark.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/france.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/germany.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/incfiles.dat
%attr(644,root,root) /usr/share/kylix3_open/bin/italy.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/japan.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/korea.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/netherld.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/norway.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/phone.txt
%attr(644,root,root) /usr/share/kylix3_open/bin/spain.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/statelist.txt
%attr(644,root,root) /usr/share/kylix3_open/bin/sweden.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/taiwan.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/uk.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/us.dem
%attr(644,root,root) /usr/share/kylix3_open/bin/version.txt
