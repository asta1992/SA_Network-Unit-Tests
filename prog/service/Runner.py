import subprocess

class Runner:

    def __init__(self, testSuite):
        self.testSuite = testSuite


    def run(self, testCase):
        proc = subprocess.Popen(['salt-call ' + "nuts." + testCase.command + " " + testCase.devices + " " + testCase.parameter + " " + self.testSuite.getDeviceOS(testCase)], stdout=subprocess.PIPE, shell=True)
        result = proc.communicate()
        self.testSuite.setActualResult(testCase, result[0].split( )[1].decode('utf-8'))

    def runAll(self):
        for test in self.testSuite.testcases:
            self.run(test)



