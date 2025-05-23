from aiogram.fsm.state import State, StatesGroup, default_state


class ClientState(StatesGroup):
    default_state: State = default_state
    waiting_for_confirmation: State = State()
    waiting_for_row: State = State()

    confirm: State = State()
