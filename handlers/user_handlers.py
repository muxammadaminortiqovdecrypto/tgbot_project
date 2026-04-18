import json
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from states import StudentForm
from buttons import main_menu, contact_button, student_actions_keyboard

router = Router()

def load_students():
    try:
        with open('students.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_students(students):
    with open('students.json', 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=2)

def get_student_by_id(user_id):
    students = load_students()
    for student in students:
        if student['user_id'] == user_id:
            return student
    return None

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    student = get_student_by_id(user_id)
    
    if student:
        await message.answer(
            f"Assalomu alaykum, {student['full_name']}! Siz allaqachon ro'yxatdan o'tgansiz.",
            reply_markup=main_menu
        )
    else:
        await message.answer(
            "Assalomu alaykum! O'quvchilar ma'lumotlar bazasiga xush kelibsiz!\n"
            "Iltimos, to'liq ismingizni kiriting:",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(StudentForm.full_name)

@router.message(StudentForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    full_name = message.text.strip()
    if len(full_name) < 3:
        await message.answer("Iltimos, to'liq ismingizni kamida 3 harfdan iborat bo'lishini kiriting:")
        return
    
    await state.update_data(full_name=full_name)
    await message.answer("Yoshingizni kiriting:")
    await state.set_state(StudentForm.age)

@router.message(StudentForm.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text.strip()
    if not age.isdigit() or int(age) < 10 or int(age) > 100:
        await message.answer("Iltimos, to'g'ri yosh kiriting (10-100 orasida):")
        return
    
    await state.update_data(age=int(age))
    await message.answer("Guruhiingizni kiriting (masalan: 201-guruh):")
    await state.set_state(StudentForm.group)

@router.message(StudentForm.group)
async def process_group(message: types.Message, state: FSMContext):
    group = message.text.strip()
    if len(group) < 2:
        await message.answer("Iltimos, guruh nomini to'g'ri kiriting:")
        return
    
    await state.update_data(group=group)
    await message.answer("Telefon raqamingizni ulashing:", reply_markup=contact_button)
    await state.set_state(StudentForm.phone)

@router.message(StudentForm.phone, F.contact)
async def process_phone_contact(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await message.answer("Manzilingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(StudentForm.address)

@router.message(StudentForm.phone)
async def process_phone_text(message: types.Message, state: FSMContext):
    phone = message.text.strip()
    if not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
        await message.answer("Iltimos, to'g'ri telefon raqamini kiriting:")
        return
    
    await state.update_data(phone=phone)
    await message.answer("Manzilingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(StudentForm.address)

@router.message(StudentForm.address)
async def process_address(message: types.Message, state: FSMContext):
    address = message.text.strip()
    if len(address) < 5:
        await message.answer("Iltimos, to'liq manzil kiriting (kamida 5 harf):")
        return
    
    await state.update_data(address=address)
    await message.answer("Qiziqishlaringizni kiriting (masalan: dasturlash, sport, musiqa):")
    await state.set_state(StudentForm.interests)

@router.message(StudentForm.interests)
async def process_interests(message: types.Message, state: FSMContext):
    interests = message.text.strip()
    if len(interests) < 3:
        await message.answer("Iltimos, qiziqishlaringizni kiriting:")
        return
    
    data = await state.get_data()
    user_id = message.from_user.id
    
    new_student = {
        'user_id': user_id,
        'full_name': data['full_name'],
        'age': data['age'],
        'group': data['group'],
        'phone': data['phone'],
        'address': data['address'],
        'interests': interests,
        'registration_date': message.date.isoformat()
    }
    
    students = load_students()
    students.append(new_student)
    save_students(students)
    
    await state.clear()
    await message.answer(
        f"Tabriklayman, {data['full_name']}! Siz muvaffaqiyatli ro'yxatdan o'tdingiz!\n\n"
        f"📝 To'liq ism: {data['full_name']}\n"
        f"🎂 Yosh: {data['age']}\n"
        f"👥 Guruh: {data['group']}\n"
        f"📱 Telefon: {data['phone']}\n"
        f"📍 Manzil: {data['address']}\n"
        f"🎯 Qiziqishlar: {interests}",
        reply_markup=main_menu
    )

@router.message(F.text == "📝 Anketa to'ldirish")
async def fill_form(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    student = get_student_by_id(user_id)
    
    if student:
        await message.answer("Siz allaqachon ro'yxatdan o'tgansiz. Ma'lumotlaringizni ko'rish uchun '👤 Mening ma'lumotlarim' tugmasini bosing.")
    else:
        await message.answer("Iltimos, to'liq ismingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(StudentForm.full_name)

@router.message(F.text == "👤 Mening ma'lumotlarim")
async def my_info(message: types.Message):
    user_id = message.from_user.id
    student = get_student_by_id(user_id)
    
    if student:
        info_text = (
            f"👤 *Sizning ma'lumotlaringiz:*\n\n"
            f"📝 *To'liq ism:* {student['full_name']}\n"
            f"🎂 *Yosh:* {student['age']}\n"
            f"👥 *Guruh:* {student['group']}\n"
            f"📱 *Telefon:* {student['phone']}\n"
            f"📍 *Manzil:* {student['address']}\n"
            f"🎯 *Qiziqishlar:* {student['interests']}\n"
            f"📅 *Ro'yxatdan o'tgan sana:* {student['registration_date']}"
        )
        await message.answer(info_text, parse_mode="Markdown")
    else:
        await message.answer("Siz hali ro'yxatdan o'tmagansiz. '📝 Anketa to'ldirish' tugmasini bosing.")

@router.message(F.text == "📊 Guruh statistikasi")
async def group_statistics(message: types.Message):
    students = load_students()
    
    if not students:
        await message.answer("Hali hech kim ro'yxatdan o'tmagan.")
        return
    
    total_students = len(students)
    avg_age = sum(s['age'] for s in students) / total_students
    groups = {}
    interests = {}
    
    for student in students:
        groups[student['group']] = groups.get(student['group'], 0) + 1
        student_interests = [i.strip() for i in student['interests'].split(',')]
        for interest in student_interests:
            interests[interest] = interests.get(interest, 0) + 1
    
    stats_text = (
        f"📊 *Guruh statistikasi*\n\n"
        f"👥 *Jami o'quvchilar:* {total_students}\n"
        f"🎂 *O'rtacha yosh:* {avg_age:.1f}\n\n"
        f"👥 *Guruhlar bo'yicha:*\n"
    )
    
    for group, count in sorted(groups.items()):
        stats_text += f"• {group}: {count} ta\n"
    
    stats_text += f"\n🎯 *Eng mashhur qiziqishlar:*\n"
    for interest, count in sorted(interests.items(), key=lambda x: x[1], reverse=True)[:5]:
        stats_text += f"• {interest}: {count} ta\n"
    
    await message.answer(stats_text, parse_mode="Markdown")

@router.message(F.text == "🔍 O'quvchilarni qidirish")
async def search_students(message: types.Message, state: FSMContext):
    await message.answer("Qidirish uchun ism yoki guruh nomini kiriting:")
    await state.set_state("search")

@router.message(F.state == "search")
async def process_search(message: types.Message, state: FSMContext):
    query = message.text.lower()
    students = load_students()
    
    found_students = []
    for student in students:
        if (query in student['full_name'].lower() or 
            query in student['group'].lower() or
            query in student['interests'].lower()):
            found_students.append(student)
    
    if found_students:
        result_text = f"🔍 *Qidiruv natijalari ({len(found_students)} ta):*\n\n"
        for student in found_students:
            result_text += (
                f"👤 {student['full_name']}\n"
                f"👥 {student['group']} | 🎂 {student['age']} yosh\n"
                f"📱 {student['phone']}\n\n"
            )
        await message.answer(result_text, parse_mode="Markdown")
    else:
        await message.answer("Hech narsa topilmadi.")
    
    await state.clear()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "🤖 *Bot yordam*\n\n"
        "📝 *Asosiy komandalar:*\n"
        "/start - Botni ishga tushirish\n"
        "/help - Yordam\n"
        "/stats - Statistika\n\n"
        "🎯 *Tugmalar:*\n"
        "📝 Anketa to'ldirish - Yangi o'quvchi ro'yxatdan o'tishi\n"
        "👤 Mening ma'lumotlarim - O'z ma'lumotlarini ko'rish\n"
        "📊 Guruh statistikasi - Umumiy statistika\n"
        "🔍 O'quvchilarni qidirish - Izlash"
    )
    await message.answer(help_text, parse_mode="Markdown")
