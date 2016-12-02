import yaml
class FileHandler:


    def __init__(self, testSuite, testFile, deviceFile):
        self.testSuite = testSuite
        self.testFile = testFile
        self.deviceFile = deviceFile


    def yaml(self):
       return yaml.dump(self.__dict__)


    @staticmethod
    def addTests(data, testSuite):
        values = yaml.safe_load(data)
        for val in values:
            testSuite.createTest(val["name"], val["command"], val["devices"], val["parameter"], val["operator"], val["expected"])

    @staticmethod
    def addDevices(data, testSuite):
        values = yaml.safe_load(data)
        for val in values:
            testSuite.createDevice(val["name"], val["os"], val["ipAddress"], val["username"], val["password"])

    def readFile(self, file, type):
        try:
            from yaml import CLoader as Loader, CDumper as Dumper
        except ImportError:
            from yaml import Loader, Dumper

        with open(file, 'r') as stream:
            try:
                if(type=="tests"):
                    self.addTests(stream, self.testSuite)
                else:
                    self.addDevices(stream, self.testSuite)
            except yaml.YAMLError as exc:
                print(exc)


