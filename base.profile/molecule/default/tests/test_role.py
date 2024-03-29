import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('pkg', [
    'vim', 'zsh', 'git', 'apt-transport-https', 'ca-certificates', 'gnupg2',
    'software-properties-common', 'curl', 'dnsutils', 'git', 'jq',
    'python-setuptools', 'sudo', 'vim', 'zsh', 'htop'
])
def test_pkg(host, pkg):
    package = host.package(pkg)
    assert package.is_installed


def test_root(host):
    user = host.user('root')
    ssh_keys = host.file("/root/.ssh/authorized_keys").content_string.split(
        '\n')

    assert user.exists
    assert user.shell == '/usr/bin/zsh'
    assert host.file(user.home + '/.oh-my-zsh').exists
    assert host.file(user.home + '/.zshrc').exists
    assert host.file(user.home + '/.zshrc').contains('ZSH_THEME="spaceship"')
    assert host.file(user.home +
                     '/.zshrc').contains('plugins=(git docker debian systemd)')
    assert len(list(filter(None, ssh_keys))) == 5


def test_usr_ubuntu(host):
    user = host.user('ubuntu')
    ssh_keys = host.file(
        "/home/ubuntu/.ssh/authorized_keys").content_string.split('\n')

    assert user.exists
    assert user.shell == '/usr/bin/zsh'
    assert 'sudo' not in user.groups
    assert host.file(user.home).exists
    assert host.file(user.home + '/.oh-my-zsh').exists
    assert host.file(user.home + '/.zshrc').exists
    assert host.file(user.home + '/.zshrc').contains('ZSH_THEME="agnoster"')
    assert host.file(user.home +
                     '/.zshrc').contains('plugins=(git docker debian systemd)')
    assert len(list(filter(None, ssh_keys))) == 5


def test_usr_debian(host):
    user = host.user('debian')
    ssh_keys = host.file(
        "/home/debian/.ssh/authorized_keys").content_string.split('\n')

    assert user.exists
    assert user.shell == '/usr/bin/zsh'
    assert 'sudo' in user.groups
    assert host.file(user.home).exists
    assert host.file(user.home + '/.oh-my-zsh').exists
    assert host.file(user.home + '/.zshrc').exists
    assert host.file(user.home + '/.zshrc').contains('ZSH_THEME="spaceship"')
    assert host.file(user.home + '/.zshrc').contains(
        'plugins=(git docker debian systemd sudo)')
    assert len(list(filter(None, ssh_keys))) == 4
