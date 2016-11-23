import datetime

class Evaluator:

    def __init__(self, testSuite):
        self.testSuite = testSuite
        self.date = str(datetime.datetime.now())


    def compare(self, testCase):
        return testCase.actualResult == testCase.expectedResult


    def printResult(self, testCase):
        if self.compare(testCase):
            print('\033[92m' + testCase.name + ": Test bestanden -------------------------" + '\033[0m')
            result = testCase.name + ': Test bestanden ------------------------- \n'
        else:
            print('\033[91m' + testCase.name + ": Test nicht bestanden -------------------" + '\033[0m')
            result = testCase.name + ': Test nicht bestanden ------------------- \n'

        with open('/var/log/nuts/' + self.testSuite.name + ' - ' + self.date, 'a') as logfile:
            logfile.write(result)


    def printAllResults(self):
        for test in self.testSuite.testCases:
            self.printResult(test)

