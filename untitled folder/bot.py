import asyncio
import time
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, URLInputFile
from secret import GAMEBOTTOKEN
from commands import START_COMMAND, TEST_COMMAND, GAME_START_COMMAND, GAME_GUESS_COMMAND
from aiogram.fsm.context import FSMContext
from fsm_models import *
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from random import randint
from keyboard import *


TOKEN = getenv(GAMEBOTTOKEN)

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)} {message.from_user.id}! \nI am a bot that can test your math skills and play a game for you! 🟰🎮")

@dp.message(Command("test"))
async def command_test(msg: Message, state:FSMContext):
    await state.set_state(TestForm.q1)
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=str(randint(0, 3))+"."+str(randint(0, 3))+" Liters")
    keyboard.button(text=read_txt()[0])
    keyboard.button(text=str(randint(1, 4))+"."+str(randint(1, 3))+" Liters")
    await msg.answer("Write 100 milliliters as a decimal.", reply_markup=keyboard.as_markup())

@dp.message(TestForm.q1)
async def question_1(msg: Message, state:FSMContext):
    if msg.text == read_txt()[0]:
        await msg.answer("Correct!")
        await state.set_state(TestForm.q2)
        keyboard = ReplyKeyboardBuilder()
        keyboard.button(text=str(randint(0, 3))+"."+str(randint(0, 3))+" Miles")
        keyboard.button(text=str(randint(1, 4))+"."+str(randint(1, 3))+" Miles")
        keyboard.button(text=read_txt()[1])
        await msg.answer("A man has walked one mile north and then a quarter mile south. How far is he from the starting point?", reply_markup=keyboard.as_markup())
    else:
        await msg.answer("Try again!")

@dp.message(TestForm.q2)
async def question_2(msg: Message, state:FSMContext):
    if msg.text == read_txt()[1]:
        await msg.answer("Correct!")
        await state.set_state(TestForm.q3)
        keyboard = ReplyKeyboardBuilder()
        keyboard.button(text=read_txt()[2])
        keyboard.button(text="The Brother")
        keyboard.button(text="The Sister")
        await msg.answer("The brother was born in the spring, and the sister was born in the summer. Which one is older?", reply_markup=keyboard.as_markup())
    else:
        await msg.answer("Try again!")

@dp.message(TestForm.q3)
async def question_3(msg: Message, state:FSMContext):
    if msg.text == read_txt()[2]:
        await msg.answer("Correct!")
        await state.set_state(TestForm.q4)
        keyboard = ReplyKeyboardBuilder()
        keyboard.button(text="4")
        keyboard.button(text=read_txt()[3])
        keyboard.button(text="3")
        await msg.answer("Imagine a square with straight lines drawn through the midpoints of the sides. How many squares do we have now?", reply_markup=keyboard.as_markup())
    else:
        await msg.answer("Try again!")

@dp.message(TestForm.q4)
async def question_4(msg: Message, state:FSMContext):
    if msg.text == read_txt()[3]:
        await msg.answer("Correct!")
        await state.set_state(TestForm.q5)
        keyboard = ReplyKeyboardBuilder()
        keyboard.button(text="129")
        keyboard.button(text=read_txt()[4])
        keyboard.button(text="1,569")
        await msg.answer("77x75x92x17x0x82x99?", reply_markup=keyboard.as_markup())
    else:
        await msg.answer("Try again!")

@dp.message(TestForm.q5)
async def question_5(msg: Message, state:FSMContext):
    if msg.text == read_txt()[4]:
        await msg.answer("Correct!", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        
    else:
        await msg.answer("Try again!")


@dp.message(Command("game"))
async def game_quiz(message:Message, state:FSMContext):
    await state.set_state(GameForm.q1)
    await message.answer_photo(caption="Right! A game. Here's a quick adventure quiz!\n\nYou are walking through a forest when you\nstumble across a chest. Do you open it? (Y/N)", photo="https://staticg.sportskeeda.com/editor/2022/04/9377e-16487527787276-1920.jpg")

@dp.message(GameForm.q1)
async def chest_question(message:Message, state:FSMContext):
    await state.update_data(q1=message.text)
    if message.text.upper() == "Y":
        photo = FSInputFile("portal.jpg")
        await state.set_state(GameForm.q1cont)
        await message.answer_photo(caption="You open the chest, only to find a portal\nand three potions. Do you take the potions? (Y/N)", photo=photo)
    elif message.text.upper() == "N":
        await state.set_state(GameForm.q2)
        await message.answer_photo(caption="You continue walking without touching the chest, deeper into the dark forest and see a man that tells you not to go any further. Do you listen? (Y/N)", photo="https://api.deepai.org/job-view-file/13fa94ed-a7c4-4978-a37f-b048dd9f7d92/outputs/output.jpg")
    else:
        await message.answer("Please enter Y or N (Yes No)")

@dp.message(GameForm.q1cont)
async def potion_question(message:Message, state:FSMContext):
    await state.update_data(q1cont=message.text)
    if message.text.upper() == "Y":
        await state.set_state(GameForm.q3)
        await message.answer_photo(caption="You take the shiny potions and enter the portal. You get\nteleported to 1992 and notice a monster. Do you fight it or drink the first potion? (D/F)", photo="https://api.deepai.org/job-view-file/2878cc75-070d-466d-8710-c5f8af4feebb/outputs/output.jpg")
    elif message.text.upper() == "N":
        await state.set_state(GameForm.qe)
        await message.answer_photo(caption="You leave the potions and enter the portal, which teleports you away... (send anything to continue)", photo="https://api.deepai.org/job-view-file/3ddaa45e-7e7c-4976-bfd5-8c8ace824956/outputs/output.jpg")
    else:
        await message.answer("Please enter Y or N (Yes No)")

@dp.message(GameForm.q2)
async def listen_question(message:Message, state:FSMContext):
    await state.update_data(q2=message.text)
    if message.text.upper() == "Y":
        await state.set_state(GameForm.q3)
        await message.answer_photo(caption="You turn around to go home, but then, a bird picks you up and throws you into a battle arena, where a monster is waiting. The bird gives you potions, so will you fight or drink it to see what happens? (D/F)", photo="https://api.deepai.org/job-view-file/2878cc75-070d-466d-8710-c5f8af4feebb/outputs/output.jpg")
    elif message.text.upper() == "N":
        await state.set_state(GameForm.q3)
        await message.answer_photo(caption="You keep going forward into an arena with a monster. You feel someting heavy in your pocket and realize it's a potion. Do you drink it or fight the monster? (D/F)", photo="https://api.deepai.org/job-view-file/3ddaa45e-7e7c-4976-bfd5-8c8ace824956/outputs/output.jpg")
    else:
        await message.answer("Please enter Y or N (Yes No)")

@dp.message(GameForm.q3)
async def drink_fight_question(message:Message, state:FSMContext):
    await state.update_data(q3=message.text)
    if message.text.upper() == "D":
        await state.set_state(GameForm.qe)
        await message.answer_photo(caption="You drink the potion and dissapear... (send anything to continue)", photo="https://api.deepai.org/job-view-file/2878cc75-070d-466d-8710-c5f8af4feebb/outputs/output.jpg")
    elif message.text.upper() == "F":
        await state.set_state(GameForm.qe)
        await message.answer_photo(caption="You fight the monster with a sword you found on the floor and win... (send anything to continue)", photo="https://api.deepai.org/job-view-file/3ddaa45e-7e7c-4976-bfd5-8c8ace824956/outputs/output.jpg")
    else:
        await message.answer("Please enter D or F (Drink Fight)")

@dp.message(GameForm.qe)
async def end(message:Message, state:FSMContext):
    await state.update_data(qe=message.text)
    await message.answer_video("https://v.ftcdn.net/10/18/77/93/700_F_1018779357_gjioNpiS0pFHiuPrfnDkltJ9RGIcstFa_ST.mp4", caption="The End!")
    await state.clear()

level = 1
secret = randint(1, level*50)
guesses = 5



@dp.message(Command("guess_number"))
async def guess_the_number(message:Message, state:FSMContext):
    await message.answer(f"Guess my number from 1 to {level*50}.")
    await state.set_state(NumberForm.l1)

async def process_guess(message: Message, state: FSMContext, next_state: State, next_level: int):
    global guesses, level, secret
    num = message.text

    if guesses > 0:
        if num.isdigit():
            num = int(num)
            if 1 <= num <= level * 50:
                if num > secret:
                    await message.answer("Your number is too BIG!")
                    guesses -= 1
                    await message.answer(f"You have {guesses} guess(es).")
                elif num < secret:
                    await message.answer("Your number is too SMALL!")
                    guesses -= 1
                    await message.answer(f"You have {guesses} guess(es).")
                else:
                    await message.answer("Your number is correct!")
                    level = next_level
                    time.sleep(0.00000001)
                    guesses = guesses+3
                    secret = randint(1, level * 50)
                    await state.set_state(next_state)
                    await message.answer(f"Guess my number from 1 to {level * 50}.")
            else:
                await message.answer(f"Your number is out of bounds (1-{level * 50})!")
        else:
            await message.answer("Please enter a valid number!")
    else:
        if num.isdigit():
            num = int(num)
            if 1 <= num <= level * 50:
                if num > secret:
                    await message.answer("Your number is too BIG!")
                    await message.answer("You ran out of guesses!")
                    await message.answer(f"You have {guesses} guess(es).")
                    guesses = 5
                elif num < secret:
                    await message.answer("Your number is too SMALL!")
                    await message.answer(f"You have {guesses} guesses.")
                    await message.answer("You ran out of guesses!")
                    guesses = 5
                else:
                    await message.answer("Your number is correct!")
                    level = next_level
                    guesses += 3
                    secret = randint(1, level * 50)
                    await state.set_state(next_state)
                    await message.answer(f"Guess my number from 1 to {level * 50}.")
            else:
                await message.answer(f"Your number is out of bounds (1-{level * 50})!")
        else:
            await message.answer("Please enter a valid number!")
        

@dp.message(NumberForm.l1)
async def guess_level_1(message: Message, state: FSMContext):
    await process_guess(message, state, NumberForm.l2, 2)

@dp.message(NumberForm.l2)
async def guess_level_2(message: Message, state: FSMContext):
    await process_guess(message, state, NumberForm.l3, 3)

@dp.message(NumberForm.l3)
async def guess_level_3(message: Message, state: FSMContext):
    await process_guess(message, state, NumberForm.l4, 4)

@dp.message(NumberForm.l4)
async def guess_level_4(message: Message, state: FSMContext):
    await process_guess(message, state, NumberForm.l5, 5)

@dp.message(NumberForm.l5)
async def guess_level_5(message: Message, state: FSMContext):
    await process_guess(message, state, NumberForm.l6, 6)

@dp.message(NumberForm.l6)
async def guess_level_6(message: Message, state: FSMContext):
    await process_guess(message, state, NumberForm.l7, 7)

@dp.message(NumberForm.l7)
async def guess_level_7(message: Message, state: FSMContext):
    await process_guess(message, state, NumberForm.l8, 8)

@dp.message(NumberForm.l8)
async def guess_level_8(message: Message, state: FSMContext):
    await process_guess(message, state, NumberForm.l9, 9)

@dp.message(NumberForm.l9)
async def guess_level_9(message: Message, state: FSMContext):
    await process_guess(message, state, NumberForm.l10, 10)

@dp.message(NumberForm.l10)
async def guess_level_10(message: Message, state: FSMContext):
    await process_guess(message, state, NumberForm.l10, 10)
    await state.clear()
    await message.answer("🎉🎉🎉🎉🎉🎉🎉🎉!YOU WIN!🎉🎉🎉🎉🎉🎉🎉🎉")

# @dp.message(NumberForm.l1)
# async def guess_the_number_level_1(message:Message, state:FSMContext):
#     global guesses, level, secret
#     num = message.text
#     if guesses > 0:
#         if num.isdigit():
#             num = int(message.text)
#             if 1 <= num <= level*50:
#                 if num > secret:
#                     await message.answer("Your number is too BIG!")
#                     guesses-=1
#                 elif num < secret:
#                     await message.answer("Your number is too SMALL!")
#                     guesses-=1
#                 else:
#                     await message.answer("Your number is correct!")
#                     guesses = 5
#                     await state.set_state(NumberForm.l2)
#                     level = 2
#                     secret = randint(1, level*50)
#                     await message.answer(f"Guess my number from 1 to {level*50}.")
#             else:
#                 await message.answer(f"Your number is out of bounds (1-{level*50})!")
#         else:
#             await message.answer("Your text is not a integer!")
#     else:
#         await message.answer("You ran out of guesses!")
#         guesses = 5
#         await state.clear()

# @dp.message(NumberForm.l2)
# async def guess_the_number_level_1(message:Message, state:FSMContext):
#     global guesses, level, secret
#     num = message.text
#     if guesses > 0:
#         if num.isdigit():
#             num = int(message.text)
#             if 1 <= num <= level*50:
#                 if num > secret:
#                     await message.answer("Your number is too BIG!")
#                     guesses-=1
#                 elif num < secret:
#                     await message.answer("Your number is too SMALL!")
#                     guesses-=1
#                 else:
#                     await message.answer("Your number is correct!")
#                     guesses = 5
#                     await state.set_state(NumberForm.l3)
#                     level = 3
#                     secret = randint(1, level*50)
#                     await message.answer(f"Guess my number from 1 to {level*50}.")
#             else:
#                 await message.answer(f"Your number is out of bounds (1-{level*50})!")
#         else:
#             await message.answer("Your text is not a integer!")
#     else:
#         await message.answer("You ran out of guesses!")
#         guesses = 5
#         await state.clear()

# @dp.message(NumberForm.l3)
# async def guess_the_number_level_1(message:Message, state:FSMContext):
#     global guesses, level, secret
#     num = message.text
#     if guesses > 0:
#         if num.isdigit():
#             num = int(message.text)
#             if 1 <= num <= level*50:
#                 if num > secret:
#                     await message.answer("Your number is too BIG!")
#                     guesses-=1
#                 elif num < secret:
#                     await message.answer("Your number is too SMALL!")
#                     guesses-=1
#                 else:
#                     await message.answer("Your number is correct!")
#                     guesses = 5
#                     await state.set_state(NumberForm.l4)
#                     level = 4
#                     secret = randint(1, level*50)
#                     await message.answer(f"Guess my number from 1 to {level*50}.")
#             else:
#                 await message.answer(f"Your number is out of bounds (1-{level*50})!")
#         else:
#             await message.answer("Your text is not a integer!")
#     else:
#         await message.answer("You ran out of guesses!")
#         guesses = 5
#         await state.clear()


async def main() -> None:   
    bot = Bot(token=GAMEBOTTOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands([START_COMMAND, TEST_COMMAND, GAME_START_COMMAND, GAME_GUESS_COMMAND])
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())