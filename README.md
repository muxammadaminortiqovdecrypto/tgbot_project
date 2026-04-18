# Telegram O'quvchilar Anketasi Boti

Bu bot guruhdagi o'quvchilar haqida ma'lumot to'playdi va boshqaradi.

## Xususiyatlari

### 👤 Foydalanuvchi uchun:
- 📝 Anketa to'ldirish (FSM orqali)
- 👤 O'z ma'lumotlarini ko'rish
- 📊 Guruh statistikasi
- 🔍 O'quvchilarni qidirish

### 🔧 Admin uchun:
- 📋 Barcha o'quvchilarni ko'rish
- 📈 To'liq statistika
- 🗑️ O'quvchini o'chirish
- 📤 Ma'lumotlarni eksport qilish (JSON va Text format)

## Texnologiyalar

- **Python 3.10+**
- **aiogram 3.x** - Telegram Bot API
- **FSM** - Finite State Machine
- **F Magic Filter** - Filtrlash
- **Commands** - Komandalar
- **Inline Buttons** - Inline tugmalar
- **Reply Keyboard** - Reply klaviatura

## O'rnatish

1. Repositoryni kloning:
```bash
git clone https://github.com/muxammadaminortiqovdecrypto/tgbot_project.git
cd tgbot_project
```

2. Virtual environment yaratish:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Dependencylarni o'rnatish:
```bash
pip install -r requirements.txt
```

4. Bot tokenini sozlash:
- `.env` faylini oching
- `YOUR_BOT_TOKEN_HERE` o'rniga o'zingizning bot tokeningizni yozing

5. Admin ID ni sozlash:
- `handlers/admin_handlers.py` faylida `ADMIN_IDS` ro'yxatiga o'zingizning Telegram ID'ingizni qo'shing

6. Botni ishga tushirish:
```bash
python main.py
```

## Foydalanish

### Foydalanuvchilar uchun:
1. `/start` - Botni ishga tushirish
2. Anketa to'ldirish: Ism, yosh, guruh, telefon, manzil, qiziqishlar
3. O'z ma'lumotlarini ko'rish
4. Guruh statistikasini ko'rish
5. Boshqa o'quvchilarni qidirish

### Adminlar uchun:
1. `/admin` - Admin paneliga kirish
2. Barcha o'quvchilarni ko'rish
3. Statistikani ko'rish
4. O'quvchilarni o'chirish
5. Ma'lumotlarni eksport qilish

## Fayl tuzilishi

```
tgbot_project/
├── main.py              # Asosiy fayl
├── states.py            # FSM statelari
├── buttons.py           # Tugmalar va klaviaturalar
├── handlers/            # Handlerlar
│   ├── user_handlers.py # Foydalanuvchi handlerlari
│   └── admin_handlers.py# Admin handlerlari
├── .env                 # Environment o'zgaruvchilari
├── requirements.txt     # Dependencylar
├── students.json        # O'quvchilar ma'lumotlari
└── README.md           # Hujjat
```

## State lar

- `StudentForm.full_name` - To'liq ism
- `StudentForm.age` - Yosh
- `StudentForm.group` - Guruh
- `StudentForm.phone` - Telefon raqami
- `StudentForm.address` - Manzil
- `StudentForm.interests` - Qiziqishlar

## F Magic Filter

Bot F magic filter dan foydalaniladi:
- `F.text == "📝 Anketa to'ldirish"`
- `F.contact` - Kontakt ma'lumotlari
- `F.photo` - Rasmlar
- `F.state == "search"` - Qidirish state

## Command lar

- `/start` - Botni ishga tushirish
- `/help` - Yordam
- `/admin` - Admin paneli
- `/stats` - Statistika

## Inline Buttons

- ✏️ Tahrirlash
- 🗑️ O'chirish  
- 📊 Batafsil
- ✅ Ha / ❌ Yo'q (tasdiqlash)

## Ma'lumotlar saqlash

O'quvchilar ma'lumotlari `students.json` faylida saqlanadi:
```json
{
  "user_id": 123456789,
  "full_name": "O'quvchi Ismi",
  "age": 20,
  "group": "201-guruh",
  "phone": "+998901234567",
  "address": "Toshkent shahar",
  "interests": "dasturlash, sport",
  "registration_date": "2024-01-01"
}
```

## Litsenziya

MIT License
