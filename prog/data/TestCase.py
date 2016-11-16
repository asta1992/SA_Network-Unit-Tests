class TestCase:

    def __init__(self, name, command, devices, parameter, expectedResult):
        self.name = name
        self.command = command
        self.devices = devices
        self.parameter = parameter
        self.expectedResult = expectedResult

    def setActualResult(self, actualResult):
        self.actualResult = actualResult

    def getActualResult(self):
        return self.actualResult

    def displayTestCase(self):
        print("Name : ", self.name, ", Command: ", self.command, "Devices : ", self.devices, ", Parameter: ", self.parameter, ", Expected: ", self.expectedResult)