import subprocess
import os
import sys

class FileValidator:


    def __init__(self, testFile, deviceFile):
        self.testFile = testFile
        self.deviceFile = deviceFile


    def validate(self, fileType):
        FNULL = open(os.devnull, 'w')
        if fileType == "tests":
            return subprocess.Popen(['pykwalify -d ' + self.testFile + ' -s ' + os.getcwd() + '/src/service/testSchema.yaml' ], stdout=subprocess.PIPE, stderr=FNULL, shell=True)
        elif fileType == "devices":
            return subprocess.Popen(['pykwalify -d ' + self.deviceFile + ' -s ' + os.getcwd() + '/src/service/deviceSchema.yaml' ], stdout=subprocess.PIPE,  stderr=FNULL, shell=True)


    def printTestFileResults(self, procTest):
        print("Test-File: \n" + procTest.communicate()[0].decode('utf-8'))


    def printDeviceFileResults(self, procDev):
        print("Device-File: \n" + procDev.communicate()[0].decode('utf-8'))

