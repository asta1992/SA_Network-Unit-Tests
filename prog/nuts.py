#!/usr/bin/env python
import sys
import getopt
from application.ValidationController import ValidationController
from application.TestController import TestController



def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hv:i:", ["help", "validate=", "input="])
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printUsage()
            sys.exit()
        elif opt in ("-v", "--validate"):
            validater = ValidationController(arg)
            #Todo
        elif opt in ("-i", "--input"):
            tester = TestController(arg)
            tester.logic()


def printUsage():
    print("usage")


if __name__ == "__main__":
    main(sys.argv[1:])
