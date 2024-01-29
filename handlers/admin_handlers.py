from aiogram import Router
from aiogram.filters import BaseFilter, Text, Command, StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove as Rep_Rem
from config_data.config import Config, load_config
import keyboards.keyboards as kbs
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from dotenv import find_dotenv, set_key, load_dotenv
from os import environ

config: Config = load_config()
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

admin_list: list[int] = config.tg_bot.admin_ids

class IsAdmin(BaseFilter):
    def __init__(self, admin_list: list[int]) -> None:
        self.admin_list = admin_list
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_list

router: Router = Router()
router.message.filter(IsAdmin(admin_list))

"""
Что должен уметь только админ?
1) добавить пользователя:
- админа
- препода
- студента
2) удалить пользователя
- препода
- студента
уже умеем #####################################
3) видеть статистику по каким-то параметрам

"""

class UserToAdd(StatesGroup):
    user = State()
    id_number = State()

class UserToDel(StatesGroup):
    id_number = State()

@router.message(Command('start'))
async def admin_start(message: Message):
    await message.answer(
        text="Приветствую Вас в боте! Вы являетесь админом и можете "
             "воспользоваться панелью админа по команде /admin_menu"
    )

@router.message(Command('admin_menu'))
async def process_admin_menu(message: Message):
    await message.answer(
        text='Выберите, что хотите сделать',
        reply_markup=kbs.admin_menu
    )

@router.callback_query(Text("cancel_admin_menu"))
async def cancel_admin_menu(callback: CallbackQuery):
    await callback.message.answer(
        text="Отмена\nНапоминаю, /admin_menu откроет панель админа.",
        reply_markup=Rep_Rem()
    )

@router.callback_query(Text('admin_stats_pressed'))
async def process_admin_stats(callback: CallbackQuery):
    admins = environ["ADMIN_IDS"].rstrip(',').split(',') if environ.get("ADMIN_IDS") else []
    tutors = environ["TUTOR_IDS"].rstrip(',').split(',') if environ.get("TUTOR_IDS") else []
    students = environ["STUDENT_IDS"].rstrip(',').split(',') if environ.get("STUDENT_IDS") else []
    text_to_send = ''
    text_to_send += "Статистика\n"
    text_to_send += f"Всего пользователей: {len(admins) + len(tutors) + len(students)}\n"
    text_to_send += f"  Админы: ({len(admins)} чел.)\n"
    if len(admins) > 0:
        for i, id_num in enumerate(admins):
            text_to_send += f"{i+1:<3} {id_num:<11}\n"
    text_to_send += f"  Преподаватели: ({len(tutors)} чел.)\n"
    if len(tutors) > 0:
        for i, id_num in enumerate(tutors):
            text_to_send += f"{i+1:<3}  {id_num:<11}\n"
    text_to_send += f"  Студенты: ({len(students)} чел.)\n"
    if len(students) > 0:
        for i, id_num in enumerate(students):
            text_to_send += f"{i+1:<3}  {id_num:<11}\n"
    await callback.message.answer(
        text=text_to_send,
        reply_markup=kbs.admin_menu
    )

@router.callback_query(Text('add_user_pressed'), StateFilter(default_state))
async def start_add_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Выберите роль нового пользователя',
        reply_markup=kbs.new_user_kd)
    await state.set_state(UserToAdd.user)

@router.callback_query(Text('admin_chosen'), StateFilter(UserToAdd.user))
async def user_chosen(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user='ADMIN_IDS')
    await callback.message.answer(
        text="Введите id нового админа (натуральное число)",
        reply_markup=kbs.cancel_put_id_kd
    )
    await state.set_state(UserToAdd.id_number)

@router.callback_query(Text('tutor_chosen'), StateFilter(UserToAdd.user))
async def tutor_chosen(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user='TUTOR_IDS')
    await callback.message.answer(
        text="Введите id нового преподавателя (натуральное число)",
        reply_markup=kbs.cancel_put_id_kd
    )
    await state.set_state(UserToAdd.id_number)

@router.callback_query(Text('student_chosen'), StateFilter(UserToAdd.user))
async def student_chosen(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user='STUDENT_IDS')
    await callback.message.answer(
        text="Введите id нового студента (натуральное число)",
        reply_markup=kbs.cancel_put_id_kd
    )
    await state.set_state(UserToAdd.id_number)

@router.callback_query(Text('cancel_put_id_pressed'), StateFilter(UserToAdd.id_number))
async def cancel_put_id(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        text='Выберите, что хотите сделать',
        reply_markup=kbs.admin_menu
    )

@router.message(lambda message: not message.text.isdigit(), StateFilter(UserToAdd.id_number))
async def got_wrong_id(message: Message, state: FSMContext):
    await message.answer(
        text='Введённое значение некорректно, попробуйте еще раз',
        reply_markup=kbs.cancel_put_id_kd
    )

def id_exists(id_number: str) -> bool:
    admins = environ["ADMIN_IDS"].rstrip(',').split(',')
    tutors = environ["TUTOR_IDS"].rstrip(',').split(',')
    students = environ["STUDENT_IDS"].rstrip(',').split(',')
    return id_number in admins or id_number in tutors or id_number in students

@router.message(lambda message: id_exists(message.text), StateFilter(UserToAdd.id_number))
async def id_already_exists(message: Message, state: FSMContext):
    await message.answer(text="Пользователь уже числится в базе, введите другой id")

@router.message(StateFilter(UserToAdd.id_number))
async def get_id(message: Message, state: FSMContext):
    await state.update_data(id_number=message.text)
    user = await state.get_data()
    user_env, user_id = user["user"], user["id_number"]
    current_ids = environ[user_env].rstrip(',').split(',') if environ.get(user_env) else []
    if user_id not in current_ids:
        current_ids.append(user_id)
    environ[user_env] = ','.join(current_ids)
    set_key(dotenv_file, user_env, environ[user_env])
    word = ''
    if user_env == 'ADMIN_IDS':
        word = 'Админ'
    elif user_env == 'TUTOR_IDS':
        word = 'Преподаватель'
    elif user_env == 'STUDENT_IDS':
        word = 'Студент'
    await message.answer(
        text=f"{word} {user_id} успешно добавлен", 
        reply_markup=kbs.admin_menu
    )
    await state.clear()

@router.callback_query(Text('del_user_pressed'), StateFilter(default_state))
async def start_del_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Введите id удаляемого пользователя',
        reply_markup=kbs.cancel_put_id_kd
    )
    await state.set_state(UserToDel.id_number)

@router.callback_query(Text('cancel_put_id_pressed'), StateFilter(UserToDel.id_number))
async def cancel_put_id(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        text='Выберите, что хотите сделать',
        reply_markup=kbs.admin_menu
    )

@router.message(lambda message: not message.text.isdigit(), StateFilter(UserToDel.id_number))
async def got_wrong_id(message: Message, state: FSMContext):
    await message.answer(
        text='Введённое значение некорректно, попробуйте еще раз',
        reply_markup=kbs.cancel_put_id_kd
    )

def not_id_exists(id_number: str) -> bool:
    tutors = environ["TUTOR_IDS"].rstrip(',').split(',')
    students = environ["STUDENT_IDS"].rstrip(',').split(',')
    return not (id_number in tutors or id_number in students)

@router.message(lambda message: not_id_exists(message.text), StateFilter(UserToDel.id_number))
async def not_id_in_db(message: Message, state: FSMContext):
    await message.answer(
        text="Пользователь не числится в базе преподавателей и студентов, введите другой id",
        reply_markup=kbs.cancel_put_id_kd
    )
    
@router.message(StateFilter(UserToDel.id_number))
async def del_user(message: Message, state: FSMContext):
    await state.update_data(id_number=message.text)
    user = await state.get_data()
    user_id = user["id_number"]
    tutors = environ["TUTOR_IDS"].rstrip(',').split(',') if environ.get("TUTOR_IDS") else []
    students = environ["STUDENT_IDS"].rstrip(',').split(',') if environ.get("STUDENT_IDS") else []
    if user_id in tutors:
        tutors.remove(user_id)
        user_env = "TUTOR_IDS"
        environ[user_env] = ','.join(tutors)
    elif user_id in students:
        students.remove(user_id)
        user_env = "STUDENT_IDS"
        environ[user_env] = ','.join(students)
    set_key(dotenv_file, user_env, environ[user_env])
    if user_env == 'TUTOR_IDS':
        word = 'Преподаватель'
    elif user_env == 'STUDENT_IDS':
        word = 'Студент'
    await message.answer(
        text=f"{word} {user_id} успешно удален", 
        reply_markup=kbs.admin_menu
    )
    await state.clear()

    # 1191974231 1092594784