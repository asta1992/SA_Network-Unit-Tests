import subprocess
import os
import sys

class FileValidator:


    def __init__(self, testFile, deviceFile):
        self.testFile = testFile
        self.deviceFile = deviceFile


    def validate(self):
        FNULL = open(os.devnull, 'w')
        procTest = subprocess.Popen(['pykwalify -d ' + self.testFile + ' -s ' + os.getcwd() + '/src/service/testSchema.yaml' ], stdout=subprocess.PIPE, stderr=FNULL, shell=True)
        procDev = subprocess.Popen(['pykwalify -d ' + self.deviceFile + ' -s ' + os.getcwd() + '/src/service/deviceSchema.yaml' ], stdout=subprocess.PIPE,  stderr=FNULL, shell=True)
        print("Test-File: \n" + procTest.communicate()[0].decode('utf-8'))
        print("Device-File: \n" + procDev.communicate()[0].decode('utf-8'))