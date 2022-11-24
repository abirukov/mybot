import cities

NOT_VALID_LAST_LETTERS = ["ь", "ъ", "ё", "ы"]


def is_city_fits_condition(user_city, bot_last_city):
    return get_last_letter(bot_last_city) == user_city[0].lower()


def get_last_letter(city):
    for letter in reversed(city):
        if letter.lower() not in NOT_VALID_LAST_LETTERS:
            return letter.lower()


def handle_city(update, context):
    user_city = context.args[0]
    if "cities" not in context.user_data.keys():
        context.user_data["cities"] = []

    if user_city in context.user_data["cities"]:
        return "Такой город уже называли"

    if context.user_data["cities"] and not is_city_fits_condition(user_city, context.user_data["cities"][-1]):
        return f"Город не начинается на последнюю букву города {context.user_data['cities'][-1]}"

    context.user_data["cities"].append(user_city)
    user_city_last_char = get_last_letter(user_city)
    bot_city_variants = [
        city for city in cities.CITIES
        if city[0].lower() == user_city_last_char.lower()
    ]
    if not bot_city_variants:
        return "Я в тупике вы выиграли"

    context.user_data["cities"].append(bot_city_variants[0])
    return f"{bot_city_variants[0]}, ваш ход"
