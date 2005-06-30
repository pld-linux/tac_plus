
%define subver	alpha

Summary:	Tacacs+ Daemon
Summary(pl):	Demon Tacacs+
Name:		tac_plus
Version:	F4.0.3
Release:	0.alpha.9a.1
Epoch:		0
License:	BSD-like, GPL
Group:		Networking/Daemons
Source0:	http://www.gazi.edu.tr/tacacs/src/%{name}.%{version}.%{subver}.tar.Z
# Source0-md5:	451d92503b5832a848c1b76ce58a4636
Source1:	%{name}.cfg
Source2:	%{name}.init
Source3:	%{name}.pam
Source4:	README.PAM
Source5:	%{name}.sql
Source6:	%{name}.rotate
Source7:	README.LDAP
Source8:	%{name}.sysconfig
Patch0:		%{name}.patch
Patch1:		%{name}_v9a.patch
Patch2:		%{name}-mysql4.patch
Patch3:		%{name}-ldap-alt.patch
URL:		http://www.gazi.edu.tr/tacacs/
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libwrap-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	postgresql-devel
PreReq:		rc-scripts
Requires(pre):	fileutils
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TACACS+ daemon using with Cisco's NASs (or other vendors) for AAA
(Authentication, Authorization and Accounting) propose.

%description -l pl
Demon TACACS+ u¿ywany wraz z NAS-ami Cisco (lub innych producentów) do
celów uwierzytelniania, autoryzacji i rozliczania (AAA -
Authentication, Authorization and Accounting).

%prep
%setup -q -n tac_plus.%{version}.%{subver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

rm -f configure

%build
cp /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%configure \
	--with-pam \
	--enable-maxsess \
	--with-libwrap \
	--with-db \
	--with-ldap \
	--with-pgsql \
	--with-mysql

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

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/tacacs,/etc/{logrotate.d,pam.d,rc.d/init.d,sysconfig}}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/tac_plus
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/tacacs
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/tac_plus
install %{SOURCE6} $RPM_BUILD_ROOT/etc/logrotate.d/tac_plus
install %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/tac_plus

install {%{SOURCE4},%{SOURCE5},%{SOURCE7}} .

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add tac_plus
echo "Type \"/etc/rc.d/init.d/tac_plus start\" to start tac_plus" 1>&2

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/tac_plus ]; then
		/etc/rc.d/init.d/tac_plus stop
	fi
	/sbin/chkconfig --del tac_plus
fi

%files
%defattr(644,root,root,755)
%doc users_guide CHANGES convert.pl README.PAM tac_plus.sql README.LDAP
%attr(755,root,root) %{_sbindir}/generate_passwd
%attr(755,root,root) %{_sbindir}/tac_plus
%dir %{_sysconfdir}/tacacs
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tacacs/tac_plus.cfg
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/tac_plus
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/tac_plus
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/tac_plus
%attr(754,root,root) /etc/rc.d/init.d/tac_plus
%{_mandir}/man1/*
