import requests
from datetime import datetime
import smtplib

MY_LAT = 37.368832
MY_LONG = -122.036346

username = "USERNAME"
password = "PASSWORD"

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if abs(iss_latitude - MY_LAT) < 5 and abs(iss_longitude - MY_LONG) < 5:
       return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) - 7
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) - 7
    if sunrise < 0:
        sunrise += 12
    if sunset < 0:
        sunset += 12
    time_now = datetime.now().hour
    if time_now < sunrise and time_now > sunset:
        return True

if is_iss_overhead() and is_night:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=username, password=password)
        connection.sendmail(from_addr=username, to_addrs=username, msg="Subject: Look Up!")