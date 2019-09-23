import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_ouroboros_service(host):
    service = host.service('ouroboros')
    container = host.docker('ouroboros')
    assert service.is_enabled
    assert container.is_running
