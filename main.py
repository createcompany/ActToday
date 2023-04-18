import traceback
import telebot
import asyncio
from tetx import *
from timer import *
from telebot.types import InputMediaPhoto

bot = telebot.TeleBot('6121940381:AAGLygbXhCIGRfXU-M6prlfg9D0uwGIzyM0')

bot.unban_chat_member(chat_id='-1001881688132', user_id='1709337743')
bot.unban_chat_member(chat_id='-1001881688132', user_id='5082791922')

admins=[]

async def main(bot):
    # await subscription_timer(bot)
    
    @bot.callback_query_handler(func=lambda call: True)
    def process_callback_button(callback_query):
        bot.send_message(callback_query.from_user.id, callback_query.data)

    @bot.message_handler(commands=['start'])
    def message_start(message):

        message_text = message.text
        args = message_text.split()[1] if len(message_text.split()) > 1 else None
        if args == None:
            try:
                Log(message=message, text=message.text, error=None)
                name_list=[InputMediaPhoto(open(img,'rb')) for img in ['FitnesBot/img (1).png', 'FitnesBot/img (2).png', 'FitnesBot/img (3).png','FitnesBot/img (4).png','FitnesBot/img (5).png']]
                print(name_list)
                bot.send_message(message.chat.id, start_text, reply_markup=menu_button(menu_list), parse_mode='Markdown')
                bot.send_media_group(chat_id=message.chat.id, media=name_list)
            except Exception as e:
                Log(error=traceback.format_exc())
        elif args != None and '-' in args:
            args=args.split('-')
            Log(message=message,text=f"Payment methot is {args[0]} on days {args[1]} and message.text is {message.text}")
        
            if args[0] == 'False':
                Log(error=traceback.format_exc())
                bot.send_message(message.chat.id, error_invinte, reply_markup=menu_button(menu_list), parse_mode='Markdown')
            elif args[0] == 'True':
                bot.send_message(message.chat.id,'*Оплата успiшна*',parse_mode='Markdown')
                try:
                    def generate_one_time_invite_link():
                        invite_link = bot.create_chat_invite_link(
                            chat_id='-1001881688132',
                            member_limit=1
                        )
                        Log(text=invite_link)
                        return invite_link.invite_link
                    invite_link = generate_one_time_invite_link()
                    bot.send_message(message.chat.id, invite_link, reply_markup=menu_button(menu_list), parse_mode='Markdown')
                    asyncio.run(subscription_timer(bot,message.chat.id, int(args[1])))
                except:
                    Log(error=traceback.format_exc())
                    bot.send_message(message.chat.id, error_invinte, reply_markup=menu_button(menu_list), parse_mode='Markdown')

@bot.message_handler(content_types=['text', 'photo', 'video', 'document'])
def broadcasts(message):
    users = db.get_all_users()
    total_users = len(users)
    sent_count = 0

    if message.text and ':' in message.text or message.caption and ':' in message.caption:
        initial_text = "Рассылка началась:\n0%"
        sent_message = bot.send_message(message.chat.id, initial_text)

        for user in users:
            try:
                if message.text:
                    bot.send_message(user[0], message.text)
                elif message.content_type == 'photo':
                    bot.send_photo(user[0], message.photo[-1].file_id, caption=message.caption)
                elif message.content_type == 'video':
                    bot.send_video(user[0], message.video.file_id, caption=message.caption)
                elif message.content_type == 'document':
                    bot.send_document(user[0], message.document.file_id, caption=message.caption)

                sent_count += 1
                config.Log(message=message, text=f'Пользователю @{user[1]} отправлено сообщение  # {message.text or message.caption} #', error=None)

                progress = int(sent_count / total_users * 100)
                updated_text = f"Рассылка началась:\n{progress}%"
                bot.edit_message_text(updated_text, message.chat.id, sent_message.message_id)

            except Exception as e:
                config.Log(message=message, text=f"Ошибка отправки сообщения пользователю @{user[1]}: {str(e)}", error=None)

        bot.send_message(message.chat.id, "Рассылка завершена")
    else:
        continue

    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        if message.chat.id in admins:
            bot.send_message(message.chat.id, admin_panel_text, reply_markup=menu_button(admin_menu_list), parse_mode='Markdown')

    @bot.message_handler(content_types=['text'])
    def handle_button_press(message):
        Log(message=message)
        try:
            if message.text == '↩️Назад в меню':
                Log(message=message, text=message.text, error=None)
                bot.send_message(message.chat.id, '*Вертаю..*', reply_markup=menu_button(menu_list), parse_mode='Markdown')
            elif message.text == 'Клуб тренувань Act Today 🔥':
                Log(message=message, text=message.text, error=None)
                bot.send_message(message.chat.id, text, reply_markup=menu_button(club_list), parse_mode='Markdown')
            elif message.text == 'Підписка 🍎':
                keyboard = inline_button(price)
                bot.send_message(message.chat.id, '*Підписка*', reply_markup=keyboard, parse_mode='Markdown')
            elif message.text == "Зв’язок з автором/підтримка ✍":
                keyboard = inline_button(helper_list)
                bot.send_message(message.chat.id, '*Зв\'язок з автором/підтримкою*', reply_markup=keyboard, parse_mode='Markdown')
            elif message.text == 'Часті запитання ❓':
                keyboard = inline_button(ask_list)
                bot.send_message(message.chat.id, '*Часті запитання*', reply_markup=keyboard, parse_mode='Markdown')
            elif message.text == 'Клуб тренувань ActToday🏋️':
                keyboard = inline_button(price)
                bot.send_message(message.chat.id, '*Підписка*', reply_markup=keyboard, parse_mode='Markdown')
            elif message.text == 'Безкоштовне пробне тренування 💜':
                bot.send_message(message.chat.id, 'https://www.youtube.com/watch?v=8UMEfg6pvDo',reply_markup=menu_button(menu_list))
            
            elif message.text == "Розпочати розсилання":
                msg=bot.send_message(message.chat.id, 'Напишiть текст або фото з текстом у форматi (Адмiнiстарор):(ваш текст)')
                bot.register_next_step_handler(msg, broadcasts)
            
            else:
                for user in db_read():
                    if message.chat.id in admins:
                        Log(message=message, text=message.text, error=None)
                        bot.send_message(user[1], message.text, reply_markup=menu_button(menu_list), parse_mode='Markdown')
                # Handle unknown button press
                pass
        except:
            Log(error=traceback.format_exc())

    if __name__ == '__main__':
            while True:
                try:
                    bot.polling(none_stop=True, timeout=60)
                except:
                    Log(error=traceback.format_exc())
                    break
    

if __name__ == '__main__':
    tasks=[]
    asyncio.run(main(bot))