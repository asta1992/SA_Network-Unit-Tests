class TestCase:

    def __init__(self, name, command, devices, parameter, operator, expectedResult):
        self.name = name
        self.command = command
        self.devices = devices
        self.parameter = parameter
        self.operator = operator
        self.expectedResult = expectedResult

    def setActualResult(self, actualResult):
        self.actualResult = actualResult

    def getActualResult(self):
        return self.actualResult

    def displayTestCase(self):
        print("Name : ", self.name, ", Command: ", self.command, "Devices : ", self.devices, ", Parameter: ", self.parameter, "operator: ", self.operator, ", Expected: ", self.expectedResult)