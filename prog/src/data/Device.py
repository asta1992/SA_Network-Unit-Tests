class Device:

    def __init__(self, name, os, destination, loginRequired, username, password):
        self.name = name
        self.os = os
        self.loginRequired = loginRequired
        self.destination = destination
        self.username = username
        self.password = password

    def displayDevice(self):
        print("Name : ", self.name, ", OS: ", self.os, "Destination : ", self.destination, ", Login required: ", self.loginRequired, ", Username: ", self.username, ", password: **********")