import re


class CheckResult(object):

    def compareResult(self, tasks, results):
        for i in range(0, len(tasks.keys())):
            if tasks[i]["tool"] == 'nettest.linuxping ':
                text = bytes(results[i]["output"][0]).decode(encoding="utf-8", errors='ignore')
                regex = "([0-9]*)% packet loss"
                r = re.compile(regex)
                m = r.search(text)
                print(m)
                if m.group(1) == str(tasks[i]["expected"]):
                    print('\033[92m' + tasks[i]["name"] + ": Test bestanden -------------------------" + '\033[0m')
                else:
                    print('\033[91m' + tasks[i]["name"] + ": Test nicht bestanden -------------------" + '\033[0m')

