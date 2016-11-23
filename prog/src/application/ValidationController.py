from src.service.FileValidator import FileValidator

class ValidationController:

    fileHandler = None

    def __init__(self, testFile, deviceFile):
        self.testFile = testFile
        self.devFile = deviceFile
        self.fileValidator = FileValidator(self.testFile, self.devFile)

    def logic(self):
        self.fileValidator.validate()