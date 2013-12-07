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

%bcond_with	readline
%define gcj_support	0
%define section		free

Summary:	Java wrapper for the GNU-readline library
Name:		libreadline-java
Version:	0.8.1
Release:	6
License:	LGPLv2
Group:		Development/Java
Url:		http://java-readline.sourceforge.net/
Source0:	http://download.sourceforge.net/java-readline/libreadline-java-%{version}-src.tar.gz
Patch0:		libreadline-java-0.8.1-build-against-libncursesw.patch

BuildRequires:	java-rpmbuild >= 0:1.6
%if %with readline
BuildRequires:	readline-devel
%else
BuildRequires:	pkgconfig(libedit)
%endif
BuildRequires:	pkgconfig(ncursesw)
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildRequires:	java-devel >= 0:1.4.2
%endif
Provides:	java_readline = %{EVRD}
Provides:	gnu.readline = %{EVRD}

%description
Java-Readline is a port of GNU Readline for Java. Or, to be more 
precise, it is a JNI-wrapper to Readline. It is distributed under 
the LGPL.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%apply_patches
find . -type d -name CVS | xargs -t rm -r
find . -type f -name "*.dll" | xargs -t rm
sed -i -e 's|javadoc |%{javadoc} |g;' \
	-e 's|jar -c|%{jar} -c|g;' \
	Makefile

%build
export JAVA_HOME=%{java_home}
%make \
%if %with readline
	T_LIBS=JavaReadline \
%else
	T_LIBS=JavaEditline \
%endif
	JAVAC=%{javac} \
	JC_FLAGS="" \
	LIBPATH="-L%{_libdir}" \
	CFLAGS="-DPOSIX %{optflags}" \
	LD_FLAGS="-shared %{ldflags}"
%make apidoc

%install
# jar
mkdir -p %{buildroot}%{_jnidir}
install -m 644 %{name}.jar %{buildroot}%{_jnidir}/%{name}-%{version}.jar
(cd %{buildroot}%{_jnidir} && for jar in *-%{version}*; do \
%{__ln_s} ${jar} ${jar/-%{version}/}; done)
# lib
mkdir -p %{buildroot}%{_libdir}
%if %with readline
install -m 755 libJavaReadline.so %{buildroot}%{_libdir}/libJavaReadline.so
%else
install -m 755 libJavaEditline.so %{buildroot}%{_libdir}/libJavaEditline.so
%endif

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%if %{gcj_support}
aot-compile-rpm
%endif

%files
%doc COPYING.LIB NEWS README README.1st TODO VERSION contrib
%{_libdir}/*.so
%{_jnidir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

