import subprocess
import progressbar
import json
from time import sleep

class Runner:

    def __init__(self, testSuite):
        self.testSuite = testSuite


    def run(self, testCase):
        bar = progressbar.ProgressBar(maxval=20, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

        if self.testSuite.getLoginRequired(testCase):
            proc = subprocess.Popen(['salt-call ' + "nuts." + testCase.command + " " + self.testSuite.getDeviceDestination(testCase) + " " + ' '.join(testCase.parameter) + " " + self.testSuite.getDeviceOS(testCase) + " " + self.testSuite.getUsername(testCase) + " " + self.testSuite.getPassword(testCase)], stdout=subprocess.PIPE, shell=True)
        else:
            proc = subprocess.Popen(['salt-call ' + "nuts." + testCase.command + " " + self.testSuite.getDeviceDestination(testCase) + " " + ' '.join(testCase.parameter) + " " + self.testSuite.getDeviceOS(testCase)], stdout=subprocess.PIPE, shell=True)


        for i in bar(range(100)):
            if proc.poll() == 0:
                bar.update(100)
                break
            elif proc.poll() == -1:
                result = "Error"
                break
            else:
                if i == 99:
                    if proc.poll() != 0:
                        sleep(0.2)
                sleep(0.1)
                bar.update(i)


        result = proc.communicate()[0].decode('utf-8')

        self.testSuite.setActualResult(testCase, json.loads(result[result.index('{'):(result.index('}') + 1)]))


    def runAll(self):
        print("\n")
        for test in self.testSuite.testCases:
            print("Start Test " + test.name)
            self.run(test)
            print("\n")