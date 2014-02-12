## nova-agent's Tester

It's a libcloud and fabric based utility to create an instance for each supported image type.

Then prepare BINTARs on CentOS and FreeBSD.

Update nova-agent to newly created BINTAR on all the created test nodes.

Then run the nova-agent functionality test scripts on all those test-nodes.

And all this by just running...

```Shell

fab create_update_test:./cloud.cfg

```

here "./cloud.cfg" need to hold the credential details for your account

To destroy all nodes created and used for tests, run

```

fab destroy_nodes:./cloud.cfg

```

To see what all different tasks Fabric can do using it, run

```Shell

fab -l

```

---

[W.I.P.]

* The test-script currently require Python2.6+. Because some old images can't be upgraded to it the test will need to be made backward compatible.
* refactor nova-agent testing to a pluggable arch. to ease-up cloud-init adaptation

---
