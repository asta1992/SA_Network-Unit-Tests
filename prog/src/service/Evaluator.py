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
        if self.compare(testCase):
            print('\033[92m' + testCase.name + ": Test bestanden ------------------------- \033[0m\nExpected: " + str(self.getExpected(testCase)) + " " + testCase.operator +  " Actual: " + str(self.getResult(testCase)))
            self.writeLog(testCase, self.getResult(testCase), self.getExpected(testCase), True)
        else:
            print('\033[91m' + testCase.name + ": Test nicht bestanden -------------------\033[0m\nExpected: " + str(self.getExpected(testCase)) + " " + testCase.operator + " Actual: " + str(self.getResult(testCase)))
            self.writeLog(testCase, self.getResult(testCase), self.getExpected(testCase), False)


    def getResult(self, testCase):
        res = ''
        if testCase.actualResult["resulttype"] == "single":
            res = testCase.actualResult["result"]
        elif testCase.actualResult["resulttype"] == "multiple":
            res = ' '.join(testCase.actualResult["result"])
        return res

    def getExpected(self, testCase):
        exp = ''
        if testCase.actualResult["resulttype"] == "single":
            exp = testCase.expectedResult
        elif testCase.actualResult["resulttype"] == "multiple":
            exp = ' '.join(testCase.expectedResult)
        return exp


    def writeLog(self, testCase, res, exp, passed):
        if passed:
            result = '\n' + testCase.name + ": Test bestanden ------------------------- \nExpected: " + str(exp) + " " + testCase.operator + " Actual:  " + str(res)
        else:
            result = '\n' + testCase.name + ": Test nicht bestanden ------------------- \nExpected: " + str(exp) + " " + testCase.operator + " Actual:  " + str(res)

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