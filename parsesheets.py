from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#my own stuff 
from classes import Person 

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1RVDwqvr-YXgKwMgoGNGa5aWLu5LxjRBpGQzMJTgjeds'
# range of stuff --> so start if ther are no titles or smth
SAMPLE_RANGE_NAME = 'A:L'

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
    indexes_with_students = []
    if not values:
        print('No data found.')
    else:
        #this is where we parse information
        for i in range(len(values)):

            #if the first line is just description
            if i == 0:
                continue

            # *********************
            # SETUP BEFORE PARSING
            # *********************
            #parsinf info about people
            person_info = values[i]

            #time: [2-3]
            times = set()
            subjects = set()

            # *********************
            # ACTUAL PARSING
            # *********************

            # TIMES!! : parse once for each day of the week
            days = ["m", "t", "w", "r", "f"]
            for d in range(5):
                #monday avaliability is in col #6
                times_for_this_day = person_info[6 + d].split(",")
                for time in times_for_this_day:
                    if time != "none":
                        times.add(days[d] + time.strip())

            #subjects
            s = person_info[11].split(",")
            for subject in s:
                subjects.add(subject.strip())

            # *********************
            # SORTING STUDENTS VS TUTORS
            # *********************

            person = Person(person_info[0], person_info[1], person_info[2], person_info[3], person_info[4], person_info[5], times, subjects)
            if person_info[0] == "student":
                list_of_students.append(person)
                indexes_with_students.append(i + 1)
            else:
                list_of_tutors.append(person)

    # # debugging
    # print("students:")
    # for student in list_of_students:
        # print(student)
    
    # print("tutors:")
    # for tutor in list_of_tutors:
        # print(tutor)

    # set which student we want to match

    # we want to automatically match all students 
    print(indexes_with_students)
    
    n = 0
    for index in indexes_with_students:
        student_to_match = list_of_students[n]

        row = [str(student_to_match)]
        num_matches = 0
        for tutor in list_of_tutors:
            if matches(student_to_match, tutor):
                row.append(str(tutor)) 
                num_matches += 1

        range_to_update = "N" + str(index) + ":" + chr(ord("N") + num_matches) + str(index)


        values = [row]
        # body
        body = {
                "value_input_option" : "RAW",
                "data" : {
                        "range" : range_to_update,
                        "values" : values
                    }            
                }


        result = service.spreadsheets().values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body).execute()

        print(str(num_matches) + " matches found.")
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))
        n += 1


if __name__ == '__main__':
    main()
