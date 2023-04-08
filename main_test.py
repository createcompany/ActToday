import traceback
import telebot
import asyncio
import datetime
import json
from tetx import *
from telebot.types import InputMediaPhoto
from timerV2 import Timer, subscriptions, load_subscriptions, save_subscriptions, restore_timers

bot = telebot.TeleBot('6121940381:AAGLygbXhCIGRfXU-M6prlfg9D0uwGIzyM0')

bot.unban_chat_member(chat_id='-1001881688132', user_id='1709337743')
bot.unban_chat_member(chat_id='-1001881688132', user_id='5082791922')

admins = []

# Load subscriptions when the script starts
load_subscriptions()

async def main(bot):
    # Restore timers for all users
    restore_timers()

    # (The rest of the code in the "main" function remains the same)

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
            bot.send_message(message.chat.id, '*Оплата успiшна*', parse_mode='Markdown')
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

                user_id = message.chat.id
                days = int(args[1])
                subscription_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                # Save the subscription information
                subscriptions[user_id] = subscription_date
                save_subscriptions()

                # Start the timer for the subscription
                timer = Timer(user_id, subscription_date)
                timer.start()

            except:
                Log(error=traceback.format_exc())
                bot.send_message(message.chat.id, error_invinte, reply_markup=menu_button(menu_list), parse_mode='Markdown')

    # (The rest of the code remains the same)

if __name__ == '__main__':
    asyncio.run(main(bot))
