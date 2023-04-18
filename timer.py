import sqlite3
import asyncio
from datetime import datetime, timedelta
from tetx import Log, step_by_time,admins
import json
import re
import pytz
import threading
from telebot.types import *


def db_write(last_time, user_id):
    conn=sqlite3.connect('FitnesBot.db')
    curs=conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS users (last_time INTEGER, user_id INTEGER)")
    # Проверяем, существует ли запись с указанным user_id
    curs.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_record = curs.fetchone()

    if existing_record:
        # Если запись существует, обновляем ее last_time
        curs.execute("UPDATE users SET last_time=? WHERE user_id=?", (last_time, user_id))
    else:
        # Если запись не существует, вставляем новую запись
        curs.execute("INSERT INTO users (last_time, user_id) VALUES (?,?)", (last_time, user_id))

    # Сохраняем изменения в базе данных
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()


def db_read():
    conn=sqlite3.connect('FitnesBot.db')
    curs=conn.cursor()
    curs.execute("SELECT * FROM users")
    rows=curs.fetchall()
    conn.close()
    return rows

chat_privat_id = '-1001881688132'
def days_to_unix(days):
    # Get today's date
    today = datetime.now()
    
    # Add the given number of days to today's date
    future_date = today + timedelta(days=days)
    
    # Convert the future date to a Unix timestamp
    unix_timestamp = int(future_date.timestamp())-today.timestamp()
    
    return unix_timestamp

async def subscription_timer(bot, user_id:int=None, subscription_time:int=None):
    if user_id == None and subscription_time == None:
        tasks = []
        for user in db_read():
            subscription_time=user[0]
            end_date=datetime.now() + timedelta(days=subscription_time)
            while datetime.now() < end_date:
                tasks.append(asyncio.create_task(subscription_timer(bot, user[1], subscription_time)))
                break
        await asyncio.gather(*tasks)
    elif user_id != None and subscription_time != None:    
        end_date = datetime.now() + timedelta(days=subscription_time)
        while datetime.now() < end_date:
            Log(text=f"Таймер начал свою работу. пользователь {user_id} продлил подписку. Осталось {end_date - datetime.now()}", error=None)
            # Приостанавливаем выполнение на 60 секунду
            await asyncio.sleep(step_by_time)
            db_write((end_date - datetime.now()).days, user_id)

    Log(text=f"Время вышло! Останавливаем таймер {user_id}", error=None)
    bot.ban_chat_member(chat_id=chat_privat_id, user_id=user_id)  

def delete_message(bot, chat_id, message_id):
    try:
        Log(text=f"Удаление сообщения {message_id} из чата {chat_id}")
        bot.delete_message(chat_id, message_id)
        Log(text=f"Удаление сообщения {message_id} из чата {chat_id} завершено")
    except Exception as e:
        Log(text=f"Delete message in {chat_id}", error=e)

def parse_message(message):
    # Admin:text of broadcast (https://youtube.com), ПН-08:00
    name_pattern = r"^(.+?):"
    text_pattern = r": (.+?),"
    day_pattern = r", ([а-яА-Яa-zA-Z]+)-"
    time_pattern = r"-([\d:]+)"
    delete_time = r", (\(\d+\))$"
    # time_zone = pytz.timezone("Europe/Kyiv")
    Log(text=f"Текст рассылки \n\t{message} текущее время: {datetime.now()}")

    name_match = re.search(name_pattern, message)
    text_match = re.search(text_pattern, message)
    day_match = re.search(day_pattern, message)
    time_match = re.search(time_pattern, message)
    Log(text=f"Параметры рассылки:\n\t{name_match}\n\t{text_match}\n\t{day_match}\n\t{time_match}")
    if not (name_match and text_match and day_match and time_match ):
            return None
    else:
        name = re.search(name_pattern, message).group(1)
        text = re.search(text_pattern, message).group(1)
        day = re.search(day_pattern, message).group(1)
        time = re.search(time_pattern, message).group(1)
    
    time_parts = time.split(":")
    hours, minutes = time_parts[0], time_parts[1]

    if len(hours) != 2:
        hours = "0" + hours
    if len(minutes) != 2:
        minutes = "0" + minutes

    formatted_time = f"{hours}:{minutes}"

    return name, text, day, formatted_time

def broadcast_message(bot, text, chat_id):
    global users_messages
    users_messages = {}
    users = db_read()

    # Send the starting message and save its message ID for later updates
    bot.send_message(chat_id, "Рассылка началась...")

    # Send the message to all admins
    for admin in admins:
        bot.send_message(admin, text)

    for user in users:
        try:
            if user[1] not in admins:
                user_message = bot.send_message(user[1], text)
                users_messages[chat_id] = user_message.message_id
                Log(text=f'Удаление сообщения у пользователя {chat_id} через 2 дня ')
                threading.Timer(172699, delete_message, args=[bot, user[1], user_message.message_id]).start()

        except Exception as e:
            Log(text=f"Не удалось отправить сообщение пользователю {user[1]}: {e}")
    json.dump(users_messages, open('messages.json', 'a+'))
    

async def schedule_broadcast(name, text, day, time_str, bot, chat_id, delete_delay=10):
    async def job():
        Log(text=f"Sending '{text}' from '{name}' at '{time_str}'")
        broadcast_message(bot, text, chat_id=chat_id)

    # Set your desired time zone
    time_zone = pytz.timezone("Europe/Kiev")

    # Get the current time in the specified time zone
    now = datetime.now(time_zone)

    # Parse the input time string (e.g., "15:30") and set it in the desired time zone
    scheduled_time = datetime.strptime(time_str, "%H:%M").time()
    scheduled_datetime = now.replace(hour=scheduled_time.hour, minute=scheduled_time.minute, second=0, microsecond=0)

    # If the scheduled time is in the past, add one day
    if scheduled_datetime < now:
        scheduled_datetime += timedelta(days=1)

    # Calculate the remaining time in seconds
    remaining_time = (scheduled_datetime - now).total_seconds()
    bot.send_message(chat_id, f"Время до началла рассылки {int(remaining_time)}/сек")
    Log(text=f"Время до началла рассылки {int(remaining_time)}/сек")
    # Sleep until the scheduled time
    await asyncio.sleep(int(remaining_time))

    # Call the job function
    await job()


