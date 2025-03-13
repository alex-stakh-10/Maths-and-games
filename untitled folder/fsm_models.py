from aiogram.fsm.state import State, StatesGroup

class TestForm(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()

class GameForm(StatesGroup):
    q1 = State()
    q1cont = State()
    q2 = State()
    q3 = State()
    qe = State()

class NumberForm(StatesGroup):
    l1 = State()
    l2 = State()
    l3 = State()
    l4 = State()
    l5 = State()
    l6 = State()
    l7 = State()
    l8 = State()
    l9 = State()
    l10 = State()
    