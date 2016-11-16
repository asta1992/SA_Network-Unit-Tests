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
        values = yaml.safe_load_all(data)
        for val in values:
            testSuite.createTest(val["name"], val["command"], val["devices"], val["parameter"], val["expected"])

    def readFile(self, file):
        try:
            from yaml import CLoader as Loader, CDumper as Dumper
        except ImportError:
            from yaml import Loader, Dumper

        with open(file, 'r') as stream:
            try:
                self.addTests(stream, self.testSuite)
            except yaml.YAMLError as exc:
                print(exc)

    def addDevices(self):
        print("Todo")

