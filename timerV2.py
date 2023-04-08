import asyncio
import datetime
import json

class Timer:
    def __init__(self, user_id, subscription_date):
        self.user_id = user_id
        self.subscription_date = subscription_date
        self.task = None

    async def delete_user(self):
        # Здесь вы можете написать код, который удаляет пользователя
        print(f'Удален пользователь с id {self.user_id}')
        # Удалить информацию о подписке пользователя из словаря
        if self.user_id in subscriptions:
            del subscriptions[self.user_id]
            # Сохранить информацию о подписках в файле
            save_subscriptions()

    async def delete_user_after_30_days(self):
        await asyncio.sleep(datetime.timedelta(days=30).total_seconds())
        await self.delete_user()

    def start(self):
        time_diff = datetime.datetime.now() - datetime.datetime.strptime(self.subscription_date, '%Y-%m-%d %H:%M:%S.%f')
        if time_diff.days >= 30:
            asyncio.run(self.delete_user())
        else:
            self.task = asyncio.create_task(self.delete_user_after_30_days())

    def stop(self):
        if self.task:
            self.task.cancel()

# Словарь, содержащий информацию о подписках пользователей
subscriptions = {}

# Имя файла для сохранения информации о подписках
SUBSCRIPTIONS_FILE = 'subscriptions.json'

def load_subscriptions():
    global subscriptions
    try:
        with open(SUBSCRIPTIONS_FILE, 'r') as f:
            subscriptions = json.load(f)
    except FileNotFoundError:
        pass

def save_subscriptions():
    with open(SUBSCRIPTIONS_FILE, 'w') as f:
        json.dump(subscriptions, f)

# Восстановить расписание таймеров для всех пользователей
def restore_timers():
    for user_id, subscription_date in subscriptions.items():
        timer = Timer(user_id, subscription_date)
        timer.start()

# Загрузить информацию о подписках при запуске кода
load_subscriptions()

# Восстановить расписание таймеров
restore_timers()