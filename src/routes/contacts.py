from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.schemas import ContactBase, ContactCreate, ContactInDB, ContactUpdate
from src.repository import contacts as repository_contacts
from sqlalchemy import or_, select
from src.database.models import Contact
from datetime import date, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from db import get_user, get_contact_limit, create_contact, get_contacts
from fastapi import File, UploadFile
from src.repository.contacts import update_avatar
from src.schemas import ContactSchema

router = APIRouter()

app = FastAPI()

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

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=list[ContactInDB])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.post("/", response_model=ContactInDB, status_code=status.HTTP_201_CREATED)
async def create_contact(contact_data: ContactCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new contact.
    """
    try:
        contact = await repository_contacts.create(contact_data, db)
        return contact
    except Exception as e:
        logger.error(f"Error while creating contact: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")


@router.get("/birthday", response_model=list[ContactInDB])
async def get_birthdays(days: int = Query(7, ge=7), db: AsyncSession = Depends(get_db)):
    contacts = await repository_contacts.get_birthdays(days, db)
    return contacts


@router.get("/search", response_model=list[ContactInDB])
async def serch(
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        skip: int = 0,
        limit: int = Query(default=10, le=100, ge=10),
        db: AsyncSession = Depends(get_db),
):
    contacts = await repository_contacts.search(first_name, last_name, email, skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactInDB)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactUpdate, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    return contact

from fastapi import APIRouter, Depends
from fastapi_users.dependencies import current_active_user
from .models import User

router = APIRouter()

@router.get("/contacts", dependencies=[Depends(current_active_user)])
def get_contacts(user: User = Depends(current_active_user)):
    # Логіка отримання контактів для авторизованого користувача
    return contacts

@app.post("/contacts")
async def create_contact_route(request: Request):
    if request.json:
        data = request.json
        if 'email' in data and 'contact' in data:
            email = data['email']
            contact = data['contact']
            user = get_user(email)
            if user:
                if create_contact(user.id, contact):
                    return JSONResponse(content={"message": "Contact created successfully"}, media_type="application/json", status_code=201)
                else:
                    raise HTTPException(status_code=400, detail="Contact limit exceeded")
            else:
                raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(status_code=400, detail="Invalid request")
    else:
        raise HTTPException(status_code=400, detail="Invalid request")

@app.get("/contacts")
async def get_contacts_route(request: Request):
    if 'email' in request.query_params:
        email = request.query_params.get('email')
        user = get_user(email)
        if user:
            return JSONResponse(content=[contact.to_dict() for contact in get_contacts(user.id)], media_type="application/json", status_code=200)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="Invalid request")
    
@router.put("/{contact_id}/avatar", response_model=ContactSchema)
async def update_contact_avatar(contact_id: int, avatar: UploadFile = File(...)):
    """Оновлює аватар контакту"""
    avatar_url = update_avatar(contact_id, await avatar.read())
    return {"id": contact_id, "avatar": avatar_url}