from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from pathlib import Path

# Get the current directory
BASE_DIR = Path(__file__).resolve().parent

# Create instance folder if it doesn't exist
os.makedirs(BASE_DIR / "instance", exist_ok=True)

# Database setup
SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR}/instance/database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Setup templates - Note this change
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.get("/create", response_class=HTMLResponse)
async def create_get(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create")
async def create_post(name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    new_item = Item(name=name, description=description)
    db.add(new_item)
    db.commit()
    return RedirectResponse(url="/", status_code=303)