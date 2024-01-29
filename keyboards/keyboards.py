from aiogram.types import InlineKeyboardButton as Inl_B, \
                          InlineKeyboardMarkup as Inl_Markup
from aiogram.types import KeyboardButton as Key_B, \
ReplyKeyboardMarkup as Rep_Markup

admin_stats: Inl_B = Inl_B(
    text='Статистика',
    callback_data='admin_stats_pressed'
)

admin_user: Inl_B = Inl_B(
    text='Админ',
    callback_data='admin_chosen'
)

tutor_user: Inl_B = Inl_B(
    text='Преподаватель',
    callback_data='tutor_chosen'
)

student_user: Inl_B = Inl_B(
    text='Студент',
    callback_data='student_chosen'
)

new_user_kd: Inl_Markup = Inl_Markup(
    inline_keyboard=[
        [admin_user], 
        [tutor_user], 
        [student_user]
    ]
)

# del_user_kd: Inl_Markup = Inl_Markup(
#     inline_keyboard=[
#         [tutor_user],
#         [student_user]
#     ]
# )

add_user: Inl_B = Inl_B(
    text='Добавить пользователя',
    callback_data='add_user_pressed'
)

del_user: Inl_B = Inl_B(
    text='Удалить пользователя',
    callback_data='del_user_pressed'
)

cancel_admin_menu: Inl_B = Inl_B(
    text="Отмена",
    callback_data="cancel_admin_menu"
)

admin_menu: Inl_Markup = Inl_Markup(
    inline_keyboard=[
        [admin_stats],
        [add_user], 
        [del_user],
        [cancel_admin_menu]
    ]
)

cancel_put_id: Inl_B = Inl_B(
    text='Отмена', 
    callback_data='cancel_put_id_pressed'
)

cancel_put_id_kd: Inl_Markup = Inl_Markup(
    inline_keyboard=[
        [cancel_put_id]
    ]
)