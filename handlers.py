import ephem

from cities_functions import (handle_city)
from dateutil.parser import parse
from glob import glob
from random import choice
from utils import get_smile, main_keyboard, play_random_numbers


def greet_user(update, context):
    print("Вызван /start")
    context.user_data["emoji"] = get_smile(context.user_data)
    update.message.reply_text(
        f"Здравствуй пользователь {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )


def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)


def talk_to_me(update, context):
    context.user_data["emoji"] = get_smile(context.user_data)
    username = update.effective_user.first_name
    text = update.message.text
    update.message.reply_text(
        f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {text}",
        reply_markup=main_keyboard()
    )


def send_cat_picture(update, context):
    cat_photos_list = glob("images/cat*.jp*g")
    cat_photo_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(cat_photo_filename, "rb"),
        reply_markup=main_keyboard()
    )


def user_coordinates(update, context):
    context.user_data["emoji"] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )


def word_count(update, context):
    if len(context.args) > 0:
        count_words = len(context.args)
        message = f"{count_words} слова"
    else:
        message = "Введите строку"
    update.message.reply_text(message)


def next_full_moon(update, context):
    if context.args:
        try:
            today = parse(context.args[0])
            next_full_moon_date = ephem.next_full_moon(today)
            message = f"Ближайшее полнолуние {next_full_moon_date}"
        except(TypeError, ValueError):
            message = "Введите дату"
    else:
        message = "Введите дату"
    update.message.reply_text(message)


def cities(update, context):
    if context.args:
        try:
            message = handle_city(update, context)
        except(TypeError, ValueError):
            message = "Введите город"
    else:
        message = "Введите город"
    update.message.reply_text(message)
