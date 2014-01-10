## nova-agent's Tester

[W.I.P.]

It's a libcloud and fabric based utility to create an instance for each supported image type.

Then prepare BINTARs on CentOS and FreeBSD.

Update nova-agent to newly created BINTAR on all the created test nodes.

Then run the nova-agent functionality test scripts on all those test-nodes.

And all this by just running...

```Shell

./tester.py cloud.cfg

```
