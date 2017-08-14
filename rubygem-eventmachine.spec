%global gem_name eventmachine

# This enables to run full test suite, where network connection is available.
# However, it must be disabled for Koji build.
%{!?network: %global network 0}

Summary:        Ruby/EventMachine library
Name:           rubygem-%{gem_name}
Version:        XXX
Release:        1%{?dist}
Group:          Development/Languages
License:        GPLv2 or Ruby
URL:            http://rubyeventmachine.com
Source0:        http://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby-devel
BuildRequires:  rubygem(test-unit)
# Enables SSL support.
BuildRequires:  openssl-devel

%if 0%{?rhel} > 0
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
EventMachine implements a fast, single-threaded engine for arbitrary network
communications. It's extremely easy to use in Ruby. EventMachine wraps all
interactions with IP sockets, allowing programs to concentrate on the
implementation of network protocols. It can be used to create both network
servers and clients. To create a server or client, a Ruby program only needs
to specify the IP address and port, and provide a Module that implements the
communications protocol. Implementations of several standard network protocols
are provided with the package, primarily to serve as examples. The real goal
of EventMachine is to enable programs to easily interface with other programs
using TCP/IP, especially if custom protocols are required.

%package doc
Summary: Documentation for %{name}
Group: Documentation
BuildArch: noarch

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.


%prep
%setup -q -T -c
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%if 0%{?fedora} > 0
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/
%endif

%if 0%{?rhel} >= 7
mkdir -p %{buildroot}%{gem_extdir_mri}/lib
cp -ar .%{gem_instdir}/lib/* %{buildroot}%{gem_extdir_mri}/lib
%endif

# Prevent dangling symlink in -debuginfo.
rm -rf %{buildroot}%{gem_instdir}/ext

%check
pushd .%{gem_instdir}

# test_localhost(TestResolver) fails.
# https://github.com/eventmachine/eventmachine/issues/579
sed -i '/test_localhost/,/^  end$/ s/^/#/' tests/test_resolver.rb
# test_dispatch_completion(TestThreadedResource) fails randomly.
# https://github.com/eventmachine/eventmachine/issues/575
sed -i '/test_dispatch_completion/,/^  end$/ s/^/#/' tests/test_threaded_resource.rb

# Unfortunatelly test_a exists in more test cases.
ruby -Ilib:$(dirs +1)%{gem_extdir_mri}:.:tests -e "Dir.glob 'tests/test_*.rb', &method(:require)" -- \
%if 0%{network} < 1
  --ignore-name=/^test_bind_connect$/ \
  --ignore-name=/^test_get_sock_opt$/ \
  --ignore-name=/^test_cookie$/ \
  --ignore-name=/^test_http_client$/ \
  --ignore-name=/^test_http_client_1$/ \
  --ignore-name=/^test_http_client_2$/ \
  --ignore-name=/^test_version_1_0$/ \
  --ignore-name=/^test_get$/ \
  --ignore-name=/^test_get_pipeline$/ \
  --ignore-name=/^test_https_get$/ \
  --ignore-name=/^test_idle_time$/ \
  --ignore-name=/^test_a$/ \
  --ignore-name=/^test_a_pair$/ \
  --ignore-name=/^test_bad_host$/ \
  --ignore-name=/^test_failure_timer_cleanup$/ \
  --ignore-name=/^test_timer_cleanup$/ \
  --ignore-name=/^test_set_sock_opt$/ \
  --ignore-name=/^test_connect_timeout$/ \
  --ignore-name=/^test_for_real$/ \
  --ignore-name=/^test_nameserver/ \
  --ignore-name=/^test_fork_reactor$/
%endif

popd

%files
%doc %{gem_instdir}/GNU
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}/
%exclude %{gem_instdir}/.*
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/docs
%{gem_instdir}/examples
# TODO: Hmm, we can build also JRuby bindigs.
%{gem_instdir}/java
%{gem_instdir}/rakelib
%{gem_instdir}/tests

%changelog
