import logging

from glob import glob
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint, choice
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError, ValueError):
            message = 'Введите целое число'
    else:
        message = 'Введите число'
    update.message.reply_text(message)

def talk_to_me(update, context):
    print(context.args)
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ваше число {user_number}, мое {bot_number}. Вы выиграли'
    elif user_number == bot_number:
        message = f'Ваше число {user_number}, мое {bot_number}. Ничья'
    else:
        message = f'Ваше число {user_number}, мое {bot_number}. Вы проиграли'
    return message

def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'))
    pass

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()