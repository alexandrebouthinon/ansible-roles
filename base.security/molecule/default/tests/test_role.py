import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

rules = [
    'iptables -t nat -I PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 443',
    'iptables -t nat -I OUTPUT -p tcp -o lo --dport 80 -j REDIRECT --to-port 443',
    'iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT',
    'iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT',
    'iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT',
    'iptables -A INPUT -m limit --limit 15/minute -j LOG --log-level 7 --log-prefix "Dropped by firewall: "'
]

jails = {
    'sshd': [
        '[sshd]', 'enabled = true', 'port = ssh', 'filter = sshd',
        'findtime = 600', 'maxretry = 5', 'bantime = 3600'
    ]
}

kernel_opts = [
    'kernel.sysrq = 0', 'kernel.core_uses_pid = 1', 'net.ipv4.ip_forward = 0',
    'net.ipv4.tcp_syncookies = 1', 'net.ipv4.tcp_synack_retries = 5',
    'net.ipv4.conf.all.send_redirects = 0',
    'net.ipv4.conf.default.send_redirects = 0',
    'net.ipv4.conf.all.accept_source_route = 0',
    'net.ipv4.conf.all.accept_redirects = 0',
    'net.ipv4.conf.all.secure_redirects = 0',
    'net.ipv4.conf.all.log_martians = 1',
    'net.ipv4.conf.default.accept_source_route = 0',
    'net.ipv4.conf.default.accept_redirects = 0',
    'net.ipv4.conf.default.secure_redirects = 0',
    'net.ipv4.icmp_echo_ignore_broadcasts = 1',
    'net.ipv4.conf.all.rp_filter = 1', 'net.ipv4.conf.default.rp_filter = 1',
    'net.ipv6.conf.default.router_solicitations = 0',
    'net.ipv6.conf.default.accept_ra_rtr_pref = 0',
    'net.ipv6.conf.default.accept_ra_pinfo = 0',
    'net.ipv6.conf.default.accept_ra_defrtr = 0',
    'net.ipv6.conf.default.autoconf = 0',
    'net.ipv6.conf.default.dad_transmits = 0',
    'net.ipv6.conf.default.max_addresses = 1', 'fs.file-max = 65535',
    'kernel.pid_max = 65536', 'net.ipv4.ip_local_port_range = 2000 65000',
    'net.ipv4.tcp_rfc1337 = 1', 'vm.swappiness = 5'
]

sshd_opts = [
    'PasswordAuthentication no', 'PermitEmptyPasswords no',
    'PermitRootLogin without-password', 'PermitUserEnvironment yes',
    'PubkeyAuthentication yes'
]


@pytest.mark.parametrize('pkg', ['fail2ban', 'iptables', 'sudo'])
def test_pkg(host, pkg):
    package = host.package(pkg)
    assert package.is_installed


@pytest.mark.parametrize('svc', ['firewall', 'ssh', 'fail2ban'])
def test_svc(host, svc):
    service = host.service(svc)
    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize('rule', rules)
def test_firewall(host, rule):
    firewall_rules = host.file('/etc/firewall')
    assert firewall_rules.exists
    assert firewall_rules.contains(rule)


@pytest.mark.parametrize('jail', jails)
def test_fail2ban_jails(host, jail):
    jails = host.file('/etc/fail2ban/jail.local')
    assert jails.exists
    for line in jail:
        assert jails.contains(line)


@pytest.mark.parametrize('opt', kernel_opts)
def test_kernel_hardened(host, opt):
    kernel_config = host.file('/etc/sysctl.conf')
    assert kernel_config.exists
    assert kernel_config.contains(opt)


@pytest.mark.parametrize('opt', sshd_opts)
def test_sshd_opts(host, opt):
    sshd_config = host.file('/etc/ssh/sshd_config')
    assert sshd_config.exists
    assert sshd_config.contains(opt)
