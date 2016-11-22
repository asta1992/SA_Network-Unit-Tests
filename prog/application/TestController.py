from data.TestSuite import TestSuite
from service.FileHandler import FileHandler
from service.Runner import Runner
from service.Evaluator import Evaluator

class TestController:

    testSuite = TestSuite("SuiteName")


    def __init__(self, testFile, devFile):
        self.testFile = testFile
        self.devFile = devFile
        self.fileHandler = FileHandler(TestController.testSuite, self.testFile, self.devFile)
        self.runner = Runner(TestController.testSuite)
        self.evaluator = Evaluator(TestController.testSuite)

    def logic(self):
        self.fileHandler.readFile(self.testFile, "tests")
        self.fileHandler.readFile(self.devFile, "devices")
        TestController.testSuite.printAllTestCases()
        TestController.testSuite.printAllDevices()

        print("\n\n Start.........")

        self.runner.runAll()

        self.testSuite.getActualResult()