from aiogram.types.bot_command import BotCommand


START_COMMAND = BotCommand(command="start", description="Starts the bot fresh and clean.")
TEST_COMMAND = BotCommand(command="test", description="Gives you a maths test.")
GAME_START_COMMAND = BotCommand(command="game", description="Plays a quiz game.")
GAME_GUESS_COMMAND = BotCommand(command="guess_number", description="Guess the number. You have 5 tries.")