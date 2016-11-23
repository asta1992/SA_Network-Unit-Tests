import datetime

class Evaluator:

    def __init__(self, testSuite):
        self.testSuite = testSuite
        self.date = str(datetime.datetime.now())

    def compare(self, testCase):
        result = ""
        if(testCase.actualResult == testCase.expectedResult):
            print('\033[92m' + testCase.name + ": Test bestanden -------------------------" + '\033[0m')
            result = testCase.name + ': Test bestanden ------------------------- \n'
        else:
            print('\033[91m' + testCase.name + ": Test nicht bestanden -------------------" + '\033[0m')
            result = testCase.name + ': Test nicht bestanden ------------------- \n'

        with open('/var/log/nuts/' + self.testSuite.name + ' - ' + self.date, 'a') as logfile:
            logfile.write(result)

    def compareAll(self):
        for test in self.testSuite.testCases:
            self.compare(test)
