#!bash
#####
## SWITCH passing here will changed to FLAG instead of INDEX(current)
# $ ./ci.sh # picks defaults: /etc/nova-agent.cfg for Linux off master branch
# # picks given NOVA_AGENT_CFG
# # and defaults to distro:Debian7, branch:master, env:prod
# # $ ./ci.sh <path-to-cfg>
#
# # picks given NOVA_AGENT_CFG and NOVA_AGENT_DISTRO
# # and defaults to branch:master, env:prod
# $ ./ci.sh <path-to-cfg> <distro_type>
#
# # picks given NOVA_AGENT_CFG and NOVA_AGENT_DISTRO and NOVA_AGENT_BRANCH
# # and defaults to env:prod
# $ ./ci.sh <path-to-cfg> <distro_type> <branch>
#
# # picks given NOVA_AGENT_CFG and NOVA_AGENT_DISTRO and NOVA_AGENT_BRANCH and NOVA_AGENT_ENV_NAME
# $ ./ci.sh <path-to-cfg> <distro_type> <branch> <rax_env>
# on specifying branch, distro is mandatory
# distro effect only differs if value send is "bsd"
#####

if [ "$1" == "" ]; then
  NOVA_AGENT_CFG="/etc/nova-agent.cfg"
else
  NOVA_AGENT_CFG="$1"
fi

if [ "$2" == "" ]; then
  NOVA_AGENT_DISTRO="Debian7"
else
  NOVA_AGENT_DISTRO="$2"
fi

if [ "$3" == "" ]; then
  NOVA_AGENT_BRANCH="master"
else
  NOVA_AGENT_BRANCH="$3"
fi

if [ "$4" == "" ]; then
  NOVA_AGENT_ENV_NAME="prod"
else
  NOVA_AGENT_ENV_NAME="$4"
fi

NOVA_AGENT_LOCAL_BASE="/tmp/nova-agent/${NOVA_AGENT_BRANCH}"
NOVA_AGENT_TEST_BASEDIR="/tmp/nova-agent-test-runner/${NOVA_AGENT_BRANCH}"
mkdir -p $NOVA_AGENT_LOCAL_BASE
mkdir -p "${NOVA_AGENT_TEST_BASEDIR}/tools"
cp -f $NOVA_AGENT_CFG "${NOVA_AGENT_TEST_BASEDIR}/tools/server_configurations.cfg"

RELEASE_TAG=`curl -skL https://api.github.com/repos/rackerlabs/openstack-guest-agents-unix/tags | grep '"name":' | head -1 | awk -F'"' '{print $4}' | sed 's/^v//'`

if [ `which wget > /dev/null ; echo $?` == "0" ]; then
  export NOVA_AGENT_DOWNLOADER="wget -c"
elif [ `which curl > /dev/null ; echo $?` == "0" ]; then
  export NOVA_AGENT_DOWNLOADER="curl -skLO"
else
  echo "ERROR: Curl/Wget not found." ; exit 127
fi

cd $NOVA_AGENT_LOCAL_BASE
if [ $NOVA_AGENT_DISTRO == 'FreeBSD' ]; then
  $NOVA_AGENT_DOWNLOADER "https://github.com/rackerlabs/openstack-guest-agents-unix/releases/download/v${RELEASE_TAG}/nova-agent-FreeBSD-amd64-${RELEASE_TAG}.tar.gz"
else
  $NOVA_AGENT_DOWNLOADER "https://github.com/rackerlabs/openstack-guest-agents-unix/releases/download/v${RELEASE_TAG}/nova-agent-Linux-x86_64-${RELEASE_TAG}.tar.gz"
fi
$NOVA_AGENT_DOWNLOADER "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/tools/install_prerequisite.sh"
$NOVA_AGENT_DOWNLOADER "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/tools/install_agent.py"
$NOVA_AGENT_DOWNLOADER "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/agent_tester.py"

cd $NOVA_AGENT_TEST_BASEDIR
$NOVA_AGENT_DOWNLOADER "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/agent_test_runner.py"
cd "${NOVA_AGENT_TEST_BASEDIR}/tools"
$NOVA_AGENT_DOWNLOADER "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/tools/__init__.py"
$NOVA_AGENT_DOWNLOADER "https://raw.github.com/rackerlabs/openstack-guest-agents-unix/${NOVA_AGENT_BRANCH}/tests/automation_suite/tools/server_creator.py"

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
NOVA_AGENT_ENV_NAME="${NOVA_AGENT_ENV_NAME}" NOVA_AGENT_DISTRO="${NOVA_AGENT_DISTRO}" NOVA_AGENT_BRANCH="${NOVA_AGENT_BRANCH}" NOVA_AGENT_CONFIGURATION="${NOVA_AGENT_TEST_BASEDIR}/tools/server_configurations.cfg" python "./agent_test_runner.py"
