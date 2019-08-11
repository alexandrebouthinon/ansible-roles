import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pkg(host):
    package = host.package('docker-ce')
    assert package.is_installed
    assert host.file('/usr/local/bin/docker-compose').exists


def test_usr(host):
    assert 'docker' in host.user('debian').groups
    assert 'docker' not in host.user('ubuntu').groups


def test_docker_svc(host):
    service = host.service('docker')
    assert service.is_enabled
    assert service.is_running
