from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import base64
import datetime

admins=[147442381,1709337743,2095069273]
text="""Що входить у підписку до клубу «ACT TODAY» 🤩

1️⃣ тренування 3 рази на тиждень тривалістю ≈ 45 хв. (Пн-Ср-Пт)

2️⃣ 3 ранкові зарядки для підтримання тіла у тонусі тривалістю ≈ 20 хв. 💪

3️⃣ рекомендація зі здорового та сбалансованного харчування

4️⃣ телеграм-чат зі мною та іншими учасниками

Види та особливості тренувань:
✓Тренування на всі групи мʼязів (з акцентом на сідниці/стегна, прес, рельєф та тонус тіла)
✓Функціонал, табата, силові, HIIT, заняття з власною вагою, та додатковими навантаженнями
✓Тренування для зміцнення м’язів спини та рук
✓Стретчинг та робота над поставою

❕ Тренування проходять в форматі «повторюй за мною», з чітких поясненням техніки виконання вправ

З обладнання тобі потрібно:
✅ Гантелі 1-3 кг
✅ Фітнес-резинка
✅ Килимок

Ти маєш 3 дні на виконання вправ, після чого доступ до відео закривається 🙅‍♀️ Але краще не відкладати та робити все разом.

Кожне тренування ти отримуватимеш тут о 6:00 🔥

Важливо❗️ функції “заморозки” підписки немає❗️

Вибирай підписку, щоб дізнатися більше! 👇"""

error_invinte="""
Вибачте збій сервера\n
\t\tЗверніться до адміністратора за допомогою
"""
admin_menu_list=['Розпочати розсилання','↩️Назад в меню']
menu_list=['Клуб тренувань Act Today 🔥','Підписка 🍎','Зв’язок з автором/підтримка ✍','Часті запитання ❓']
ask_list={'❓ Яке обладнання необхідне?':'https://telegra.ph/YAke-obladnannya-potrіbne-03-06','❓ Чи є протипоказання для тренувань?':'https://telegra.ph/Protipokazannya-03-06','❓ Чи підходить новачкам?':'https://telegra.ph/CHi-pіdhodit-novachkam-03-09','❓ Не отримала доступ після оплати, що робити?':'https://telegra.ph/Ne-otrimala-dostup-pіslya-oplati-shcho-robiti-03-09','❓ Інше питання':'https://t.me/jpassistant'}
price={'Місяць - 799 грн. 💰 ':'https://secure.wayforpay.com/payment/sf2c665c7af8e','2 місяці - 1499 грн.💰 ':'https://secure.wayforpay.com/payment/s400aa9266004','3 місяці - 2099 грн.💰 ':'https://secure.wayforpay.com/payment/s5cadf7c4d8d4','6 місяців - 4199 грн.🥳 ':'https://secure.wayforpay.com/payment/s0fc99c558a56'}
club_list=['Безкоштовне пробне тренування 💜','Клуб тренувань ActToday🏋️','↩️Назад в меню']
helper_list={'💬 Чат з автором':'https://t.me/jane_poli','💬 Чат з підтримкою':'https://t.me/jpassistant'}
photo_dict={'📷 Ознайомитися':'https://telegra.ph/ACT-TODAY-03-09'}
start_text=""" 🌟 Вітаємо в клубі "ACT TODAY"! 🌟

Тут тебе чекають:
✅ 3 тренування на тиждень (Пн-Ср-Пт)
✅ 3 ранкові зарядки
✅ Рекомендації зі здорового харчування
✅ Телеграм-чат зі спільнотою

"""
admin_panel_text=""" “Розпочати розсилання” - ця кнопка дозволяє вам ініціювати розсилку повідомлень через вашу адмін-панель. Після натискання на кнопку, бот запитає вас ввести текст повідомлення, яке ви хочете відправити."""
admin_panel_breadcast=""" 
Напишiть текст або фото з текстом у форматi\n " Адмiнiстарор:ваш текст, ПН-08:20 ", \n\nКоми, тире, пробіли дуже важливі \n Приклад запиту з різним текстом:\n
1. Адміністратор:Доброго ранку, ПН-07:00\n
2. Адміністратор:\n\tЩоденне нагадування про воду, ВТ-10:30\n
3. Адміністратор:\n\tСьогодні планується зустріч, СР-15:45\n
4. Адміністратор:\n\tДедлайн звіту, ЧТ-17:00\n
5. Адміністратор:\n\tСподіваюсь, у вас гарний вечір {ссылка на ютуб}, ПТ-19:30\n
"""
class Log:
    def __init__(self, message=None, text=None, error=None):
        self.message = message
        self.text = text
        self.error = error
        self.save_to_log()

    def save_to_log(self):
        with open('log.txt', 'a', encoding='utf-8') as f:
            text=''
            if self.message:
                text = f'[MESSAGE] date={self.message.date} chat_id={self.message.chat.id} username={self.message.chat.username} text={self.message.text}\n'
            if self.text:
                 text += f'[TEXT] {self.text}\n'
            if self.error:
                text += f'[ERROR] {str(datetime.datetime.now())}:\n\t{str(self.error)}\n'
            print(f"{'*'*20}\n{text}\n{'*'*20}\n")
            f.write(f"{'*'*20}\n{text}\n{'*'*20}\n")

def create_button_pairs(elements):
    # Create a list of pairs of elements
    pairs = []
    for i in range(0, len(elements), 2):
        pair = (elements[i], elements[i+1]) if i+1 < len(elements) else elements[i]
        pairs.append(pair)
    return pairs

def inline_button(url_dict: dict) -> InlineKeyboardMarkup:
    """
    Generates an inline keyboard markup with buttons from a dictionary of button names and URLs.

    :param url_dict: Dictionary of button names and URLs.
    :return: An `telebot.types.InlineKeyboardMarkup` object representing the generated keyboard markup.
    """
    keyboard_markup = InlineKeyboardMarkup()
    for name, url in url_dict.items():
        button = InlineKeyboardButton(text=name, url=url, callback_data=[30 if name == 'Месяц' else 30*int(name.split(' ')[0]) if 'месяца' in name else None])
        keyboard_markup.add(button)
    return keyboard_markup


def menu_button(menu_list: list[str] = ['Test Menu']) -> ReplyKeyboardMarkup:
    """
    Generates a keyboard markup with buttons for a given menu list.

    :param menu_list: List of strings representing the names of the buttons to generate.
    :return: A `tbtypes.ReplyKeyboardMarkup` object representing the generated keyboard markup.
    """
    keyboard_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard_markup.max_row_keys=2
    menu_pairs=create_button_pairs(menu_list)
    for button_name in menu_pairs:
        if type(button_name) is tuple:
            keyboard_markup.add(button_name[0], button_name[1])
        else:
            keyboard_markup.add(button_name)
    return keyboard_markup

def decode_base64(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

step_by_time=60