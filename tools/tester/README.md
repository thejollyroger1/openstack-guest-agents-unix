## nova-agent's Tester

[W.I.P.]

Broken Support for: FreeBSD, Gentoo, OpenSUSE (issue with: Fabric)

* The test-script currently require Python2.6+. Because some old images can't be upgraded to it the test will need to be made backward compatible.
* install_package() need to be fixed for any distro which doesn't have Python already (only FreeBSD for now)
* refactor nova-agent testing to a pluggable arch. to ease-up cloud-init adaptation

---

It's a libcloud and fabric based utility to create an instance for each supported image type.

Then prepare BINTARs on CentOS and FreeBSD.

Update nova-agent to newly created BINTAR on all the created test nodes.

Then run the nova-agent functionality test scripts on all those test-nodes.

And all this by just running...

```Shell

./tester.py cloud.cfg

```
