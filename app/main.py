from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta, date
from typing import Optional
from .services.email_sender import ApigClient

import os


class Message(BaseModel):
    name: str = Form(...)
    email: str = Form(...)
    phone: str = Form(...)
    school: str = Form(...)
    subject: str = Form(...)
    message: str = Form(...)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=os.getcwd() +
          "/app/static"), name="static")

templates = Jinja2Templates(directory=os.getcwd()+"/app/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "show_alert": False})

@app.get("/features", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("features.html", {"request": request})

@app.get("/training", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("portfolio.html", {"request": request})

@app.get("/formats", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})

@app.post("/contact-us")
async def contact_us(request: Request, name: str = Form(...), email: str = Form(...), phone: Optional[str] = Form(None), school: Optional[str] = Form(None), subject: str = Form(...), message: str = Form(...)):
    apig = ApigClient()
    success = apig.send_email(name, email, phone, school, subject, message)
    return templates.TemplateResponse("contact.html", {"request": request, "success": success, "show_alert": True})