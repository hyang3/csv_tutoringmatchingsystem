# notes applicable for all classes:
# times will be a list of all times, with 1s and 0s i guess for avaliability?

class Student:
    # each time we parse thru a request: we take in availibility, subject, teacher, request date 
    def __init__(self, name, times, subject): # id, phone, guidance, hr, availibility_info):
       # self.ID = ID
       self.name = name
       self.times = times
       self.subject = subject

    def __str__(self):
        # return "ID: " + self.ID + " name: " + self.name 
        return "name: " + self.name + " times: " + self.times + " subject: " + self.subject

class Tutor: 
    # each time we parse thru a request: we take in availibility, subject, teacher, request date 
    def __init__(self, name, times, subject): #phone, guidance, hr, availibility_info):
       # self.ID = ID
       self.name = name
       self.times = times
       self.subject = subject

    def __str__(self):
        # return "ID: " + self.ID + " name: " + self.name 
        return "name: " + self.name + " times: " + self.times + " subject: " + self.subject

