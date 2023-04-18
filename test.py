from timer import *

import datetime
from dateutil import tz
import schedule
import time

def schedule_broadcast(name, text, day, time_str, bot, chat_id):
    def job():
        Log(text=f"Sending '{text}' from '{name}' at '{time_str}'")
        broadcast_message(bot, text, chat_id=chat_id)

    # Set your desired time zone
    time_zone = tz.gettz("Europe/Kiev")

    # Get the current time in the specified time zone
    now = datetime.datetime.now(time_zone)

    # Parse the input time string (e.g., "15:30") and set it in the desired time zone
    scheduled_time = datetime.datetime.strptime(time_str, "%H:%M").time()
    scheduled_datetime = now.replace(hour=scheduled_time.hour, minute=scheduled_time.minute, second=0, microsecond=0)

    # If the scheduled time is in the past, add one day
    if scheduled_datetime < now:
        scheduled_datetime += datetime.timedelta(days=1)

    # Convert the scheduled datetime to a string in the format "HH:MM"
    adjusted_time_str = scheduled_datetime.strftime("%H:%M")

    # Schedule the job using the adjusted time
    schedule.every().day.at(adjusted_time_str).do(job)

# Example usage of the function
schedule_broadcast("Example", "Hello, Europe/Kiev!", "day", "20:26", "bot", "chat_id")


