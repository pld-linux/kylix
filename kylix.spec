Summary:	Kylix 3 Open Edition
Name:		kylix3_open
Version:	1.0
Release:	1
License:	GPL
Group:		X11/Development/Tools
Source0:	ftp://ftpd.borland.com/download/kylix/k3/%{name}.tar.gz
Source1:	%{name}.response
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
cat setup.data/main.sh | sed s%~%$RPM_BUILD_ROOT/home% > ./main.sh
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

cd $RPM_BUILD_ROOT//usr/share/kylix3_open/help/lib/locale/
rm ja_JP.eucjp
# FIXME: I don't know how to add symlinks to rpm
#ln -s ja_JP.eucJP ja_JP.eucjp

#mv $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/*.so.* $RPM_BUILD_ROOT/usr/lib
#mv $RPM_BUILD_ROOT/usr/share/kylix3_open/bin/*.so $RPM_BUILD_ROOT/usr/lib
#cd $RPM_BUILD_ROOT/usr/lib
cd $RPM_BUILD_ROOT/usr/share/kylix3_open/bin

for k in *6.9.0* ; do k2=`echo $k | sed s/6.9.0\$/6.9/` ; if ! [ -f $k2 ] ; then ln -s $k $k2 ; fi ; done

cd $oldpath

cp -p $RPM_BUILD_ROOT/home/.borland/.borlandrc $RPM_BUILD_ROOT/etc/kylix/borlandrc.conf
ln -sf /etc/kylix/borlandrc.conf $RPM_BUILD_ROOT/usr/local/etc

cat > $RPM_BUILD_ROOT/usr/bin/bc++ <<"EOF"
#!/bin/bash

# BEGIN STRING TABLE

KYDEF_LOCALE="en_US"
LC_ALL_IS_C1="The LC_ALL environment variable is set to C.  Kylix cannot start with this setting."
LC_ALL_IS_C2="Defaulting LC_ALL to"
KHOME="$HOME/.borland"
KDIR=/usr/share/kylix3_open
KBIN=$KDIR/bin

# END STRING TABLE

if [ -z "\$LANG" ]; then
   LANG=\$KYDEF_LOCALE
   export LANG
fi

if [ "\$LC_ALL" = "C" ]; then
   echo "\$LC_ALL_IS_C1"
   echo "\$LC_ALL_IS_C2 \$KYDEF_LOCALE."
   LC_ALL=\$KYDEF_LOCALE
   export LC_ALL
fi

if [ ! -d "$KHOME" ]; then
  mkdir $KHOME
  kreg
fi

$KBIN/kylixpath
$KBIN/`echo $0 | sed 's+.*/++'` $@
EOF

ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/bc++.msg
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/bcpp.msg 
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/dcc
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/hyperhelp
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/ilink.msg
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/kreg
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/bcb
ln -sf /usr/bin/bc++ $RPM_BUILD_ROOT/usr/bin/delphi


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
%attr(755,root,root) /usr/share/kylix3_open/bin/*.so*
#%attr(755,root,root) /usr/lib/*.so*

%config(noreplace) /etc/kylix/borlandrc.conf
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
