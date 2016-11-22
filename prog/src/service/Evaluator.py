class Evaluator:

    def __init__(self, testSuite):
        self.testSuite = testSuite

    def compare(self, testCase):
        if(testCase.actualResult == testCase.expectedResult):
            print('\033[92m' + testCase.name + ": Test bestanden -------------------------" + '\033[0m')
        else:
            print('\033[91m' + testCase.name + ": Test nicht bestanden -------------------" + '\033[0m')

    def compareAll(self):
        for test in self.testSuite.testCases:
            self.compare(test)
