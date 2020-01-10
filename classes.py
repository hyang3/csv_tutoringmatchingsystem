class Student:
    # each time we parse thru a request: we take in availibility, subject, teacher, request date 
    def __init__(self, ID, name): #phone, guidance, hr, availibility_info):
       self.ID = ID
       self.name = name

    def __str__(self):
        return "ID: " + self.ID + " name: " + self.name 

class Tutor: 
    # each time we parse thru a request: we take in availibility, subject, teacher, request date 
    def __init__(self, ID, name): #phone, guidance, hr, availibility_info):
       self.ID = ID
       self.name = name

    def __str__(self):
        return "ID: " + self.ID + " name: " + self.name 

