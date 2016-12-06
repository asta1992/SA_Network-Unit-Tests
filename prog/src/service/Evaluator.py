import datetime
import json

class Evaluator:

    def __init__(self, testSuite):
        self.testSuite = testSuite
        self.date = str(datetime.datetime.now())


    def compare(self, testCase):
        if testCase.operator == "=":
            if testCase.actualResult["resulttype"] == "single":
                return testCase.expectedResult == testCase.actualResult["result"]
            elif testCase.actualResult["resulttype"] == "multiple":
                return self.comp(testCase.actualResult["result"], testCase.expectedResult)
        elif testCase.operator == "<":
            return testCase.expectedResult < testCase.actualResult["result"]
        elif testCase.operator == ">":
            return testCase.expectedResult > testCase.actualResult["result"]
        elif testCase.operator == "not":
            return testCase.expectedResult != testCase.actualResult["result"]


    def printResult(self, testCase):
        res = ""
        exp = ""
        if testCase.actualResult["resulttype"] == "single":
            res = testCase.actualResult["result"]
            exp = testCase.expectedResult
        elif testCase.actualResult["resulttype"] == "multiple":
            for result in testCase.actualResult["result"]:
                res += result + " "
            for expected in testCase.expectedResult:
                exp += expected + " "

        if self.compare(testCase):
            print('\033[92m' + testCase.name + ": Test bestanden ------------------------- \033[0m\nExpected: " + str(exp) + " " + testCase.operator +  " Actual: " + str(res))
            result = testCase.name + ": Test bestanden ------------------------- \nExpected: " + str(exp) + " " + testCase.operator + " \nActual:  "+ str(res)
        else:
            print('\033[91m' + testCase.name + ": Test nicht bestanden -------------------\033[0m\nExpected: " + str(exp) + " " + testCase.operator + " Actual: " + str(res))
            result = testCase.name + ": Test nicht bestanden ------------------- \nExpected: " + str(exp) + " " + testCase.operator + " \nActual:  "+ str(res)

        with open('/var/log/nuts/' + self.testSuite.name + ' - ' + self.date, 'a') as logfile:
            logfile.write(result)


    def printAllResults(self):
        for test in self.testSuite.testCases:
            self.printResult(test)

    def comp(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for val in list1:
            if val not in list2:
                return False
        return True