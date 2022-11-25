import operator
import re

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '^': operator.xor,
}


def get_calc_parts(user_expression):
    regular_result = re.findall(r"^(\d+)([-+*]|/(?!0))(\d+)$", user_expression)
    if not regular_result[0]:
        return False
    return {
        "operand_1": int(regular_result[0][0]),
        "math_symbol":  regular_result[0][1],
        "operand_2":  int(regular_result[0][2]),
    }


def calc(update, context):
    if context.args:
        parts = get_calc_parts(context.args[0])
        if not parts:
            message = "Выражение не верно"
        else:
            result = ops[parts["math_symbol"]](parts["operand_1"], parts["operand_2"])
            message = f"Результат {result}"

    else:
        message = "Введите выражение"
    update.message.reply_text(message)