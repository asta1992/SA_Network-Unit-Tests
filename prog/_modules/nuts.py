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

def connectivity(dst, param, os, user, password):
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
        value = local.cmd("arch", 'cmd.run',["salt-ssh " + dst + " -i -r 'ping '" + param + "  --roster-file=/etc/salt/roster"])
        text = bytes(value).decode(encoding="utf-8", errors='ignore')
        regex = 'percent \(([0-5])'
        r = re.compile(regex)
        m = r.search(text)
        json_data["result"] = (int(float(m.group(1))) > 0)
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)


def traceroute(dst, param, os, user, pwd):
    json_data = {}
    resultList = []
    if os == "ios":
        value = local.cmd("arch", 'cmd.run', ["salt-ssh " + dst + " -i -r 'traceroute '" + param +"  --roster-file=/etc/salt/roster"])
        text = bytes(value).decode(encoding="utf-8", errors='ignore')
        regex = "([0-9.]*)( [0-9]* msec)"
        for m in re.finditer(regex, text):
            resultList.append(m.group(1))
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)

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
    if os == "ios":
        value = local.cmd("arch", 'cmd.run', ["salt-ssh " + dst + " -i -r 'sh run | i username' --roster-file=/etc/salt/roster"])
        text = bytes(value).decode(encoding="utf-8", errors='ignore')
        regex = "username ([a-zA-Z0-9]*)"
        for m in re.finditer(regex, text):
            resultList.append(m.group(1))
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)

    elif os == "arista":
        switch = Server("http://" + user + ":" + pwd + "@" + dst + "/command-api")
        res = switch.runCmds(1, ["show user-account"])
        for users in res[0]["users"]:
            resultList.append(users)
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)


def checkversion(dst, os, user, pwd):
    json_data = {}
    if os == 'ios':
        value = local.cmd("arch", 'cmd.run', ["salt-ssh " + dst + " -i -r 'sh run | format flash:nuts.odm' --roster-file=/etc/salt/roster"])
        xml = value['arch'][value['arch'].index('<'):len(value['arch'])]
        tree = ET.fromstring(xml)
        json_data["result"] = tree[0][0].text
        json_data["resulttype"] = "single"
        return json.dumps(json_data)

    elif os == 'arista':
        switch = Server("http://" + user + ":" + pwd + "@" + dst + "/command-api")
        res = switch.runCmds(1, [ "show version" ])
        json_data["result"] = res[0]["version"]
        json_data["resulttype"] = "single"
        return json.dumps(json_data)

def checkospfneighbors(dst, os, user, pwd):
    json_data = {}
    resultList = []
    if os == 'ios':
        value = local.cmd("arch", 'cmd.run', ["salt-ssh " + dst + " -i -r 'sh ip ospf neighbor | format flash:nuts.odm' --roster-file=/etc/salt/roster"])
        xml = value['arch'][value['arch'].index('<'):len(value['arch'])]
        tree = ET.fromstring(xml)
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_ip_ospf_neighbor}NeighborID'):
            resultList.append(id.text)
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)
    elif os == 'arista':
        print('Not Implemented')


def countospfneighbors(dst, os, user, pwd):
    value = checkospfneighbors(dst, os, user, pwd)
    json_data = json.loads(value[value.index('{'):(value.index('}') + 1)])
    json_data["result"] = len(json_data["result"])
    json_data["resulttype"] = "single"
    return json.dumps(json_data)

def checkospfneighborsstatus(dst, os, user, pwd):
    json_data = {}
    resultList = []
    if os == 'ios':
        value = local.cmd("arch", 'cmd.run', ["salt-ssh " + dst + " -i -r 'sh ip ospf neighbor | format flash:nuts.odm' --roster-file=/etc/salt/roster"])
        xml = value['arch'][value['arch'].index('<'):len(value['arch'])]
        tree = ET.fromstring(xml)
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_ip_ospf_neighbor}entry'):
            resultList.append(id.find('{ODM://flash:nuts.odm//show_ip_ospf_neighbor}NeighborID').text + ":" + id.find('{ODM://flash:nuts.odm//show_ip_ospf_neighbor}State').text)
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)
    elif os == 'arista':
        print('Not Implemented')


def routingpath(dst, os, user, pwd):
    cmd = '<< EOF' \
          ' tclsh\n' \
          'ios_config "ip sla 10"\n' \
          'ios_config "ip sla 10" "path-echo 10.0.1.201"\n' \
          'ios_config "ip sla schedule 10 start-time now life 0"\n' \
          'ios_config "do sh ip sla statistics 10"\n' \
          'EOF'

    son_data = {}
    resultList = []
    if os == 'ios':
        value = local.cmd("arch", 'cmd.run', ["salt-ssh " + dst + " -i -r "+ cmd +" --roster-file=/etc/salt/roster"])
        print(cmd)
        print(value)

