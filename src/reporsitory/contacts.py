import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import ContactBase, ContactCreate, ContactInDB, ContactUpdate
from src.database.models import Contact
from sqlalchemy import select, extract
from datetime import date, timedelta
import cloudinary
import cloudinary.uploader

# Создание логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание обработчика для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Создание форматировщика для логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(console_handler)


async def create(body: ContactBase, db: AsyncSession):
    try:
        contact = Contact(**body.model_dump())
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        return contact
    except Exception as e:
        logger.error(f"Error while creating contact: {e}")
        if "ValidationError" in str(e):
            logger.error("Validation error occurred.")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def update_contact(contact_id: int, body: ContactUpdate, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        await db.commit()
        await db.refresh(contact)
    return contact

def update_avatar(contact_id: int, avatar_file: bytes) -> str:
    """Оновлює аватар користувача в Cloudinary"""
    result = cloudinary.uploader.upload(avatar_file, public_id=f"contact_{contact_id}")
    return result["secure_url"]

async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def get_birthdays(days, db: AsyncSession):
    days: int = days + 1
    filter_month = date.today().month
    filter_day = date.today().day

    stmt = select(Contact).filter(
        extract('month', Contact.birthday) == filter_month,
        extract('day', Contact.birthday) <= filter_day + days
    )

    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def search(first_name, last_name, email, skip, limit, db):
    query = select(Contact)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))

    result_query = query.offset(skip).limit(limit)

    try:
        contacts = await db.execute(result_query)
        return contacts.scalars().all()
    except Exception as e:
        # Обработка исключения, запись ошибки в журнал и возврат соответствующего ответа
        print(f"Ошибка при выполнении запроса к базе данных: {e}")
        return []

from database.models import User

def verify_email(email):
    user = session.query(User).filter_by(email=email).first()
    if user:
        return True
    return False


from datetime import datetime, timedelta
from collections import defaultdict

class ContactRepository:
    def __init__(self):
        self.contacts = defaultdict(list)
        self.last_request_time = datetime.min

    def get_contacts(self, user_id):
        if datetime.now() - self.last_request_time < timedelta(seconds=1):
            return []
        self.last_request_time = datetime.now()
        return self.contacts[user_id]

    def add_contact(self, user_id, contact):
        self.contacts[user_id].append(contact)





