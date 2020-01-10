# notes applicable for all classes:
# times will be stored in a set, with specific names for each time

class Student:
    # each time we parse thru a request: we take in availibility, subject, teacher, request date 
    def __init__(self, name, times, subjects): # id, phone, guidance, hr, availibility_info):
       # self.ID = ID
       self.name = name
       self.times = times
       self.subjects = subjects

    def __str__(self):
        # return "ID: " + self.ID + " name: " + self.name 
        return "name: " + self.name + " times: " + str(self.times) + " subject: " + str(self.subjects)

class Tutor: 
    # each time we parse thru a request: we take in availibility, subject, teacher, request date 
    def __init__(self, name, times, subjects): #phone, guidance, hr, availibility_info):
       # self.ID = ID
       self.name = name
       self.times = times
       self.subjects = subjects

    def __str__(self):
        # return "ID: " + self.ID + " name: " + self.name 
        return "name: " + self.name + " times: " + str(self.times) + " subject: " + str(self.subjects)

