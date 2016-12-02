class Device:

    def __init__(self, name, os, ipAddress, username, password):
        self.name = name
        self.os = os
        self.ipAddress = ipAddress
        self.username = username
        self.password = password

    def displayDevice(self):
        print("Name : ", self.name, ", OS: ", self.os, "IP-Adresse : ", self.ipAddress, ", Username: ", self.username, ", password: **********")