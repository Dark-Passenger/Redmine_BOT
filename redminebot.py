from sqlite3 import connect
from redmine import Redmine
from datetime import date
from datetime import timedelta
from datetime import datetime
from random import choice
from os import remove
from sys import argv

if len(sys.argv) < 2:
    print("usage : ",argv[0]," < issue / time >")
    exit()

conn = connect('redmine.db')

conn.execute('''CREATE TABLE IF NOT EXISTS ISSUES
	   (ID 			 INTEGER    PRIMARY KEY,
	   ISSUE_ID      INT        NOT NULL,
	   SUBJECT       TEXT       NOT NULL,
	   HOURS         INT        NOT NULL,
	   ACTIVITY      TEXT       NOT NULL,
	   TEAM          TEXT       NOT NULL,
	   END_DATE      TEXT       NOT NULL);''')

user_id = 
user_key = 
projects = 
task_id = 
status_id = 
activity_id = 

print("Hello User")
run = argv[1].lower()
red = Redmine('<redmine_url>', key=user_key['<user>'])
cursor = conn.cursor()
today = date.today()

if run == 'issue':
	print("Today is ",today)
	subject = input("Subject is : ")
	#Dumb-Dumb starts here
	# keywords detection and setting parameters based on that.
	# scrubbed due to possible Insider info

	duration = int(input("duration : <In days>"))
	future = today + timedelta(days=duration)
	time = int(input("How long will it take <In hours> "))

	print("Creating issue  for : ",today)

	issue = red.issue.create(project_id=projects[project], subject=subject, tracker_id=task_id[task], assigned_to_id=user_id['<user>'], start_date=today, due_date=future, estimated_hours=time, done_ratio=0)
	
	print("issue with id : ",issue.id," created")
	print("Saving issue ...")

	cursor.execute("""INSERT INTO ISSUES (ISSUE_ID, SUBJECT, HOURS ,ACTIVITY ,TEAM, END_DATE) VALUES (?,?,?,?,?,?)""", (issue.id, subject, round(time), Activity, Team, future))
	conn.commit()
	print("Issue saved")
	conn.close()
	print("All done")
	print("Bye !")

elif run == 'time' :

	for wordlist in cursor.execute("SELECT * FROM ISSUES"):

		print("Building Query now ...")

		issue_id = wordlist[1]
		duration = wordlist[3]
		activity = wordlist[4]
		team     = wordlist[5]
		end_date = wordlist[6]
		#incase it does not work
		#end_date = datetime.strptime(wordlist[7],"%Y-%m-%d").date()


		print("Processing "+wordlist[2]+" Issue now")


		status = red.issue.update(issue_id, status_id=status_id['Completed'], done_ratio=100)
		
		if status == True:
			print("Issue status Updated")
		else:
			print("Issue failed to update")
		
		coin_toss = choice([-1, 0, 1])

		time_spent = duration + coin_toss
		
		print("Entering time now ...")
		
		issue = red.time_entry.create(issue_id=issue_id, spent_on=end_date, hours=time_spent, activity_id=activity_id[activity], custom_fields=[{'id': 64, 'value': team}])

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
	print("All done")
	print("Bye !")

else :
	print("You chose poorly #ThePrincessBride")
	print("Shutting down now ...")
