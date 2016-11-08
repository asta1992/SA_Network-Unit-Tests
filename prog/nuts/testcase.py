import yaml

class Testcase(object):
    testcases = {}
    i = 0

    def __init__(self):
        self.testcases = {}
        self.i = 0

    def yaml(self):
        return yaml.dump(self.__dict__)


    def load(self, data):
        values = yaml.safe_load_all(data)
        for val in values:
            self.__adds(val["number"], val["name"], val["command"], val["nodes"], val["parameter"], val["expected"], val["timeout"])
        return self.testcases

    def __adds(self, number, name, command, nodes, parameter, expected, timeout):
        self.testcases.update( {self.i: {'number': number, 'name' : name, 'command': command, 'nodes': nodes, 'parameter' : parameter, 'expected': expected, 'timeout': timeout}})
        self.i += 1