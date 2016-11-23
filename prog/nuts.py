#!/usr/bin/env python
import sys
import os
import getopt
from src.application.ValidationController import ValidationController
from src.application.TestController import TestController



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
            validater = ValidationController(os.getcwd() + "/" + arg, os.getcwd() + "/" + args[0])
            validater.logic()
        elif opt in ("-i", "--input"):
            tester = TestController(os.getcwd() + "/" + arg, os.getcwd() + "/" + args[0])
            tester.logic()


def printUsage():
    print("usage")


if __name__ == "__main__":
    main(sys.argv[1:])
