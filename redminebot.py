from sqlite3 import connect
from redmine import Redmine
from datetime import date, timedelta
from calendar import day_name
from random import choice
from os import remove
from sys import argv

if len(argv) > 1:
    run = argv[1]
else:
    print("Oh no you didnt tell me what to do ...")
    print("usage : ",argv[0]," <issue/time>")
    exit()

#print("Login : ")
#username = input("Enter your redmine username : ")
username = 'dhruv.paranjape'                #hardcode it here but when user_id and user_key has more entries make this input based selection.
user = username.split('.')[0].title()
print("Hello ",user)

conn = connect('redmine.db')

conn.execute('''CREATE TABLE IF NOT EXISTS ISSUES
       (ID           INTEGER    PRIMARY KEY,
       ISSUE_ID      INT        NOT NULL,
       SUBJECT       TEXT       NOT NULL,
       HOURS         INT        NOT NULL,
       ACTIVITY      TEXT       NOT NULL,
       TEAM          TEXT       NOT NULL,
       END_DATE      TEXT       NOT NULL);''')

user_id = {'dhruv.paranjape' : 598}
user_key = {'dhruv.paranjape' :'4ff211d2eb10cda87af5001049c6115112363562'}
projects = {'Development' : 431, 'UTM' : 112, '1.8.0' : 306, '2.0.0' : 308}
task_id = {'QA-Task': 10,'Dev-Task' : 9}
status_id = {'In Progress' : 2, 'Completed' : 13, 'Closed' : 5}
activity_id = {"Design" : 8, "Documentation" : 26, "Coding" : 9, "Meeting" : 16, "KT" : 17, "Code Review" : 18, "Test Design" : 27, "Test Execution" : 28, "Test Review" : 29, "Analysis" : 43, "Test Plan creation" : 133}

red = Redmine('http://projects.qhtpl.com/redmine', key=user_key[username])

cursor = conn.cursor()

def IssueCreator(late_counter = 0):

    today = date.today() - timedelta(days=late_counter)

    print("Today is ",today)

    if day_name[today.weekday()].lower() == "saturday" or day_name[today.weekday()].lower() == "sunday":
        print(day_name[today.weekday()]," skipping ... ")
        return 1

    subject = input("Subject is : ")
    #Dumb-Dumb starts here
    if subject.lower().find('automation') != -1 or subject.lower().find('creat') != -1 or subject.lower().find('cod') != -1:
        Activity = "Coding"
    elif subject.lower().find('meeting') != -1 or subject.lower().find('discus') != -1:
        Activity = "Meeting"
    elif subject.lower().find('kt') != -1:
        Activity = "KT"
    else:
        Activity = "Test Execution"

    task = 'QA-Task'
    Team = 'QA'
    project = '2.0.0'

    duration = int(input("duration : <In days> defaults to only today : "))
    duration = duration or 0
    future = today + timedelta(days=duration)
    time = int(input("How long will it take <In hours> : "))

    print("Creating issue  for : ",today)

    issue = red.issue.create(project_id=projects[project], subject=subject, tracker_id=task_id[task], assigned_to_id=user_id[username], start_date=today, due_date=future, estimated_hours=time, done_ratio=0)

    print("issue with id : ",issue.id," created")
    print("Saving issue ...")

    cursor.execute("""INSERT INTO ISSUES (ISSUE_ID, SUBJECT, HOURS ,ACTIVITY ,TEAM, END_DATE) VALUES (?,?,?,?,?,?)""", (issue.id, subject, round(time), Activity, Team, future))
    conn.commit()
    print("Issue saved")

    if late_counter == 0:
        conn.close()

if run == 'issue':

    IssueCreator()

elif run == 'time' :

    for wordlist in cursor.execute("SELECT * FROM ISSUES"):

        print("Building Query now ...")

        issue_id = wordlist[1]
        duration = wordlist[3]
        activity = wordlist[4]
        team     = wordlist[5]
        end_time = wordlist[6]

        print("Processing "+wordlist[2]+" Issue now")


        status = red.issue.update(issue_id, status_id=status_id['Completed'], done_ratio=100)

        if status == True:
            print("Issue status Updated")
        else:
            print("Issue failed to update")

        coin_toss = choice([0, 1, 2])

        time_spent = duration + coin_toss

        print("Entering time now ...")

        issue = red.time_entry.create(issue_id=issue_id, spent_on=end_time, hours=time_spent, activity_id=activity_id[activity], custom_fields=[{'id': 64, 'value': team}])

        print("time entry for issue id : ",issue_id," added")

        close_status = red.issue.update(issue_id, status_id=status_id['Closed'], done_ratio=100)

        if close_status == True:
            print("Issue Closed")
        else:
            print("Issue closing failed")

    conn.close()
    print("All issue time entries created deleting db file now...")

    remove('redmine.db')
    print(" Database Removed")

elif run == "late":
    print("you are using a secret feature ! shhhh")
    late_counter = int(input("how late are you ?"))

    while late_counter > -1:
        IssueCreator(late_counter)
        late_counter -= 1
else :
    print("You chose poorly #ThePrincessBride")
    print("Shutting down now ...")

print("All done")
print("Bye !")
