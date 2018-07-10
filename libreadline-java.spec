%{?_javapackages_macros:%_javapackages_macros}
%global editline_ver    2.9
%global src_dirs        org test

%if 0%{?fedora}
%else
# Force same version as in fedora...
Epoch:         1
%endif
Name:          libreadline-java
Version:       0.8.0
Release:       37.3
Summary:       Java wrapper for the EditLine library
Group:		Development/Java
License:       LGPLv2+
URL:           http://java-readline.sf.net/
Source0:       http://download.sf.net/java-readline/%{name}-%{version}-src.tar.gz
Source1:       %{name}-%{version}-pom.xml
Patch0:        %{name}-ncurses.patch
Patch1:        %{name}-libdir.patch

BuildRequires: jpackage-utils >= 1.5
BuildRequires: libedit-devel >= %{editline_ver}
BuildRequires: ncurses-devel
BuildRequires: java-devel >= 1.4.2

%if 0%{?fedora}
Requires:      libedit >= %{editline_ver}
%else
%define libedit %mklibname edit 0
Requires:      %{libedit} >= %{editline_ver}
%endif
Requires:      java >= 1.4.2

%description
libreadline-java provides Java bindings for libedit though a JNI
wrapper.

%package javadoc
Summary:   Javadoc for %{name}
BuildArch: noarch

%description javadoc
API documentation for %{name}.

%prep
%setup -q
%patch0
%patch1
sed -i 's|@LIBDIR@|%{_libdir}|' src/org/gnu/readline/Readline.java

%build
export JAVA_HOME=%{java_home}
export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
make CFLAGS="$RPM_OPT_FLAGS -fPIC -DPOSIX" T_LIBS=JavaEditline
make apidoc

# fix debuginfo package
rm -f %{src_dirs}
for dir in %{src_dirs}
do
  ln -s src/$dir
done

%install

# install jar file and JNI library under %{_libdir}/%{name}
# FIXME: fix jpackage-utils to handle multilib correctly
mkdir -p %{buildroot}%{_libdir}/%{name}
install -m 755 libJavaEditline.so %{buildroot}%{_libdir}/%{name}

mkdir -p %{buildroot}%{_jnidir}
install -pm 644 %{name}.jar %{buildroot}%{_jnidir}/%{name}.jar
ln -sf ../java/%{name}.jar %{buildroot}%{_libdir}/%{name}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -a api/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc ChangeLog NEWS README README.1st VERSION COPYING.LIB
%dir %{_libdir}/%{name}
%attr(-,root,root) %{_libdir}/%{name}/*
%{_jnidir}/*

%pre javadoc
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files javadoc
%{_javadocdir}/%{name}
%doc COPYING.LIB

%changelog
* Tue Aug 06 2013 gil cattaneo <puntogil@libero.it> 0.8.0-33
- add maven pom
- add %%pre javadoc script
- minor changes to adapt to current guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Alexander Kurtakov <akurtako@redhat.com> 0.8.0-27
- Drop gcj.
- Adapt to current guidelines.

* Fri Jan 15 2010 Andrew Overholt <overholt@redhat.com> 0.8.0-26
- Fix License

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0.8.0-25
- Add Public Domain to License

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 14 2008 David Walluck <dwalluck@redhat.com> 0.8.0-22
- add unversioned javadoc symlink
- remove unnecessary gcc-java requirement
- fix permissions

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.0-21
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8.0-20
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.8.0-19
- Rebuild for selinux ppc32 issue.

* Thu Jul  5 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.8.0-18
- Specify full path to libedit backing library.
- Default to libedit backing library.
- Satisfy termcap requirements with ncurses.
- Resolves: rhbz#231209

* Mon Mar 26 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.8.0-17
- Honor $RPM_OPT_FLAGS.

* Mon Mar 26 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.8.0-16
- Install jar file and JNI library under libdir.
- Group BuildRequires and Requires.
- Eliminate devel subpackage.
- Remove ldconfig requirements.
- Reformat.

* Fri Mar 23 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.8.0-15
- Fix libJavaEditline.so symlink typo.

* Fri Mar 23 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.8.0-14
- Rebuild against unorphaned libedit.

* Fri Sep 08 2006 Igor Foox <ifoox@redhat.com> 0.8.0-13
- Changed summary and description to describe the change to editline.

* Fri Sep 08 2006 Igor Foox <ifoox@redhat.com> 0.8.0-12
- Remove dependency on readline and readline-devel.
- Add dependency on libedit{,-devel}, change make argument to JavaEditline
  from JavaReadline.

* Fri Sep 08 2006 Igor Foox <ifoox@redhat.com> 0.8.0-11
- Doubled percent signs in changelog section.
- Fixed dependency on readline to be >= instead of =.
- Move jar to %%{_javadir} from %%{_jnidir}
- Added dist tag.
- Added COPYING.LIB to doc files.

* Mon Jun 26 2006 Igor Foox <ifoox@redhat.com> 0.8.0-10jpp_3fc
- Moved the unversioned .so file into a -devel package 
- Changed Group of the -javadoc package to Development/Libraries

* Fri Jun 23 2006 Igor Foox <ifoox@redhat.com> 0.8.0-10jpp_2fc
- Remove Vendor and Distribution tags
- Change group to Development/Libraries
- Removed Epoch, and Epoch in Requires for libreadline
- Added (post) and (postun) to Requires of /sbin/ldconfig
- Changed Source0 to use the version and name macros
- Fixed debuginfo package

* Wed May 31 2006 Igor Foox <ifoox@redhat.com> 0:0.8.0-10jpp_1fc
- Natively compile
- Changed BuildRoot to what Extras expects

* Wed Nov 09 2005 Fernando Nasser <fnasser@redhat.com> 0:0.8.0-10jpp
- Rebuild for readline 5.0

* Tue Mar 29 2005 David Walluck <david@jpackage.org> 0:0.8.0-9jpp
- fix duplicate files in file list
- set java bins in path

* Tue Nov 2 2004 Nicolas Mailhot <nim@jpackage.org> -  0:0.8.0-8jpp
- Move jars into %%{_jnidir}

* Tue Nov 2 2004 Nicolas Mailhot <nim@jpackage.org> -  0:0.8.0-7jpp
- Replace build dep on termcap-devel with dep on %%{_libdir}/libtermcap.so
  (needed on RH/FC systems)

* Sat Oct 09 2004 David Walluck <david@jpackage.org> 0:0.8.0-6jpp
- rebuild for JPackage 1.5 devel

* Thu Jan 30 2003 David Walluck <david@anti-microsoft.org> 0:0.8.0-5jpp
- rebuild for JPackage 1.5

* Thu Jan 30 2003 David Walluck <david@anti-microsoft.org> 0.8.0-4jpp
- AutoReqProvides: no
- Strict requires on readline version and /sbin/ldconfig

* Sun Jan 26 2003 David Walluck <david@anti-microsoft.org> 0.8.0-3jpp
- set JAVA_HOME/bin in PATH

* Wed Jan 22 2003 David Walluck <david@anti-microsoft.org> 0.8.0-2jpp
- 1jpp was missing %%changelog
