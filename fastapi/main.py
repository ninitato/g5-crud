# from fastapi import FastAPI, Request, Form
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from sqlalchemy import create_engine, Column, Integer, String, Text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from starlette.templating import Jinja2Templates
# from starlette.responses import RedirectResponse

# app = FastAPI()

# # Database setup
# DATABASE_URL = "sqlite:///./database.db"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# class Item(Base):
#     __tablename__ = "items"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
#     description = Column(Text)

# Base.metadata.create_all(bind=engine)

# # Static files and templates
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     session = SessionLocal()
#     items = session.query(Item).all()
#     session.close()
#     return templates.TemplateResponse("index.html", {"request": request, "items": items})

# @app.get("/create", response_class=HTMLResponse)
# async def create_form(request: Request):
#     return templates.TemplateResponse("create.html", {"request": request})

# @app.post("/create")
# async def create_item(name: str = Form(...), description: str = Form(...)):
#     session = SessionLocal()
#     new_item = Item(name=name, description=description)
#     session.add(new_item)
#     session.commit()
#     session.close()
#     return RedirectResponse(url="/", status_code=303)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")