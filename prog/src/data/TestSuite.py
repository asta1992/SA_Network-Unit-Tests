from .Device import Device
from .TestCase import TestCase

class TestSuite:
    name = ""
    testCases = []
    devices = []

    def __init__(self, name):
        TestSuite.name = name

    def createTest(self, name, command, devices, parameter, expectedResult):
        test = TestCase(name, command, devices, parameter, expectedResult)
        TestSuite.testCases.append(test)


    def createDevice(self, name, os, ipAddress, username, password):
        dev = Device(name, os, ipAddress, username, password)
        TestSuite.devices.append(dev)

    def getDeviceOS(self, testCase):
        return self.getDeviceByName(testCase.devices).os


    def setActualResult(self, testCase, actualResult):
       self.getTestByName(testCase.name).setActualResult(actualResult)

    def getActualResult(self, testCase):
        return self.getTestByName(testCase.name).getActualResult()


    def getTestByName(self,name):
        for test in TestSuite.testCases:
            if test.name == name:
                return test


    def getDeviceByName(self,name):
        for dev in TestSuite.devices:
            if dev.name == name:
                return dev


    def printAllTestCases(self):
        for test in TestSuite.testCases:
            test.displayTestCase()


    def printAllDevices(self):
        for dev in TestSuite.devices:
            dev.displayDevice()