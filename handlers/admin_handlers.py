import json
from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from buttons import admin_menu, student_actions_keyboard, confirm_keyboard

router = Router()

ADMIN_IDS = [123456789]  # O'zingizning Telegram ID'ingizni kiriting

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def load_students():
    try:
        with open('students.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_students(students):
    with open('students.json', 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=2)

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz!")
        return
    
    await message.answer("🔧 Admin paneliga xush kelibsiz!", reply_markup=admin_menu)

@router.message(F.text == "📋 Barcha o'quvchilar")
async def all_students(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz!")
        return
    
    students = load_students()
    
    if not students:
        await message.answer("Hali hech kim ro'yxatdan o'tmagan.")
        return
    
    for i, student in enumerate(students, 1):
        student_text = (
            f"👤 *{i}. {student['full_name']}*\n"
            f"🎂 Yosh: {student['age']}\n"
            f"👥 Guruh: {student['group']}\n"
            f"📱 Telefon: {student['phone']}\n"
            f"📍 Manzil: {student['address']}\n"
            f"🎯 Qiziqishlar: {student['interests']}\n"
            f"📅 Ro'yxatdan o'tgan: {student['registration_date']}"
        )
        
        await message.answer(student_text, parse_mode="Markdown", 
                          reply_markup=student_actions_keyboard(student['user_id']))
        
        if i % 5 == 0:  # Har 5 ta o'quvchidan so'ng kutish
            await asyncio.sleep(1)

@router.message(F.text == "📈 Statistika")
async def admin_statistics(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz!")
        return
    
    students = load_students()
    
    if not students:
        await message.answer("Hali hech kim ro'yxatdan o'tmagan.")
        return
    
    total = len(students)
    avg_age = sum(s['age'] for s in students) / total
    
    # Guruhlar bo'yicha statistika
    groups = {}
    ages = {}
    
    for student in students:
        groups[student['group']] = groups.get(student['group'], 0) + 1
        age_group = student['age'] // 10 * 10
        ages[f"{age_group}-{age_group+9}"] = ages.get(f"{age_group}-{age_group+9}", 0) + 1
    
    stats_text = (
        f"📈 *To'liq statistika*\n\n"
        f"👥 *Jami o'quvchilar:* {total}\n"
        f"🎂 *O'rtacha yosh:* {avg_age:.1f}\n\n"
        f"👥 *Guruhlar bo'yicha:*\n"
    )
    
    for group, count in sorted(groups.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total) * 100
        stats_text += f"• {group}: {count} ta ({percentage:.1f}%)\n"
    
    stats_text += f"\n🎂 *Yosh toifalari:*\n"
    for age_range, count in sorted(ages.items()):
        percentage = (count / total) * 100
        stats_text += f"• {age_range} yosh: {count} ta ({percentage:.1f}%)\n"
    
    await message.answer(stats_text, parse_mode="Markdown")

@router.message(F.text == "🗑️ O'quvchini o'chirish")
async def delete_student_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz!")
        return
    
    await message.answer("O'chirish uchun o'quvchi ismini yoki Telegram ID sini kiriting:")
    await state.set_state("delete_student")

@router.message(F.state == "delete_student")
async def delete_student_process(message: types.Message, state: FSMContext):
    query = message.text.strip().lower()
    students = load_students()
    
    found_students = []
    for student in students:
        if (query in student['full_name'].lower() or 
            query == str(student['user_id'])):
            found_students.append(student)
    
    if len(found_students) == 1:
        student = found_students[0]
        await state.update_data(delete_student_id=student['user_id'])
        await message.answer(
            f"❌ *{student['full_name']}* ni o'chirmoqchimisiz?",
            reply_markup=confirm_keyboard,
            parse_mode="Markdown"
        )
        await state.set_state("confirm_delete")
    elif len(found_students) > 1:
        result_text = "🔍 *Bir nechta o'quvchi topildi:*\n\n"
        for i, student in enumerate(found_students, 1):
            result_text += f"{i}. {student['full_name']} (ID: {student['user_id']})\n"
        result_text += "\nO'chirish uchun Telegram ID sini kiriting:"
        await message.answer(result_text, parse_mode="Markdown")
    else:
        await message.answer("O'quvchi topilmadi.")
        await state.clear()

@router.callback_query(F.data.startswith("confirm_"))
async def confirm_delete_callback(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!")
        return
    
    action = callback.data.split("_")[1]
    
    if action == "yes":
        data = await state.get_data()
        student_id = data.get('delete_student_id')
        
        if student_id:
            students = load_students()
            students = [s for s in students if s['user_id'] != student_id]
            save_students(students)
            
            await callback.message.edit_text("✅ O'quvchi muvaffaqiyatli o'chirildi!")
        else:
            await callback.message.edit_text("❌ Xatolik yuz berdi!")
    else:
        await callback.message.edit_text("❌ O'chirish bekor qilindi.")
    
    await state.clear()
    await callback.answer()

@router.message(F.text == "📤 Ma'lumotlarni eksport qilish")
async def export_data(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz!")
        return
    
    students = load_students()
    
    if not students:
        await message.answer("Eksport qilish uchun ma'lumot yo'q.")
        return
    
    # JSON formatida eksport
    json_data = json.dumps(students, ensure_ascii=False, indent=2)
    
    # Text formatida eksport
    text_data = "O'QUVCHILAR RO'YXATI\n" + "="*50 + "\n\n"
    for i, student in enumerate(students, 1):
        text_data += f"{i}. {student['full_name']}\n"
        text_data += f"   Yosh: {student['age']}\n"
        text_data += f"   Guruh: {student['group']}\n"
        text_data += f"   Telefon: {student['phone']}\n"
        text_data += f"   Manzil: {student['address']}\n"
        text_data += f"   Qiziqishlar: {student['interests']}\n"
        text_data += f"   Ro'yxatdan o'tgan: {student['registration_date']}\n"
        text_data += "-"*30 + "\n\n"
    
    # JSON faylni yuborish
    await message.answer_document(
        document=types.BufferedInputFile(
            json_data.encode('utf-8'),
            filename="students_export.json"
        ),
        caption="📄 O'quvchilar ma'lumotlari (JSON format)"
    )
    
    # Text faylni yuborish
    await message.answer_document(
        document=types.BufferedInputFile(
            text_data.encode('utf-8'),
            filename="students_export.txt"
        ),
        caption="📄 O'quvchilar ma'lumotlari (Text format)"
    )

@router.callback_query(F.data.startswith("edit_"))
async def edit_student_callback(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!")
        return
    
    student_id = int(callback.data.split("_")[1])
    students = load_students()
    
    student = next((s for s in students if s['user_id'] == student_id), None)
    if student:
        info_text = (
            f"✏️ *{student['full_name']} ma'lumotlarini tahrirlash*\n\n"
            f"🎯 Hozirgi ma'lumotlar:\n"
            f"📝 Ism: {student['full_name']}\n"
            f"🎂 Yosh: {student['age']}\n"
            f"👥 Guruh: {student['group']}\n"
            f"📱 Telefon: {student['phone']}\n"
            f"📍 Manzil: {student['address']}\n"
            f"🎯 Qiziqishlar: {student['interests']}\n\n"
            f"⚠️ *Tahrirlash funksiyasi tez orada qo'shiladi!*"
        )
        await callback.message.answer(info_text, parse_mode="Markdown")
    
    await callback.answer()

@router.callback_query(F.data.startswith("details_"))
async def student_details_callback(callback: types.CallbackQuery):
    student_id = int(callback.data.split("_")[1])
    students = load_students()
    
    student = next((s for s in students if s['user_id'] == student_id), None)
    if student:
        details_text = (
            f"👤 *{student['full_name']} - Batafsil ma'lumot*\n\n"
            f"🆔 *Telegram ID:* {student['user_id']}\n"
            f"🎂 *Yoshi:* {student['age']} yosh\n"
            f"👥 *Guruh:* {student['group']}\n"
            f"📱 *Telefon raqami:* {student['phone']}\n"
            f"📍 *Manzili:* {student['address']}\n"
            f"🎯 *Qiziqishlari:* {student['interests']}\n"
            f"📅 *Ro'yxatdan o'tgan sana:* {student['registration_date']}\n\n"
            f"📊 *Qo'shimcha ma'lumot:* O'quvchi ma'lumotlar bazasiga muvaffaqiyatli kiritilgan."
        )
        await callback.message.answer(details_text, parse_mode="Markdown")
    
    await callback.answer()

@router.callback_query(F.data.startswith("delete_"))
async def delete_student_callback(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!")
        return
    
    student_id = int(callback.data.split("_")[1])
    students = load_students()
    
    student = next((s for s in students if s['user_id'] == student_id), None)
    if student:
        await state.update_data(delete_student_id=student_id)
        await callback.message.edit_text(
            f"❌ *{student['full_name']}* ni o'chirmoqchimisiz?",
            reply_markup=confirm_keyboard,
            parse_mode="Markdown"
        )
        await state.set_state("confirm_delete")
    
    await callback.answer()

@router.message(F.text == "🔙 Orqaga")
async def back_to_main(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz!")
        return
    
    # Asosiy menuga qaytish uchun
    await message.answer("Asosiy menuga qaytdingiz.", reply_markup=types.ReplyKeyboardRemove())
