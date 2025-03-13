from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

def read_txt(file="answers.txt"):
    with open(file) as f:
        old_answer_list = f.readlines()
        answers = []
        for answer in old_answer_list:
            answers.append(answer.replace('\n', ''))
    return answers


print(read_txt())


# def question1()
# builder = InlineKeyboardBuilder()
# builder.adjust(1, repeat=True)