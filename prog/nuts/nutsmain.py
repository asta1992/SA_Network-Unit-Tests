#!/usr/bin/env python
import sys
import getopt
import yaml
import re
import testcase
import tasklist
import checkResult

tlist = tasklist.Tasklist()
tCase = testcase.Testcase()
cResult = checkResult.CheckResult()
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hv:i:", ["help", "validate=", "input="])
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printUsage()
            sys.exit()
        elif opt in ("-v", "--validate"):
            validate(arg)
        elif opt in ("-i", "--input"):
            inputfile(arg)
            tlist.printTasks()
            choice = input("Run all this Tasks? [Y/n]:").lower()
            if choice == "y":
                tlist.run()
            else:
                print("Bye")
            cResult.compareResult(tlist.getTasks(), tlist.getResult())



def printUsage():
    print("usage")


def inputfile(file):
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper

    with open(file, 'r') as stream:
        try:
            testcases = tCase.load(stream)
            createTasks(testcases)
        except yaml.YAMLError as exc:
            print(exc)


def createTasks(data):
    for i in range(0, len(data.keys())):
        if(data[i]["command"] == "connectivity"):
            if(data[i]["nodes"][0]["os"] == "Linux"):
                tlist.add(data[i]["name"], data[i]["nodes"][0]["name"], "nettest.linuxping ", data[i]["parameter"], data[i]["expected"])
            elif(data[i]["nodes"][0]["OS"] == "IOS"):
                print("IOS")

        elif (data[i]["command"] == "checkbgp"):
            if (data[i]["nodes"][0]["os"] == "Linux"):
                print("Not Supported!")
            elif (data[i]["nodes"][0]["os"] == "IOS"):
                tlist.add(data[i]["name"], data[i]["nodes"][0]["name"], "nettest.linuxping ", data[i]["parameter"], data[i]["expected"])

        elif (data[i]["command"] == "throughput"):
            if (data[i]["nodes"][0]["os"] == "Linux"):
                print("throughput - linux")
            elif (data[i]["nodes"][0]["os"] == "IOS"):
                print("throughput - IOS")

def parseOutput(out, err, type):
    if (type == "text"):
        text = textToJSON(out, 'rest')
        return text
    elif (type == "xml"):
        print(out)
    elif (type == "yaml"):
        print(out)
    else:
        print("Not supported")


def textToJSON(data, regex):
    text = re.search(regex, data)
    return text.group(0)

def xmlToJSON(data):
    print("TODO")

def yamlToJSON(data):
    print("TODO")


def validate(file):
    print("TODO")


if __name__ == "__main__":
    main(sys.argv[1:])
