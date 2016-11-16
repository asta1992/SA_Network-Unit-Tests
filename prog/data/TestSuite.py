from .Device import Device
from .TestCase import TestCase

class TestSuite:
    name = ""
    testcases = []
    devices = []

    def __init__(self, name):
        TestSuite.name = name

    def createTest(self, name, command, devices, parameter, expectedResult):
        test = TestCase(name, command, devices, parameter, expectedResult)
        TestSuite.testcases.append(test)


    def createDevice(self, name, os, ipAddress, username, password):
        dev = Device(name, os, ipAddress, username, password)
        TestSuite.devices.append(dev)

    def getExecutionCommand(self, testName):
        for test in TestSuite.testcases:
            if test.name == testName:
                return test.command

    def setActualResult(self, testName, actualResult):
        for test in TestSuite.testcases:
            if test.name == testName:
                test.setActualResult(actualResult)

    def printAllTestCases(self):
        for test in TestSuite.testcases:
            test.displayTestCase()

    def printAllDevices(self):
        for dev in TestSuite.devices:
            dev.displayDevice()