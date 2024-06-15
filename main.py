from fastapi import FastAPI, Request, Depends, HTTPException, status
from src.routes import contacts
from sqlalchemy.ext.asyncio import AsyncSession
from flask import Flask
from contacts import app
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.database.db import get_db
from starlette.middleware.cors import CORSMiddleware
from src.conf.config import CORS_RESOURCES

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    **CORS_RESOURCES
)

app.include_router(contacts.router, prefix="/api")


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello FastApi"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

app.run(debug=True)