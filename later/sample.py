import schedule
import time
import smtplib
import datetime
from email.message import EmailMessage

def send_email(recipient, subject, message, send_date, send_time):
    # Create the message
    msg = EmailMessage()
    msg['From'] = 'jjuliamaxxx@gmail.com'
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(message)

    # Convert the send date and time to a datetime object
    send_datetime = datetime.datetime.strptime(send_date + ' ' + send_time, '%Y-%m-%d %H:%M')

    # Schedule the email to be sent
    job = schedule.every().day.at(send_time).do(send_email_helper, msg, recipient)
    job.next_run = send_datetime  # Set the next run time to the send date and time

    # Run the schedule
    while True:
        schedule.run_pending()
        time.sleep(1)

def send_email_helper(msg, recipient):
    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('jjuliamaxxx@gmail.com', 'lguvzwzsishpgtbf')
        smtp.send_message(msg)

        print("Email sent!")






# def send_email(email, title):
#     sender = 'jjuliamaxxx@gmail.com'
#     receiver = email
#     password = 'lguvzwzsishpgtbf'
#     subject = f'The {title} is out today'
#     body = """Ran Okay"""
#     em = EmailMessage()
#     em['From'] = sender
#     em['To'] = receiver
#     em['Subject'] = subject

#     send_date = datetime.date(2023, 4, 13)
#     send_time = datetime.time(10, 50)

#     # create a scheduler object
#     scheduler = sched.scheduler(time.time, time.sleep)


#     def send():
#         # create the email message
#         em.set_content(body)

#         context = ssl.create_default_context()

#         with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#             smtp.login(sender, password)
#             # connect to the SMTP server
#             # send the email
#             smtp.sendmail(sender, receiver, em.as_string())
#             smtp.quit()

#             print("Email sent!")