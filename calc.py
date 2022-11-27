import operator
import re

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

FIRST_ELEMENT_REGEX = r"^[-+]*(\d+)"
VALIDATE_EXPRESSION_REGEX = r"^(([-+*]|/(?!0))(\d+))+$"
GET_ELEMENTS_EXPRESSION_REGEX = r"([-+*]|/(?!0))(\d+)"


def get_calc_parts(user_expression):
    elements = []
    try:
        first_element = re.match(FIRST_ELEMENT_REGEX, user_expression).group(0)
    except BaseException:
        return False
    elements.append(int(first_element))
    user_expression = user_expression.replace(first_element, "", 1)
    is_expression_valid = re.match(VALIDATE_EXPRESSION_REGEX, user_expression)
    if is_expression_valid is None:
        return False
    remaining_elements = re.findall(GET_ELEMENTS_EXPRESSION_REGEX, user_expression)
    for group in remaining_elements:
        for element in group:
            try:
                elements.append(int(element))
            except ValueError:
                elements.append(element)
    return elements


def one_pass(parts):
    for i, element in enumerate(parts, start=0):
        if element in ops.keys():
            result = ops[element](parts[i - 1], parts[i + 1])
            parts[i - 1] = result
            del parts[i]
            del parts[i]
    return parts


def calc(update, context):
    if context.args:
        parts = get_calc_parts(context.args[0])
        if not parts:
            message = "Выражение не верно"
        else:
            while len(parts) > 1:
                while '*' in parts or '/' in parts:
                    parts = one_pass(parts)
                while '+' in parts or '-' in parts:
                    parts = one_pass(parts)
            message = parts[0]
    else:
        message = "Введите выражение"
    update.message.reply_text(message)


def calc2(update, context):
    if context.args:
        if not context.args[0]:
            message = "Выражение не верно"
        else:
            try:
                message = calculation(context.args[0])
            except ZeroDivisionError:
                message = "Деление на ноль невозможно"
    else:
        message = "Введите выражение"
    update.message.reply_text(message)


def calculation(user_input: str) -> str:
    if len(user_input) < 3:
        return "Слишком коротко."

    for symbol_ in user_input:
        if symbol_ not in "0123456789-+/* ":
            return "Ты ввёл НЕ только цифры и операторы!"

    if not any(calc_operator in user_input for calc_operator in ["+", "-", "*", "/"]):
        return "Ты НЕ ввёл оператор вычисления."

    result = eval(user_input)
    return f"Результат: {result:.2f}"
