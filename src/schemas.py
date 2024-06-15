from datetime import datetime, date
from pydantic import BaseModel, EmailStr
from marshmallow import Schema, fields
from typing import Optional

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date | None = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactInDB(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ContactSchema(Schema):
    class Meta:
        fields = ('name', 'phone', 'email')

class UserSchema(Schema):
    class Meta:
        fields = ('email', 'contacts')

class ContactSchema(BaseModel):
    id: Optional[int]
    name: str
    email: str
    avatar: Optional[str]