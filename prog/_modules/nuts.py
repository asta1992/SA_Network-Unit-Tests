import salt.client
import re
import json
import xml.etree.ElementTree as ET
from salt.client.ssh.client import SSHClient
from jsonrpclib import Server
client = SSHClient()
local = salt.client.LocalClient()


__virtualname__ = 'nuts'


def __virtual__():
    return __virtualname__

def connectivity(dst, param, os):
    json_data = {}
    if os == "linux":
        result = local.cmd(dst, 'cmd.run', ['ping -c 3 ' + dst])
        text = bytes(result).decode(encoding="utf-8", errors='ignore')
        regex = "([0-9]*)% packet loss"
        r = re.compile(regex)
        m = r.search(text)
        json_data["result"] = (int(float(m.group(1))) < 100)
        json_data["resulttype"] = "single"
        return json.dumps(json_data)
    elif os == "ios":
        return True

def bandwidth(dst, host, os):
    json_data = {}
    if os == "linux":
        local.cmd(dst, 'cmd.run', ['iperf3 -s -D -1'])
        result = local.cmd(host, 'cmd.run', ['iperf3 -c ' + dst])
        text = bytes(result).decode(encoding="utf-8", errors='ignore')
        regex = "([0-9.]{4})(\sGbits\/sec)([\s]*receiver)"
        r = re.compile(regex)
        m = r.search(text)
        json_data["result"] = float(m.group(1)) *1000.0 *1000.0
        json_data["resulttype"] = "single"
        return json.dumps(json_data)

def dnscheck(dst, param, os):
    json_data = {}
    if os == "linux":
        result = local.cmd(dst, 'cmd.run', ['nslookup ' + param])
        text = bytes(result).decode(encoding="utf-8", errors='ignore')
        regex = "(Name:[\s]*[a-z0-9.]*)"
        r = re.compile(regex)
        if r.search(text):
            json_data["result"] = True
        else:
            json_data["result"] = False
        json_data["resulttype"] = "single"
        return json.dumps(json_data)

def dhcpcheck(dst, param, os):
    json_data = {}
    if os == "linux":
        result = local.cmd(dst, 'cmd.run', ['dhcping -s ' + param])
        text = bytes(result).decode(encoding="utf-8", errors='ignore')
        regex = "(Got answer)"
        r = re.compile(regex)
        if r.search(text):
            json_data["result"] = True
        else:
            json_data["result"] = False
        json_data["resulttype"] = "single"
        return json.dumps(json_data)

def webresponse(dst, param, os):
    json_data = {}
    if os == "linux":
        result = local.cmd(dst, 'cmd.run', ['curl -Is '+ param + ' | head -n 1'])
        text = bytes(result).decode(encoding="utf-8", errors='ignore')
        regex = "(HTTP\/1.1 200 OK)"
        r = re.compile(regex)
        if r.search(text):
            json_data["result"] = True
        else:
            json_data["result"] = False
        json_data["resulttype"] = "single"
        return json.dumps(json_data)

def portresponse(dst, port, param, os):
    json_data = {}
    resultList = []
    if os == "linux":
        result = local.cmd(dst, 'cmd.run', ['nmap -p '+ str(port) + ' ' + param])
        text = bytes(result).decode(encoding="utf-8", errors='ignore')
        regex = "([0-9]*)\/[a-z]* (open)"
        r = re.compile(regex)
        for m in re.finditer(regex, text):
            if m.group(2) == "open":
                resultList.append(m.group(1))
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)

def checkuser(dst, os, user, pwd):
    json_data = {}
    resultList = []
    if os == "cisco":
        print('Todo')
    elif os == "arista":
        switch = Server("http://" + user + ":" + pwd + "@" + dst + "/command-api")
        res = switch.runCmds(1, [ "show user-account" ])
        json_data["result"] = res[0]["users"]
        for users in res[0]["users"]:
            resultList.append(users)
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)


def checkversion(dst, os, user, pwd):
    json_data = {}
    if os == 'cisco':
        print('Todo')
    elif os == 'arista':
        switch = Server("http://" + user + ":" + pwd + "@" + dst + "/command-api")
        res = switch.runCmds(1, [ "show version" ])
        json_data["result"] = res[0]["version"]
        json_data["resulttype"] = "single"
        return json.dumps(json_data)


