from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from Config import Config


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=Config.MYSQL_PASSWORD,
    database="website"
)
cursor = db.cursor()

app.add_middleware(SessionMiddleware, secret_key=Config.SESSION_SECRET_KEY)

@app.get("/")
def get_home(request:Request):
    return templates.TemplateResponse(request=request, name="app.html")

@app.post("/signin")
def verify_user(request:Request, username: Annotated[str, Form()]=None, password: Annotated[str, Form()]=None):
    cursor.execute("SELECT id, name, username, password FROM member WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchall()
    print(result) 
    if (not result):
        return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code=303)
    result = result[0]
    request.session["SIGNED-IN"] = True
    request.session["ID"] = result[0]
    request.session["NAME"] = result[1]
    request.session["USERNAME"] = result[2]
    return RedirectResponse("/member", status_code=303)

@app.get("/error")
def error_msg(request:Request, message):
    return templates.TemplateResponse(request=request, name="message.html", context={"message": message, "title": "失敗頁面"})

@app.get("/member")
def loggedIn(request:Request):
    if "SIGNED-IN" in request.session and request.session["SIGNED-IN"]:
        name = request.session["NAME"]
        cursor.execute("SELECT member.name, message.content, message.id FROM message JOIN member ON message.member_id=member.id ORDER BY message.time DESC")
        messages = cursor.fetchall()
        return templates.TemplateResponse(request=request, name="member.html", context={"name": name, "messages": messages})
    return RedirectResponse("/")

@app.get("/signout")
def sign_out(request:Request):
    request.session["SIGNED-IN"] = False
    request.session["ID"] = ""
    request.session["NAME"] = ""
    request.session["USERNAME"] = ""
    return RedirectResponse("/")

@app.post("/signup")
def sign_up(request:Request, name:Annotated[str, Form()], username:Annotated[str, Form()], password: Annotated[str, Form()]):
    cursor.execute("SELECT * FROM member WHERE username=%s", (username, ))
    result = cursor.fetchone()
    if result == None:
        cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
        db.commit()
        return RedirectResponse("/", status_code=303)
    return RedirectResponse("/error?message=帳號重複", status_code=303)

@app.post("/createMessage")
def create_message(request:Request, content:Annotated[str, Form()]):
    member_id = request.session['ID']
    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (member_id, content))
    db.commit()
    return RedirectResponse("/member", status_code=303)

class Message(BaseModel):
    id: str

@app.post("/deleteMessage")
def delete_message(request:Request, message:Message):
    cursor.execute("SELECT member_id FROM message WHERE id=%s", (message.id, ))
    member_id = cursor.fetchone()[0]
    if member_id == request.session["ID"]:
        cursor.execute("DELETE FROM message WHERE id=%s", (message.id, ))
        db.commit()
        return RedirectResponse("/member", status_code=303)
    return