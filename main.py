import requests
from datetime import datetime
import smtplib
import time
import pandas as pd
MY_EMAIL = "##########"
MY_PASSWORD = "############"
MY_LAT = 28.524578 # Your latitude
MY_LONG = 77.206612 # Your longitude

data = pd.read_csv("mails.csv")
names = data.name.to_list()
mails = data.email.to_list()

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the iss position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
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
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        for n in names:
            check_email = data[data['name'] == n]
            filtered_email = check_email.email.to_list()
            name = n.title()
            connection = smtplib.SMTP("smpt.google.com")
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=filtered_email,
                msg=f"Subject:Look Up👆{name}\n\nThe ISS is above you in the sky."
            )


