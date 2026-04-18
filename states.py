from aiogram.fsm.state import StatesGroup, State

class StudentForm(StatesGroup):
    full_name = State()
    age = State()
    group = State()
    phone = State()
    address = State()
    interests = State()
