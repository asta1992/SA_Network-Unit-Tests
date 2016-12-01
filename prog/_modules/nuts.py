from salt.client.ssh.client import SSHClient
client = SSHClient()
import salt.client
local = salt.client.LocalClient()
import re

__virtualname__ = 'nuts'

def __virtual__():
    return __virtualname__

def linuxping(src, dest, os):
    if os == "linux":
        result = local.cmd(src, 'cmd.run', ['ping -c 3 ' + dest])
        text = bytes(result).decode(encoding="utf-8", errors='ignore')
        regex = "([0-9]*)% packet loss"
        r = re.compile(regex)
        m = r.search(text)
        return m.group(1)
    elif os == "ios":
        return True

def bandwidth(server, host, os):
    if os == "linux":
        local.cmd(server, 'cmd.run', ['iperf3 -s -D -1'])
        result = local.cmd(host, 'cmd.run', ['iperf3 -c ' + server])
        text = bytes(result).decode(encoding="utf-8", errors='ignore')
        regex = "([0-9.]{4})(\sGbits\/sec)([\s]*receiver)"
        r = re.compile(regex)
        m = r.search(text)
        return float(m.group(1)) *1000.0 *1000.0

def dnscheck(src, dst, os):
    if os == "linux":
        result = local.cmd(src, 'cmd.run', ['nslookup ' + dst])
        text = bytes(result).decode(encoding="utf-8", errors='ignore')
        regex = "(Name:[\s]*[a-z0-9.]*)"
        r = re.compile(regex)
        if(r.search(text)):
           return True
        else:
            return False

