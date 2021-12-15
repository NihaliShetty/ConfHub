import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date, datetime, timedelta
import time

from app import db_path

server = None


def login():
    global server
    email_user='noreplyconfhub@gmail.com'
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,'confhub123')
    print("Logged in")


def run_iteration():
    print("Looking for new mails to send..")
    connection=sqlite3.connect(db_path)
    cur=connection.cursor()

    logged_in = False
    cur.execute('SELECT * FROM pending_emails')
    allrows=cur.fetchall()
    for eachrow in allrows:
        if not logged_in:
            login()
            logged_in = True
        print(eachrow)
        today=date.today()
        deadline = datetime.strptime(eachrow[2], '%Y-%m-%d').date()
        # print((deadline-today).days)
        daysleft=(deadline-today).days
        if(daysleft<=2):
            print("Sending email.. (less than or equal to 2 days)")
            deadline = deadline + timedelta(days=1)
            mail_content = "Gentle reminder as your conference "+ "'"+eachrow[1]+"' is on "+str(deadline)+" at "+eachrow[3]
            sender_address = 'noreplyconfhub@gmail.com'
            sender_pass = 'confhub123'
            receiver_address = eachrow[0]
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'REMINDER FOR CONFERENCE'
            message.attach(MIMEText(mail_content, 'plain'))
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(sender_address, sender_pass) #login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            print('Mail Sent')
            delete_query="DELETE from pending_emails where confname=? and email=?"
            # print(delete_query)
            cur.execute(delete_query, (eachrow[1], eachrow[0]))
            connection.commit()
            # print("Record deleted successfully ")
            cur.close()
    print("Done")


if __name__ == "__main__":
    while True:
        try:
            run_iteration()
        except Exception as e:
            print(e)
        time.sleep(3)