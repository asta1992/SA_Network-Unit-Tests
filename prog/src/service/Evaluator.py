class Evaluator:

    def __init__(self, testSuite):
        self.testSuite = testSuite


    def compare(self, testCase):
        return testCase.actualResult == testCase.expectedResult


    def printResult(self, testCase):
        if self.compare(testCase):
            print('\033[92m' + testCase.name + ": Test bestanden -------------------------" + '\033[0m')
        else:
            print('\033[91m' + testCase.name + ": Test nicht bestanden -------------------" + '\033[0m')


    def printAllResults(self):
        for test in self.testSuite.testCases:
            self.printResult(test)

