from data.TestSuite import TestSuite
from service.FileHandler import FileHandler
from service.Runner import Runner
from service.Evaluator import Evaluator

class TestController:

    testSuite = TestSuite("SuiteName")


    def __init__(self, arg):
        self.testFile = arg
        self.devFile = arg[3]
        self.fileHandler = FileHandler(TestController.testSuite, self.testFile, self.devFile)
        self.runner = Runner(TestController.testSuite)
        self.evaluator = Evaluator(TestController.testSuite)

    def logic(self):
        self.fileHandler.readFile(self.testFile)
        TestController.testSuite.printAllTestCases()