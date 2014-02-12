#!/usr/bin/env csh

#####################################################################
# source: https://github.com/abhishekkr/raguel/blob/master/src/configurator/distro_manager.sh
#####
# check for Distro Mother and load for Info & Commands

set uname_s = `uname -s`
set uname_n = `uname -n`
set uname_m = `uname -m`

if (-f /etc/redhat-release) then
  set RAGUEL_DISTRO_TYPE = 'rhel'
  set RAGUEL_PACKAGE_INSTALL = 'yum install -y '
  set RAGUEL_PACKAGE_UNINSTALL = 'yum erase -y '
else if (-f /etc/debian_version) then
  set RAGUEL_DISTRO_TYPE = 'debian'
  set RAGUEL_PACKAGE_INSTALL = 'apt-get -y install '
  set RAGUEL_PACKAGE_UNINSTALL = 'apt-get -y remove '
else if (-f /etc/gentoo-release) then
  set RAGUEL_DISTRO_TYPE = 'gentoo'
  set RAGUEL_PACKAGE_INSTALL = 'emerge '
  set RAGUEL_PACKAGE_UNINSTALL = 'emerge --depclean '
else if (-f /etc/arch-release) then
  set RAGUEL_DISTRO_TYPE = 'arch'
  set RAGUEL_PACKAGE_INSTALL = 'pacman -Sy --noconfirm '
  set RAGUEL_PACKAGE_UNINSTALL = 'pacman -R --noconfirm '
else if ($uname_s == 'FreeBSD')  then
  set RAGUEL_DISTRO_TYPE = 'bsd'
  set RAGUEL_PACKAGE_INSTALL = 'pkg_add -r  '
  set RAGUEL_PACKAGE_UNINSTALL = 'pkg_deinstall --preserve '
else if (-f /etc/SuSE-release)  then
  set RAGUEL_DISTRO_TYPE = 'slackware'
  set RAGUEL_PACKAGE_INSTALL = 'zypper install -y '
  set RAGUEL_PACKAGE_UNINSTALL = 'zypper remove -y '
else
  echo "Raguel is not able to find signature of this Distro."
  exit 1
endif

set RAGUEL_NODENAME = $uname_n
set RAGUEL_ARCH = $uname_m

#####################################################################

foreach pkg ($*)
  echo "installing package: ${pkg}"
  `$RAGUEL_PACKAGE_INSTALL $pkg`
end
