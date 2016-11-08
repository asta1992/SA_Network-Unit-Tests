from salt.client.ssh.client import SSHClient
client = SSHClient()
import salt
import salt.client
local = salt.client.LocalClient()

__virtualname__ = 'nettest'

def __virtual__():
    return __virtualname__

def hello(*args, **kwargs):
    return "hello world"

def ifconfig():
    return __salt__['cmd.run']('ifconfig')

def linuxping(src, dest):
    return local.cmd(src, 'cmd.run', ['ping -c 3 ' + dest])

def showarp(dev):
    #value=client.cmd(dev, '-r "sh afrp"', 'roster-file: /etc/salt/roster, -i')
    #return value
    return 1




