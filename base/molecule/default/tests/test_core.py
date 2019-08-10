import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('pkg', [
    'vim', 'zsh', 'git', 'apt-transport-https', 'ca-certificates', 'gnupg2',
    'software-properties-common', 'curl', 'dnsutils', 'git', 'iptables', 'jq',
    'python-setuptools', 'sudo', 'vim', 'zsh', 'htop'
])
def test_pkg(host, pkg):
    package = host.package(pkg)
    assert package.is_installed


@pytest.mark.parametrize('usr', ['ubuntu', 'debian'])
def test_usr(host, usr):
    user = host.user(usr)

    assert user.exists
    assert 'sudo' in user.groups
    assert host.file(user.home).exists
    assert user.shell == '/usr/bin/zsh'
