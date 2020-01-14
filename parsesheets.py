from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#my own stuff 
from classes import Student
from classes import Tutor

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '11dWm0lbaDnaburQQiRPA54idP63n2lz_Q1KSnGhM6oQ'
# range of stuff --> so start if ther are no titles or smth
SAMPLE_RANGE_NAME = 'A45:E52'

def matches(student, tutor):
    # if student.times != tutor.times:
        # match = False 
    # if student.subject != tutor.subject:
        # match = False 
    t = False
    s = False
    
    for time in student.times:
        if time in tutor.times:
            t = True 
    for subject in student.subjects:
        if subject in tutor.subjects:
            s = True 

    return t and s 


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # will need to edit later 
    if os.path.exists('../token.pickle'):
        with open('../token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #here is whre instead we could get all of the valus
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    # values[0] returns things by column
    values = result.get('values', [])

    # parsing notes: for avalibilities, we will represent as [DAY][b,a,1,2,3,4]
    # reminder: student constructor: (name, times, subject)

    # This is where the parsing is going to happen
    list_of_tutors = []
    list_of_students = []
    if not values:
        print('No data found.')
    else:
        #this is where we parse information
        for i in range(len(values)):
            person_info = values[i]
            #time: [2-3]
            times = set()
            subjects = set()

            #monday times
            mt = person_info[2].split(",")
            for t in mt:
                if t != "none":
                    times.add("m" + t.strip())
            #tuesday times
            tt = person_info[3].split(",")
            for t in tt:
                if t != "none":
                    times.add("t" + t.strip())

            #subjects
            s = person_info[4].split(",")
            for subject in s:
                subjects.add(subject.strip())

            if person_info[1] == "student":
                student = Student(person_info[0], times, subjects)
                list_of_students.append(student)
            else:
                tutor = Tutor(person_info[0], times, subjects)
                list_of_tutors.append(tutor)

    # # debugging
    # print("students:")
    # for student in list_of_students:
        # print(student)
    
    # print("tutors:")
    # for tutor in list_of_tutors:
        # print(tutor)

    # set which student we want to match
    student_to_match = list_of_students[0]


    row = [str(student_to_match)]
    num_matches = 0
    for tutor in list_of_tutors:
        if matches(student_to_match, tutor):
            row.append(str(tutor)) 
            num_matches += 1

    range_to_update = "A54:" + chr(ord("A") + num_matches) + "54"


    values = [row]
    # body
    body = {
            "value_input_option" : "RAW",
            "data" : {
                    "range" : range_to_update,
                    "values" : values
                }            
            }

    range_to_update = "A54:B54"

    result = service.spreadsheets().values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body).execute()

    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))


if __name__ == '__main__':
    main()
