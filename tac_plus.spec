
%define subver	alpha

Summary:	Cisco Tacacs+ Daemon
Name:		tac_plus
Version:	F4.0.3
Release:	0.alpha.9a.0
Epoch:		0
Copyright:	Cisco systems, Inc.
Group:		Networking/Daemons
URL:		http://www.gazi.edu.tr/tacacs
Source0:	%{name}.%{version}.%{subver}.tar.Z
# Source0-md5:	451d92503b5832a848c1b76ce58a4636
Source1:	%{name}.cfg
Source2:	%{name}.init
Source3:	%{name}.pam
Source4:	README.PAM
Source5:	%{name}.sql
Source6:	%{name}.rotate
Source7:	README.LDAP
Patch0:		%{name}.patch
Patch1:		%{name}_v9a.patch
BuildRequires:	autoconf
BuildRequires:	pam-devel
BuildRequires:	libwrap-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TACACS+ daemon using with Cisco's NASs (Or other vendors) for AAA
(Authentication , Authorization and Accounting) propose.


%prep
%setup -q -n tac_plus.%{version}.%{subver}
%patch0 -p1
%patch1 -p1

%build
rm configure
%{__autoconf}
%configure \
    --with-pam \
    --enable-maxsess \
    --with-libwrap \
    --without-db

# configure script have some options describe below
# --with-pam  : For PAM support
# --with-ldap : For LDAP support
# --with-db   : If you like to use db feature you must enable it
# --with-mysql: For MySQL database support
# --with-mysql-include-dir=PREFIX :  Mysql include path [default=/usr/include/mysql]
# --with-mysql-lib-dir=PREFIX  Mysql library path [default=/usr/lib/mysql]
# --with-pgsql		With PgSQL Support
# --with-pgsql-include-dir=PREFIX  PgSQL include path [default=/usr/include/pgsql]
# --with-pgsql-lib-dir=PREFIX  PgSQL library path [default=/usr/lib/pgsql]

# --enable-maxsess: For check concurrent logins
# --with-tacuid: If you like to run tac_plus specify UID
# --with-tacgid: If you like to run tac_plus specify GID
# --with-tacplus_pid=PREFIX  Tac_plus pid file location [default=/var/run]
# --with-libwrap[=PATH]   Compile in libwrap (tcp_wrappers) support
# --enable-finger	Enable finger at maxsess check

%{__make} tac_plus


%install
rm -rf $RPM_BUILD_ROOT

%{__make} rpm_install \
    DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}{/tacacs,/logrotate.d,/pam.d,/rc.d{/init.d,/rc{0,1,2,3,4,5,6}.d}}
install %SOURCE2 $RPM_BUILD_ROOT/etc/rc.d/init.d/tac_plus
install %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/tacacs/
install %SOURCE3 $RPM_BUILD_ROOT/etc/pam.d/pap
install %SOURCE6 $RPM_BUILD_ROOT/etc/logrotate.d/tac_plus

install {%SOURCE4,%SOURCE5,%SOURCE7} %{_builddir}/%{name}.%{version}.%{subver}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -f /etc/tacacs/tac_plus.cfg ]; then
	cp -a /etc/tacacs/tac_plus.cfg /etc/tacacs/tac_plus.cfg.old
fi

if [ -f /etc/tacacs/tac_plus.pam ]; then
	cp /etc/pam.d/tac_plus.pam /etc/pam.d/tac_plus.pam.old
fi

%post
/sbin/chkconfig --add tac_plus
echo "Type \"/etc/rc.d/init.d/tac_plus start\" to start tac_plus" 1>&2

%preun
if [ $1 = 0 ]; then
   if [ -f /var/lock/subsys/tac_plus ]; then
      /etc/rc.d/init.d/tac_plus stop
   fi
   /sbin/chkconfig --del tac_plus
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/tacacs
%config /etc/logrotate.d/tac_plus
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/tacacs/tac_plus.cfg
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/pap
%attr(754,root,root) 		/etc/rc.d/init.d/tac_plus
%attr(755,root,root) 		%{_sbindir}/generate_passwd
%attr(755,root,root) 		%{_sbindir}/tac_plus
%attr(644,root,root) 		%{_mandir}/man1/*
%doc users_guide CHANGES convert.pl README.PAM tac_plus.sql README.LDAP
