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

def getCiscoXML(dst, param, cmd, attribut):
    value = local.cmd("arch", 'cmd.run', [
        "salt-ssh " + dst + " -i -r '" + cmd + " " + str(param) + " " + attribut + " | format flash:nuts.odm' --roster-file=/etc/salt/roster"])
    xml = value['arch'][value['arch'].index('<'):len(value['arch'])]
    return ET.fromstring(xml)

def returnMultiple(result):
    json_data = {}
    json_data["result"] = result
    json_data["resulttype"] = "multiple"
    return json.dumps(json_data)

def returnSingle(result):
    json_data = {}
    json_data["result"] = result
    json_data["resulttype"] = "single"
    return json.dumps(json_data)


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


def stpinterfacestate(dst, param, os, user, pwd):
    json_data = {}
    resultList = []
    if os == 'ios':
        value = local.cmd("arch", 'cmd.run', ["salt-ssh " + dst + " -i -r 'sh spanning-tree interface " + param + " | format flash:nuts.odm' --roster-file=/etc/salt/roster"])
        xml = value['arch'][value['arch'].index('<'):len(value['arch'])]
        tree = ET.fromstring(xml)
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_spanning-tree_interface_*}entry'):
            resultList.append(id.find('{ODM://flash:nuts.odm//show_spanning-tree_interface_*}Vlan').text + ":" + id.find('{ODM://flash:nuts.odm//show_spanning-tree_interface_*}Sts').text)
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)
    elif os == 'arista':
        print('Not Implemented')

def stpinterfacerole(dst, param, os, user, pwd):
    json_data = {}
    resultList = []
    if os == 'ios':
        value = local.cmd("arch", 'cmd.run', ["salt-ssh " + dst + " -i -r 'sh spanning-tree interface " + param + " | format flash:nuts.odm' --roster-file=/etc/salt/roster"])
        xml = value['arch'][value['arch'].index('<'):len(value['arch'])]
        tree = ET.fromstring(xml)
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_spanning-tree_interface_*}entry'):
            resultList.append(id.find('{ODM://flash:nuts.odm//show_spanning-tree_interface_*}Vlan').text + ":" + id.find('{ODM://flash:nuts.odm//show_spanning-tree_interface_*}Role').text)
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)
    elif os == 'arista':
        print('Not Implemented')

def stpinterfacecost(dst, param, os, user, pwd):
    json_data = {}
    resultList = []
    if os == 'ios':
        value = local.cmd("arch", 'cmd.run', [
            "salt-ssh " + dst + " -i -r 'sh spanning-tree interface " + param + " | format flash:nuts.odm' --roster-file=/etc/salt/roster"])
        xml = value['arch'][value['arch'].index('<'):len(value['arch'])]
        tree = ET.fromstring(xml)
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_spanning-tree_interface_*}entry'):
            resultList.append(
                id.find('{ODM://flash:nuts.odm//show_spanning-tree_interface_*}Vlan').text + ":" + id.find('{ODM://flash:nuts.odm//show_spanning-tree_interface_*}Cost').text)
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)
    elif os == 'arista':
        print('Not Implemented')


def stprootid(dst, param, os, user, pwd):
    json_data = {}
    resultList = []
    if os == 'ios':
        value = local.cmd("arch", 'cmd.run', [
            "salt-ssh " + dst + " -i -r 'sh spanning-tree root | format flash:nuts.odm' --roster-file=/etc/salt/roster"])
        xml = value['arch'][value['arch'].index('<'):len(value['arch'])]
        tree = ET.fromstring(xml)
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_spanning-tree_root}entry'):
            resultList.append(
                id.find('{ODM://flash:nuts.odm//show_spanning-tree_root}Vlan').text + ":" + id.find('{ODM://flash:nuts.odm//show_spanning-tree_root}RootID').text.split(' ')[1])
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)
    elif os == 'arista':
        print('Not Implemented')

def stprootcost(dst, param, os, user, pwd):
    json_data = {}
    resultList = []
    if os == 'ios':
        value = local.cmd("arch", 'cmd.run', [
            "salt-ssh " + dst + " -i -r 'sh spanning-tree root | format flash:nuts.odm' --roster-file=/etc/salt/roster"])
        xml = value['arch'][value['arch'].index('<'):len(value['arch'])]
        tree = ET.fromstring(xml)
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_spanning-tree_root}entry'):
            resultList.append(
                id.find('{ODM://flash:nuts.odm//show_spanning-tree_root}Vlan').text + ":" + id.find('{ODM://flash:nuts.odm//show_spanning-tree_root}Cost').text)
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)
    elif os == 'arista':
        print('Not Implemented')

def stpvlaninterfaces(dst, param, os, user, pwd):
    json_data = {}
    resultList = []
    if os == 'ios':
        value = local.cmd("arch", 'cmd.run', [
            "salt-ssh " + dst + " -i -r 'sh spanning-tree vlan " + str(param) + " | format flash:nuts.odm' --roster-file=/etc/salt/roster"])
        xml = value['arch'][value['arch'].index('<'):len(value['arch'])]
        tree = ET.fromstring(xml)
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_spanning-tree_vlan_*}entry'):
            resultList.append(
                id.find('{ODM://flash:nuts.odm//show_spanning-tree_vlan_*}Interface').text)
        json_data["result"] = resultList
        json_data["resulttype"] = "multiple"
        return json.dumps(json_data)
    elif os == 'arista':
        print('Not Implemented')

def stpvlanblockedports(dst, param, os, user, pwd):
    resultList = []
    if os == 'ios':
        tree = getCiscoXML(dst, param, "sh spanning-tree blockedports")
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_spanning-tree_blockedports}entry'):
            resultList.append(id.find('{ODM://flash:nuts.odm//show_spanning-tree_blockedports}Name').text + ":" + id.find('{ODM://flash:nuts.odm//show_spanning-tree_blockedports}BlockedInterfacesList').text)
        return returnMultiple(resultList)
    elif os == 'arista':
        print('Not Implemented')

def vlanports(dst, param, os, user, pwd):
    resultList = []
    if os == 'ios':
        tree = getCiscoXML(dst, param, "sh vlan id ")
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_vlan_id_*}entry'):
            resultList.append(id.find('{ODM://flash:nuts.odm//show_spanning-tree_blockedports}Ports').text)
        return returnMultiple(resultList)
    elif os == 'arista':
        print('Not Implemented')

def interfacestatus(dst, param, os, user, pwd):
    result = ""
    if os == 'ios':
        tree = getCiscoXML(dst, param, "sh interface", " status")
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_interface_*_status}entry'):
            result = (id.find('{ODM://flash:nuts.odm//show_interface_*_status}Status').text)
        return returnSingle(result)
    elif os == 'arista':
        print('Not Implemented')

def interfacevlan(dst, param, os, user, pwd):
    result = ""
    if os == 'ios':
        tree = getCiscoXML(dst, param, "sh interface", " status")
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_interface_*_status}entry'):
            result = (id.find('{ODM://flash:nuts.odm//show_interface_*_status}Vlan').text)
        return returnSingle(result)
    elif os == 'arista':
        print('Not Implemented')

def interfaceduplex(dst, param, os, user, pwd):
    result = ""
    if os == 'ios':
        tree = getCiscoXML(dst, param, "sh interface", " status")
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_interface_*_status}entry'):
            result = (id.find('{ODM://flash:nuts.odm//show_interface_*_status}Duplex').text)
        return returnSingle(result)
    elif os == 'arista':
        print('Not Implemented')

def interfacespeed(dst, param, os, user, pwd):
    result = ""
    if os == 'ios':
        tree = getCiscoXML(dst, param, "sh interface", " status")
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_interface_*_status}entry'):
            result = (id.find('{ODM://flash:nuts.odm//show_interface_*_status}Speed').text)
        return returnSingle(result)
    elif os == 'arista':
        print('Not Implemented')

def cdpneighbor(dst, param, os, user, pwd):
    result = ""
    if os == 'ios':
        tree = getCiscoXML(dst, param, "sh cdp neighbors", "")
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_cdp_neighbors_*}entry'):
            result = (id.find('{ODM://flash:nuts.odm//show_cdp_neighbors_*}DeviceID').text)
        return returnSingle(result)
    elif os == 'arista':
        print('Not Implemented')

def cdpneighborcount(dst, param, os, user, pwd):
    if os == 'ios':
        tree = getCiscoXML(dst, "", "sh cdp neighbors", "")
        i = 0
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_cdp_neighbors}entry'):
            i += 1
        return returnSingle(i)
    elif os == 'arista':
        print('Not Implemented')

def arp(dst, param, os, user, pwd):
    resultList= []
    if os == 'ios':
        tree = getCiscoXML(dst, "", "sh arp", "")
        for id in tree.iter(tag='{ODM://flash:nuts.odm//show_arp}entry'):
            if id.find('{ODM://flash:nuts.odm//show_arp}Address').text == param:
                resultList.append(param + ":" + id.find('{ODM://flash:nuts.odm//show_arp}HardwareAddr').text)
                return returnMultiple(resultList)
        resultList.append(param + ":-")
        return returnMultiple(resultList)
    elif os == 'arista':
        print('Not Implemented')