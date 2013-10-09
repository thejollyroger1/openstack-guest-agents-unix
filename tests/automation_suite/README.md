### Usage

```Shell
CI_SUITE_CONF="/tmp/test_nova_agent/server_configurations.cfg"
NOVA_AGENT_BRANCH="createserver-mod"
IMAGE_NAME=CentOS64
RAXENV_NAME=prod

bash ci.sh $CI_SUITE_CONF $NOVA_AGENT_BRANCH $IMAGE_NAME $RAXENV_NAME
```

A Demo Server Config file can be referred [here](https://github.com/rackerlabs/openstack-guest-agents-unix/blob/ci_suite/tests/automation_suite/server_configurations.cfg.sample)
