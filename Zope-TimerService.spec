
%define		zope_subname	TimerService
%define		module timerserver
Summary:	Support module for Zope-Scheduler
Summary(pl.UTF-8):   Moduł wspomagający dla Zope-Scheduler
Name:		Zope-%{zope_subname}
Version:	0.2
Release:	4
License:	GPL
Group:		Libraries/Python
Source0:	http://dev.legco.biz/downloads/%{zope_subname}-%{version}.tar.gz
# Source0-md5:	5fb0fce2b90f69478a9370b313a45aa9
Source1:	Zope-timerserver_remover
URL:		http://dev.legco.biz/products/timerservice/
BuildRequires:	python
BuildRequires:	rpmbuild(macros) >= 1.268
%pyrequires_eq	python-modules
Requires(post,postun):	/usr/sbin/installzopeproduct
Requires:	Zope
Requires:	perl-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Support module for Zope-Scheduler.

%description -l pl.UTF-8
Moduł wspomagający dla Zope-Scheduler.

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

# ln -s %{py_sitedir}/%{module} %{_prefix}/lib/zope/lib/python/timerserver
if [ "$1" = 1 ]; then
	echo "%import timerserver" >> /etc/zope/main/zope.conf
	echo "<timer-server>" >> /etc/zope/main/zope.conf
	echo "</timer-server>" >> /etc/zope/main/zope.conf
fi

%service -q zope restart

%preun
/usr/sbin/Zope-timerserver_remover

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/installzopeproduct -d %{zope_subname}
	%service -q zope restart
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/Zope-timerserver_remover
%doc %{zope_subname}/{CREDITS.txt,INSTALL.txt}
%{_datadir}/%{name}
%{py_sitedir}/%{module}
