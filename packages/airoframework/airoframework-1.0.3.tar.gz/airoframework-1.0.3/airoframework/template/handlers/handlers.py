from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from config.states import UserStates
from utils.utils import add_user, set_user_state

router = Router()

@router.message(Command('start'))
async def start_handler(message: Message, state: FSMContext, bot: Bot):
    await message.reply('Welcome to the bot')