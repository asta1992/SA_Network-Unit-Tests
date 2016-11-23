from salt.client.ssh.client import SSHClient
client = SSHClient()
import salt.client
local = salt.client.LocalClient()
import re

__virtualname__ = 'nuts'

def __virtual__():
    return __virtualname__

def hello(*args, **kwargs):
    return "hello world"

def ifconfig():
    return 0

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

def showarp(dev):
    #value=client.cmd(dev, '-r "sh afrp"', 'roster-file: /etc/salt/roster, -i')
    #return value
    return 1




