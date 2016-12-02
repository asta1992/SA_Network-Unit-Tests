import datetime

class Evaluator:

    def __init__(self, testSuite):
        self.testSuite = testSuite
        self.date = str(datetime.datetime.now())


    def compare(self, testCase):
        if testCase.operator == "=":
            return testCase.expectedResult == testCase.actualResult
        elif testCase.operator == "<":
            return testCase.expectedResult < testCase.actualResult
        elif testCase.operator == ">":
            return testCase.expectedResult > testCase.actualResult
        elif testCase.operator == "not":
            return testCase.expectedResult != testCase.actualResult


    def printResult(self, testCase):
        if self.compare(testCase):
            print('\033[92m' + testCase.name + ": Test bestanden ------------------------- \033[0m\nExpected: " + testCase.expectedResult + " " + testCase.operator +  " Actual: " + testCase.actualResult)
            result = testCase.name + ": Test bestanden ------------------------- \nExpected: " + testCase.expectedResult + " " + testCase.operator + " \nActual:  "+ testCase.actualResult
        else:
            print('\033[91m' + testCase.name + ": Test nicht bestanden -------------------\033[0m\nExpected: " + testCase.expectedResult + " " + testCase.operator + " Actual: " + testCase.actualResult)
            result = testCase.name + ": Test nicht bestanden ------------------- \nExpected: " + testCase.expectedResult + " " + testCase.operator + " \nActual:  "+ testCase.actualResult

        with open('/var/log/nuts/' + self.testSuite.name + ' - ' + self.date, 'a') as logfile:
            logfile.write(result)


    def printAllResults(self):
        for test in self.testSuite.testCases:
            self.printResult(test)

