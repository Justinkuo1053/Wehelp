from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from Config import Config
import mysql.connector
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=Config.MYSQL_PASSWORD,
    database="website"
)
cursor = db.cursor()

# Middleware for sessions
app.add_middleware(SessionMiddleware, secret_key=Config.SESSION_SECRET_KEY)

# Routes
@app.get("/")
def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signin")
def verify_user(request: Request, username: Annotated[str, Form()] = None, password: Annotated[str, Form()] = None):
    query = "SELECT id, name, username, password FROM member WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchall()
    if not result:
        return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code=303)
    result = result[0]
    request.session.update({"SIGNED-IN": True, "ID": result[0], "NAME": result[1], "USERNAME": result[2]})
    return RedirectResponse("/member", status_code=303)

@app.get("/error")
def error_msg(request: Request, message: str):
    return templates.TemplateResponse("message.html", {"request": request, "message": message, "title": "失敗頁面"})

@app.get("/member")
def logged_in(request: Request):
    if request.session.get("SIGNED-IN"):
        name = request.session["NAME"]
        query = """
        SELECT member.name, message.content, message.id 
        FROM message 
        JOIN member ON message.member_id = member.id 
        ORDER BY message.time DESC
        """
        cursor.execute(query)
        messages = cursor.fetchall()
        return templates.TemplateResponse("member.html", {"request": request, "name": name, "messages": messages})
    return RedirectResponse("/")

@app.get("/signout")
def sign_out(request: Request):
    request.session.clear()
    return RedirectResponse("/")

@app.post("/signup")
def sign_up(request: Request, name: Annotated[str, Form()], username: Annotated[str, Form()], password: Annotated[str, Form()]):
    cursor.execute("SELECT * FROM member WHERE username=%s", (username,))
    if cursor.fetchone() is not None:
        return RedirectResponse("/error?message=帳號重複", status_code=303)
    cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
    db.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/createMessage")
def create_message(request: Request, content: Annotated[str, Form()]):
    member_id = request.session['ID']
    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (member_id, content))
    db.commit()
    return RedirectResponse("/member", status_code=303)

class Message(BaseModel):
    id: str

@app.post("/deleteMessage")
def delete_message(request: Request, message: Message):
    cursor.execute("SELECT member_id FROM message WHERE id=%s", (message.id,))
    if cursor.fetchone()[0] == request.session["ID"]:
        cursor.execute("DELETE FROM message WHERE id=%s", (message.id,))
        db.commit()
        return RedirectResponse("/member", status_code=303)

@app.get("/api/member")
def search_member(request: Request, username: str):
    if request.session.get("SIGNED-IN"):
        cursor.execute("SELECT id, name, username FROM member WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result:
            return {"data": {"id": result[0], "name": result[1], "username": result[2]}}
    return {"data": None}

class Name(BaseModel):
    name: str

@app.patch("/api/member")
def update_name(request: Request, body: Name):
    if request.session.get("SIGNED-IN"):
        member_id = request.session["ID"]
        request.session["NAME"] = body.name
        try:
            cursor.execute("UPDATE member SET name=%s WHERE id=%s", (body.name, member_id))
            db.commit()
            return {"ok": True}
        except:
            pass
    return {"error": True}
