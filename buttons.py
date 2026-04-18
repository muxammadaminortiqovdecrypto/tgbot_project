from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Anketa to'ldirish"), KeyboardButton(text="👤 Mening ma'lumotlarim")],
        [KeyboardButton(text="📊 Guruh statistikasi"), KeyboardButton(text="🔍 O'quvchilarni qidirish")],
        [KeyboardButton(text="⚙️ Sozlamalar")]
    ],
    resize_keyboard=True,
)

contact_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Telefon raqamni ulashish", request_contact=True)]
    ],
    resize_keyboard=True,
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Barcha o'quvchilar"), KeyboardButton(text="📈 Statistika")],
        [KeyboardButton(text="🗑️ O'quvchini o'chirish"), KeyboardButton(text="📤 Ma'lumotlarni eksport qilish")],
        [KeyboardButton(text="🔙 Orqaga")]
    ],
    resize_keyboard=True,
)

def student_actions_keyboard(student_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✏️ Tahrirlash", callback_data=f"edit_{student_id}"),
                InlineKeyboardButton(text="🗑️ O'chirish", callback_data=f"delete_{student_id}")
            ],
            [
                InlineKeyboardButton(text="📊 Batafsil", callback_data=f"details_{student_id}")
            ]
        ]
    )

confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="confirm_yes"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="confirm_no")
        ]
    ]
)
