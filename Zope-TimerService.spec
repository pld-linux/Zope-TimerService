
%define		zope_subname	TimerService
%define		module timerserver
Summary:	Support module for Zope-Scheduler
Summary(pl):	Modu³ wspomagaj±cy dla Zope-Scheduler
Name:		Zope-%{zope_subname}
Version:	0.2
Release:	4
License:	GPL
Group:		Libraries/Python
Source0:	http://dev.legco.biz/downloads/%{zope_subname}-%{version}.tar.gz
# Source0-md5:	5fb0fce2b90f69478a9370b313a45aa9
Source1:	Zope-timerserver_remover
URL:		http://dev.legco.biz/products/timerservice/
BuildRequires:  python
%pyrequires_eq	python-modules
Requires:	Zope
Requires:	perl-modules
Requires(post,postun):	/usr/sbin/installzopeproduct
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Support module for Zope-Scheduler.

%description -l pl
Modu³ wspomagaj±cy dla Zope-Scheduler.

%prep
%setup -q -c

%build
CFLAGS="%{rpmcflags}"
export CFLAGS
cd %{zope_subname}/timerserver
rm -rf .#*
python setup.py build_ext

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d $RPM_BUILD_ROOT%{py_sitedir}
install -d $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/Zope-timerserver_remover

cp -af %{zope_subname}/timerserver $RPM_BUILD_ROOT%{py_sitedir}/%{module}
cp -af %{zope_subname}/{zpt,*.py,version.txt} $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}/%{module}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/%{module}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/installzopeproduct %{_datadir}/%{name} %{zope_subname}

# ln -s %{py_sitedir}/%{module} /usr/lib/zope/lib/python/timerserver

echo "%import timerserver" >> /etc/zope/main/zope.conf
echo "<timer-server>" >> /etc/zope/main/zope.conf
echo "</timer-server>" >> /etc/zope/main/zope.conf

if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%preun
/usr/sbin/Zope-timerserver_remover

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/installzopeproduct -d %{zope_subname}
	if [ -f /var/lock/subsys/zope ]; then
		/etc/rc.d/init.d/zope restart >&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/Zope-timerserver_remover
%doc %{zope_subname}/{CREDITS.txt,INSTALL.txt}
%{_datadir}/%{name}
%{py_sitedir}/%{module}
