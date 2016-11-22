from data.TestSuite import TestSuite
from service.FileHandler import FileHandler

class ValidationController:

    testSuite = TestSuite("ValidationSuite")
    fileHandler = None

    def __init__(self, arg):
        self.testFile = arg[1]
        self.devFile = arg[2]
        ValidationController.fileHandler = FileHandler(ValidationController.testSuite, self.testFile, self.devFile)
