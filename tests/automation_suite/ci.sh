#!bash
#####
# $ ./ci.sh <distro_type>
# $ ./ci.sh <distro_type> <branch>
# on specifying branch, distro is mandatory
# distro effect only differs if value send is "bsd"
#####

if [ "$1" == "" ]; then
  DISTRO="rhel,deb,gentoo,arch,suse"
else
  DISTRO="$1"
fi

if [ "$2" == "" ]; then
  NOVA_AGENT_BRANCH="master"
else
  NOVA_AGENT_BRANCH="$2"
fi

NOVA_AGENT_TEST_BASEDIR="/tmp/nova-agent-test-runner/${NOVA_AGENT_BRANCH}"
NOVA_AGENT_LOCAL_BASE="/tmp/nova-agent/${NOVA_AGENT_BRANCH}"
mkdir -p "${NOVA_AGENT_TEST_BASEDIR}/tools"
mkdir -p $NOVA_AGENT_LOCAL_BASE

RELEASE_TAG=`curl -skL https://api.github.com/repos/rackerlabs/openstack-guest-agents-unix/tags | grep '"name":' | head -1 | awk -F'"' '{print $4}' | sed 's/^v//'`
cd $NOVA_AGENT_LOCAL_BASE
if [ $DISTRO == 'bsd' ]; then
  curl -C - -sLkO "https://github.com/rackerlabs/openstack-guest-agents-unix/releases/download/v${RELEASE_TAG}/nova-agent-FreeBSD-amd64-${RELEASE_TAG}.tar.gz"
else
  curl -C - -sLkO "https://github.com/rackerlabs/openstack-guest-agents-unix/releases/download/v${RELEASE_TAG}/nova-agent-Linux-x86_64-${RELEASE_TAG}.tar.gz"
fi
curl -C - -sLkO "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/tools/install_prerequisite.sh"
curl -C - -sLkO "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/tools/install_agent.py"
curl -C - -sLkO "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/agent_tester.py"
cd $NOVA_AGENT_TEST_BASEDIR

echo "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/agent_test_runner.py"
curl -C - -sLk -o "${NOVA_AGENT_TEST_BASEDIR}/agent_test_runner.py" "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/agent_test_runner.py"
touch "${NOVA_AGENT_TEST_BASEDIR}/tools/__init__.py"
curl -C - -sLk -o "${NOVA_AGENT_TEST_BASEDIR}/tools/server_creator.py" "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/tools/server_creator.py"

IF_FAB=`which fab > /dev/null ; echo $?`
IF_PIP=`which pip > /dev/null ; echo $?`
IF_EASYINSTALL=`which easy_install > /dev/null ; echo $?`
if [[ $IF_FAB == '1' ]]; then
  if [[ $IF_PIP != '1' ]]; then
    pip install fabric
  elif [[ $IF_EASYINSTALL != '1' ]]; then
    easy_install pip
    pip install fabric
  else
    echo "Install 'Fabric' python module. No pip or easy_install found."
    exit 127
  fi
fi

cd $NOVA_AGENT_TEST_BASEDIR
python "./agent_test_runner.py"
