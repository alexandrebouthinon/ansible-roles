import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pip_pkgs(host):
    pip_packages = host.pip_package.get_packages(pip_path='pip3')
    assert 'ouroboros-cli' in pip_packages


def test_ouroboros_service(host):
    service = host.service('ouroboros')
    assert service.is_running
    assert service.is_enabled
