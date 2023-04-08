import sqlite3
import time
import asyncio
from datetime import datetime, timedelta
from tetx import Log, step_by_time


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









# async def subscription_timer(bot,user_id=None, date_message=None, subscription_time=None, time_left=None):
#     if user_id is None and date_message is None and subscription_time is None:
#         # Restart all active timers
#         print('Restarting all timers')
#         active_subscriptions = get_active_subscriptions()
#         tasks = []
#         print('active_subscriptions:', active_subscriptions)
#         for subscription in active_subscriptions:
#             print(f'Restarting timer for {active_subscriptions.index(subscription)}')
#             user_id, date_message, expiration_date, subscription_time, time_left = subscription
#             if time_left is not None and time_left <= 0:
#                 print(f'Subscription {user_id} has expired')
#                 continue  # Subscription has already expired, don’t restart the timer
#             elif time_left is not None:
#                 # Subscription still has time left, continue counting down
#                 date_message = datetime.now()
#                 tasks.append(asyncio.create_task(subscription_timer(user_id, date_message, subscription_time, time_left)))
#                 print(f'Timer started for {user_id}')
#                 print('Restarting timer')
#             else:
#                 # New subscription
#                 date_message = datetime.now()
#                 tasks.append(asyncio.create_task(subscription_timer(user_id, date_message, subscription_time, time_left)))
#                 print(f'Timer started for {user_id}')
#                 print('Starting timer')
#         print('All timers restarted')
#         print('tasks:', tasks)
#         await asyncio.gather(*tasks)
#         return

#     # Start a new timer
#     print(f"Timer started for {user_id}")
#     conn = sqlite3.connect('subscriptions.db')
#     c = conn.cursor()
#     expiration_date = date_message + int(timedelta(days=subscription_time).total_seconds())

#     c.execute('''CREATE TABLE IF NOT EXISTS subscriptions
#                 (user_id INTEGER, date_message INTEGER, expiration_date INTEGER, subscription_time INTEGER, time_left INTEGER)''')
#     c.execute('INSERT INTO subscriptions VALUES (?, ?, ?, ?, ?)', (user_id, date_message,
#             int(expiration_date), subscription_time, time_left))
#     conn.commit()
#     conn.close()

#     while True:
#         conn = sqlite3.connect('subscriptions.db')
#         c = conn.cursor()
#         users_id = c.execute('SELECT * FROM subscriptions').fetchall()
#         Log(text=f'Users {users_id}')
#         time_left -= 60
#         c.execute(
#             'UPDATE subscriptions SET time_left = ? WHERE user_id = ?', (time_left, user_id))
#         conn.commit()
#         conn.close()

#         if time_left <= 0:
#             # User is no longer subscribed
#             Log(text=f'Subscription {user_id} has expired')
#             c.execute('DELETE FROM subscriptions WHERE user_id = ?', (user_id,))
#             bot.ban_chat_member(chat_privat_id, user_id)
#             break
#         days_left = time_left // 86400
#         hours_left = (time_left % 86400) // 3600
#         minutes_left = (time_left % 3600) // 60
#         Log(text=f'Time {user_id} {days_left} days, {hours_left} hours, {minutes_left} minutes left')
#         await asyncio.sleep(60)


# def get_active_subscriptions():
#     conn = sqlite3.connect('subscriptions.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS subscriptions
#                 (user_id INTEGER, date_message INTEGER, expiration_date INTEGER, subscription_time INTEGER, time_left INTEGER)''')
#     conn.commit()
#     active_subscriptions = c.execute('SELECT * FROM subscriptions').fetchall()
#     conn.close()
#     return active_subscriptions
