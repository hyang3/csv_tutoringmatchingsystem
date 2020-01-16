# notes applicable for class:
# times will be stored in a set, with specific names for each time

class Person:
    # each time we parse thru a request: we take in availibility, subject, teacher, request date 
    def __init__(self, type_of_user, email, first_name, last_name, phone_num, home_num, times, subjects): # id, phone, guidance, hr, availibility_info):
       # self.ID = ID
       self.type_of_user = type_of_user
       self.email = email
       self.first_name = first_name
       self.last_name = last_name
       self.phone_num = phone_num
       self.home_num = home_num
       self.times = times
       self.subjects = subjects

    def __str__(self):
        # return "ID: " + self.ID + " name: " + self.name 
        return "{ type_of_user: " + "\"" +  self.type_of_user + "\"" + ", email: " + "\"" + self.email + "\"" + ", first_name: " + "\"" + self.first_name + "\"" + ", last_name: " + "\"" + self.last_name + "\"" + ", phone_num: " + "\"" + self.phone_num + "\"" + ", home_num: " + "\"" + self.home_num + "\"" + ", times: " + "[" + str(self.times)[1:-1] + "]" + ", subjects: " + "[" + str(self.subjects)[1:-1] + "]" + " }"
