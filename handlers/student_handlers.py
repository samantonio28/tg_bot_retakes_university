from aiogram import Router
from aiogram.filters import BaseFilter, Text, Command
from aiogram.types import Message, CallbackQuery
from keyboards import keyboards as kbs
from config_data.config import load_config

config = load_config()
admin_list: list[int] = config.tg_bot.admin_ids
student_list: list[int] = config.tg_bot.student_ids

class IsStudent(BaseFilter):
    def __init__(self, admin_list: list[int], student_list: list[int]):
        self.admin_list = admin_list
        self.student_list = student_list
    async def __call__(self, message: Message):
        return message.from_user.id \
                in self.admin_list + self.student_list
    
router: Router = Router()
router.message.filter(IsStudent(admin_list, student_list))

@router.message(Command('start'))
async def student_info(message: Message):
    await message.answer(text="Вы - студент")

@router.message(Text("только студент"))
async def secret_function(message: Message):
    await message.answer(text="да, да, эта функция доступна только студенту")