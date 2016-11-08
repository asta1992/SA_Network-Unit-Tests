import subprocess
import salt

class Tasklist(object):
    tasks = {}
    taskResult = {}
    i = 0

    def __init__(self):
        self.tasks = {}
        self.taskResult = {}
        self.i = 0

    def add(self, name, dev, tool, parameter, expected):
        self.tasks.update({self.i: {'name' : name, 'dev' : dev, 'tool' : tool,'parameter' : parameter, 'expected': expected}})
        self.i += 1

    def run(self):
        for i in range(0, len(self.tasks.keys())):
            proc = subprocess.Popen(['salt-call ' + self.tasks[i]['tool'] + self.tasks[i]['dev'] + " "+ self.tasks[i]['parameter']], stdout=subprocess.PIPE, shell=True)
            self.taskResult.update({i: {'name' : self.tasks[i]['name'], 'output' : proc.communicate()}})

    def getResult(self):
        return self.taskResult

    def getTasks(self):
        return self.tasks

    def printTasks(self):
        for i in range(0, len(self.tasks.keys())):
            print(self.tasks[i]["name"])


    def printResult(self):
        for i in range(0, len(self.taskResult.keys())):
            print(bytes(self.taskResult[i]["output"][0]).decode(encoding="utf-8", errors='ignore'))