import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('pkg', ['docker-ce'])
def test_pkg(host, pkg):
    package = host.package(pkg)
    assert package.is_installed
    assert host.file('/usr/local/bin/docker-compose').exists


@pytest.mark.parametrize('usr', ['ubuntu', 'debian'])
def test_usr(host, usr):
    user = host.user(usr)
    assert 'docker' in user.groups


@pytest.mark.parametrize('svc', ['docker'])
def test_svc(host, svc):
    service = host.service(svc)
    assert service.is_enabled
    assert service.is_running
