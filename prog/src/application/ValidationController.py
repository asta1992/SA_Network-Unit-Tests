from src.service.FileValidator import FileValidator

class ValidationController:

    fileHandler = None

    def __init__(self, testFile, deviceFile, fileType):
        self.fileType = fileType
        self.testFile = testFile
        self.devFile = deviceFile
        self.fileValidator = FileValidator(self.testFile, self.devFile)


    def __init__(self, file, fileType):
        self.fileType = fileType
        if fileType == "tests":
            self.testFile = file
            self.fileValidator = FileValidator(self.testFile)
        elif fileType == "devices":
            self.devFile == file
            self.fileValidator = FileValidator(self.devFile)


    def logic(self):
        if self.fileType == "both":
            procTest = self.fileValidator.validate("tests")
            procDev = self.fileValidator.validate("devices")
            self.fileValidator.printTestFileResults(procTest)
            self.fileValidator.printDeviceFileResults(procDev)

        elif self.fileType == "tests":
            procTest = self.fileValidator.validate(self.fileType)
            self.fileValidator.printTestFileResults(procTest)

        elif self.fileType == "devices":
            devTest = self.fileValidator.validate(self.fileType)
            self.fileValidator.printDeviceFileResults(devTest)
