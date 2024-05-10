from fastapi import FastAPI, Form, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Union
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 設定 Session 中間件，用來保持狀態
app.add_middleware(
    SessionMiddleware,
    secret_key="some-random-string",
    session_cookie="session",
    max_age=600,
   
)

@app.get("/",response_class=HTMLResponse,name="index")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/error",name="error")
async def route_error(request: Request,message: Union[str, None] = None):
    if message == "請輸入帳號、密碼":
        return templates.TemplateResponse("error.html", {"request": request, "failed_text": message})
    elif message == "帳號、密碼輸入錯誤":
        return templates.TemplateResponse("error.html", {"request": request, "failed_text": message})

@app.post("/signin", name="signin")
async def signin(request: Request, username: str = Form(None), password: str = Form(None)):
    try:
        print("登入嘗試")
        if not username or not password:
            return RedirectResponse(url="/error?message=請輸入帳號、密碼", status_code=status.HTTP_303_SEE_OTHER)
        if username == "test" and password == "test":
            request.session.update({"username": username})
            return RedirectResponse(url="/member", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse(url="/error?message=帳號、密碼輸入錯誤", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        request.app.logger.error(f"Error during sign in: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
@app.get("/member",name="member")
async def success(request: Request):
    if not request.session:
        return RedirectResponse(url="/")
    print(request.session)
    return templates.TemplateResponse("member.html", {"request": request})

@app.get("/signout")
async def signout(request: Request):
    request.session.pop('username', None)
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


# calculator
@app.get("/square/{num}", name="square_calculator")
async def square_calculator(request: Request, num: int):
    result = num ** 2
    return templates.TemplateResponse("Calculator.html", {"request": request, "result": result})