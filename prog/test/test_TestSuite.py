import pytest
from src.data.Device import Device
from src.data.TestSuite import TestSuite

class TestTestSuite:

    testSuite = TestSuite("TestTestSuite")

    @classmethod
    def setup_class(cls):
        device1 = Device("Server01", "Linux", "192.168.100.1", "root", "1234")
        device2 = Device("Server02", "Linux", "192.168.100.2", "root", "1234")
        device3 = Device("Switch01", "Cisco", "192.168.200.1", "admin", "1234")
        device4 = Device("Switch02", "Cisco", "192.168.200.1", "admin", "1234")
        cls.testSuite.createDevice("Server01", "Linux", "192.168.100.1", "root", "1234")
        cls.testSuite.createDevice("Server02", "Linux", "192.168.100.2", "root", "1234")
        cls.testSuite.createDevice("Switch01", "Cisco", "192.168.200.1", "admin", "1234")
        cls.testSuite.createDevice("Switch02", "Cisco", "192.168.200.1", "admin", "1234")
        cls.testSuite.createTest("testPingFromAToB", "ping", device1, "", "0")
        cls.testSuite.createTest("showNeighborsByArp", "arp", device2, "", "0")

    def test_getDeviceByName(self):
        assert self.testSuite.getDeviceByName("Server01").name == "Server01"
