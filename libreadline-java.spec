# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%bcond_with             readline
%define gcj_support     0
%define section         free

Name:           libreadline-java
Version:        0.8.1
Release:        3
Epoch:          0
Summary:        Java wrapper for the GNU-readline library
License:        LGPL
URL:            http://java-readline.sourceforge.net/
Source0:        http://download.sourceforge.net/java-readline/libreadline-java-%{version}-src.tar.gz
Patch0:		libreadline-java-0.8.1-build-against-libncursesw.patch
BuildRequires:  java-rpmbuild >= 0:1.6
%if %with readline
BuildRequires:  readline-devel
%else
BuildRequires:  edit-devel
%endif
BuildRequires:  pkgconfig(ncursesw)
Provides:       java_readline = %{epoch}:%{version}-%{release}
Provides:       gnu.readline = %{epoch}:%{version}-%{release}
Group:          Development/Java
#Distribution:  JPackage
#Vendor:        JPackage Project
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel >= 0:1.4.2
%endif

%description
Java-Readline is a port of GNU Readline for Java. Or, to be more 
precise, it is a JNI-wrapper to Readline. It is distributed under 
the LGPL.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch0 -p1 -b .ncurses~
%{_bindir}/find . -type d -name CVS | %{_bindir}/xargs -t %{__rm} -r
%{_bindir}/find . -type f -name "*.dll" | %{_bindir}/xargs -t %{__rm}
%{__perl} -pi -e 's|javadoc |%{javadoc} |g;' \
              -e 's|jar -c|%{jar} -c|g;' \
  Makefile

%build
export JAVA_HOME=%{java_home}
%if %with readline
%{__make} T_LIBS=JavaReadline JAVAC=%{javac} JC_FLAGS="" LIBPATH="-L%{_libdir}"
%else
%{__make} T_LIBS=JavaEditline JAVAC=%{javac} JC_FLAGS="" LIBPATH="-L%{_libdir}"
%endif
%{__make} apidoc

%install
%{__rm} -rf %{buildroot}
# jar
%{__mkdir_p} %{buildroot}%{_jnidir}
%{__install} -m 644 %{name}.jar %{buildroot}%{_jnidir}/%{name}-%{version}.jar
(cd %{buildroot}%{_jnidir} && for jar in *-%{version}*; do \
%{__ln_s} ${jar} ${jar/-%{version}/}; done)
# lib
%{__mkdir_p} %{buildroot}%{_libdir}
%if %with readline
%{__install} -m 755 libJavaReadline.so %{buildroot}%{_libdir}/libJavaReadline.so
%else
%{__install} -m 755 libJavaEditline.so %{buildroot}%{_libdir}/libJavaEditline.so
%endif

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%files
%defattr(0644,root,root,0755)
%doc COPYING.LIB NEWS README README.1st TODO VERSION contrib
%attr(0755,root,root) %{_libdir}/*.so
%{_jnidir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}




%changelog
* Sun Nov 28 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.8.1-1.8mdv2011.0
+ Revision: 602601
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.8.1-1.7mdv2010.1
+ Revision: 520899
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:0.8.1-1.6mdv2010.0
+ Revision: 425696
- rebuild

* Mon Jun 09 2008 Pixel <pixel@mandriva.com> 0:0.8.1-1.5mdv2009.0
+ Revision: 217191
- do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:0.8.1-1.5mdv2008.1
+ Revision: 120972
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:0.8.1-1.4mdv2008.0
+ Revision: 87248
- fix buildrequires
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

  + Thierry Vignaud <tv@mandriva.org>
    - kill ldconfig require as requested by pixel

* Wed Jul 04 2007 David Walluck <walluck@mandriva.org> 0:0.8.1-1.3mdv2008.0
+ Revision: 48242
- don't ship binary win32 .dll

* Wed Jul 04 2007 David Walluck <walluck@mandriva.org> 0:0.8.1-1.2mdv2008.0
+ Revision: 48239
- lib should be unversioned and mode 0755


* Thu Mar 15 2007 David Walluck <walluck@mandriva.org> 0.8.1-1.1mdv2007.1
+ Revision: 144079
- 0.8.1 (CVS)

* Mon Mar 12 2007 David Walluck <walluck@mandriva.org> 0:0.8.0-11.2mdv2007.1
+ Revision: 142055
- add gcj support
  add unversioned javadoc directory
- Import libreadline-java

* Sun Mar 11 2007 David Walluck <walluck@mandriav.org> 0:0.8.0-11.1mdv2007.1
- release

* Sat May 27 2006 Ralph Apel <r.apel@r-apel.de> 0:0.8.0-11jpp
- First JPP-1.7 release

* Wed Nov 09 2005 Fernando Nasser <fnasser@redhat.com> 0:0.8.0-10jpp
- Rebuild for readline 5.0

* Wed Mar 30 2005 David Walluck <david@jpackage.org> 0:0.8.0-9jpp
- fix duplicate files in file list
- set java bins in path

* Tue Nov 02 2004 Nicolas Mailhot <nim@jpackage.org> -  0:0.8.0-8jpp
- Move jars into %%{_jnidir}

* Tue Nov 02 2004 Nicolas Mailhot <nim@jpackage.org> -  0:0.8.0-7jpp
- Replace build dep on termcap-devel with dep on %%{_libdir}/libtermcap.so
  (needed on RH/FC systems)

* Sun Oct 10 2004 David Walluck <david@jpackage.org> 0:0.8.0-6jpp
- rebuild for JPackage 1.5 devel

