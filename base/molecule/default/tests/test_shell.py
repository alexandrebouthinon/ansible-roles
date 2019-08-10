import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('usr', ['ubuntu', 'debian'])
def test_user_files(host, usr):
    user = host.user(usr)
    assert host.file(user.home).exists
    assert host.file(user.home + '/.oh-my-zsh').exists
    assert host.file(user.home + '/.zshrc').exists
    assert host.file(user.home + '/.zshrc').contains('ZSH_THEME="spaceship"')
    assert host.file(user.home +
                     '/.zshrc').contains('plugins=(git docker debian systemd)')
