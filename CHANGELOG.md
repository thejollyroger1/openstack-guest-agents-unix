OpenStack-Guest-Agents-Unix CHANGELOG
=====================================


RELEASE: v1.39.0
-----------------

2013-12-31 AbhishekKr <abhikumar163@gmail.com>

> First of all, we are changing Release Versioning from [major[.minor[.maintenance[.build]]] to the [Semantic Versioning](http://semver.org/) model of [major[.minor[.patch]]] as is evident from our Release Tag.

This release contain several small steps towards stability across multiple distros:

* Hostname configuration fixed to not get reset on missing XenStore value
* FreeBSD installer corrected for Bash-dependencies
* resolvconf awareness support added for Ubuntu
* resolvconf awareness support added for FreeBSD
* Existing file's permission sustained for File Injection
* Gentoo made self-capable to clear sticky network configuration
* Ubuntu's forced Upstart network restart handled as failover
* lower level Functional Tests added for quick smoke
* some smaller dependency upgrades and/or fixes; and cleaning repo/code

***


RELEASE: v0.0.1.38
-----------------

2013-08-19 AbhishekKr <abhikumar163@gmail.com>

  * Fixed Tests, making 'make check' pass correctly
  * [pull/1] Fixed PYTHONPATH requirements for Gentoo init to enable usgae of System libraries as well
  * [pull/8] Better handling of static routes in debian/ubuntu
  * [pull/13] Making nova-agent log files secure by making limiting it's permission to owner only
  * [pull/22] SystemD support for ArchLinux
  * [pull/23] Gentoo Service Script updated to use depend() to look for 'before net' and 'after xe-daemon'
  * [pull/24] Gentoo Network updated to suit current Networking config. updates at Gentoo
  * [pull/26] Support for multi-architecture multi-lib wherever available using GCC --print-multiarch
  * Fixed PYTHONPATH and PYTHONHOME requirements at all-distro Service Script layers
  * Supports nova-agent bintar build at earlier Python 2.x minor version to run on newer Python 2.x minor version
  * Added "tools/nova-agent-builder.sh" to get the BINTAR created on all supported Distros.
  * Fixed BINTAR creation for FreeBSD, use the build script it takes care of it
  * Initiated adding automated functional tests.


***


RELEASE: v0.0.1.37
-----------------

2013-06-03 Chris Beherens <codestud@gmail.com>

  * The in-repo version was following normal SysV support and required some custom explicit patches over distro images.


***
