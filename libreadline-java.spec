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
%define gcj_support     1
%define section         free

Name:           libreadline-java
Version:        0.8.1
Release:        %mkrel 1.4
Epoch:          0
Summary:        Java wrapper for the GNU-readline library
License:        LGPL
URL:            http://java-readline.sourceforge.net/
Source0:        http://download.sourceforge.net/java-readline/libreadline-java-%{version}-src.tar.gz
BuildRequires:  jpackage-utils >= 0:1.6
%if %with readline
BuildRequires:  libreadline-devel
%else
BuildRequires:  edit-devel
%endif
BuildRequires:  libtermcap-devel
Provides:       java_readline = %{epoch}-%{version}-%{release}
Provides:       gnu.readline = %{epoch}-%{version}-%{release}
Group:          Development/Java
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
%{__cp} -a api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

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


