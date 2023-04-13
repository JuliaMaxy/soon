import os
import requests
from flask import redirect, render_template, request, session
from functools import wraps
import json
import threading
import datetime
import schedule
import time
from email.message import EmailMessage
import smtplib


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

    def send_email_helper(msg, recipient):
        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('jjuliamaxxx@gmail.com', 'lguvzwzsishpgtbf')
            smtp.send_message(msg)

            print("Email sent!")
    # Schedule the email to be sent
    job = schedule.every().day.at(send_time).do(send_email_helper, msg, recipient)
    job.next_run = send_datetime  # Set the next run time to the send date and time

    # Run the schedule
    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)
    threading.Thread(target=run_schedule, daemon=True).start()



def search_movie(title):
    url = f"https://api.themoviedb.org/3/search/multi?api_key=8e5c4304a2b0fc02884f12935ccffac9&query={title}"
    response = requests.get(url)
    response_json = response.json()
    results = response_json["results"]
    movies_and_tv = []
    for result in results:
        # Check if the result is a movie or TV show
        if result["media_type"] in ["movie", "tv"]:
            movie_or_tv_info = {}
            movie_or_tv_info["title"] = result["title"] if result["media_type"] == "movie" else result["name"]
            movie_or_tv_info["date"] = result["release_date"] if result["media_type"] == "movie" else result["first_air_date"]
            movie_or_tv_info["rating"] = result["vote_average"]
            movie_or_tv_info["image"] = f"https://image.tmdb.org/t/p/w500{result['poster_path']}"
            movie_or_tv_info["media_type"] = result["media_type"]
            movies_and_tv.append(movie_or_tv_info)
    return movies_and_tv
    

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

