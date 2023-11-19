import logging
from fastapi import FastAPI, File, UploadFile,HTTPException, Depends
from urllib.parse import quote, unquote
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import ssl
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from db_connection import database, User, SessionLocal
from security import create_jwt_token, hash_password, verify_password, SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from jose import JWTError, jwt

# 함수
from Save_all_text import Crawler
from find_name import findName
from Personal_Information_Detection import PatternMatcher
from find_api2 import findApi

app = FastAPI(openapi_prefix="/server")
# os.chdir("/Users/baeyujeong/Desktop/api/")
logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
# logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
origins = [
    "http://localhost:3000",  # 허용할 Origin을 여기에 추가
    "https://www.clubblacklist.kro.kr",
    "https://34.197.212.64","https://clubblacklist.kro.kr",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 실제 배포 시에는 원하는 Origin을 명시합니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY = "your-secret-key"  # 서버 측에서 사용하는 시크릿 키
ALGORITHM = "HS256"  # 알고리즘, 서버와 클라이언트 모두 동일해야 함

async def get_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        if user_name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await database.fetch_one(User.select().where(User.c.username == user_name))

    if user:
        return {"id": user["id"], "name": user["name"]}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.on_event("startup")
async def startup_db_client():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()

@app.post("/server/register")
async def register(data: dict, db: Session = Depends(get_db)):
    username = data.get("idSend")
    hashed_password = hash_password(data.get("pwSend"))
    name = data.get("nameSend")
    new_user = User(username=username, hashed_password=hashed_password, name=name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@app.post("/server/login")
async def login(data: dict):
    username = data.get("idSend")
    password = data.get("pwSend")

    user = await get_user(username)
    
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 토큰 만료 시간 설정 (15분)
    expires_delta = timedelta(minutes=15)
    # 토큰 생성
    token = create_jwt_token({"sub": username}, expires_delta)

    return {"access_token": token, "token_type": "bearer"}

@app.post("/server/check_duplicate")
async def check_duplicate(data: dict):
    existing_user = await database.fetch_one(User.select().where(User.c.username == data.get("idSend")))
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return {"message": "Username available"}

@app.post("/server/crawl")
def crawl_url(data:dict):
    url = data.get("url")
    option = data.get("option")
    decoded_url = unquote(url)
    response_data = {"option":option, "nameData":"", "personalData":"", "url":decoded_url}
    if option == "website":
        Crawler(urls=[decoded_url]).run()
        nameData = findName()
        Personal_info = PatternMatcher().run()
        Personal_info = Personal_info.replace("URL : "+url+"에서 찾은", "")
        response_data = {"option":option, "nameData": nameData, "personalData":Personal_info, "url": decoded_url}
    elif option == "api":
        findApi(decoded_url)
        response_data = {"option":option, "content":"아직 준비 중 입니다."}
    return response_data

@app.post("/server/file/{option:path}")
def file_process(option:str):
    try:
        shutil.rmtree('re/resres2')
    except: pass
    return {"option":option, "nameData":"이은혜", "personalData":"동래구 사직동 24", "url":"http://"}

# @app.post("/file/{option:path}")
# def file_process(option:str,file: any):
#     print("어멍머어ㅓ미친친침치닟",file)
#     return file

@app.post("/server/savePDF")
async def save_pdf(pdf_data: UploadFile = File(...)):
    try:
        # 클라이언트에서 전송한 PDF 데이터를 바이너리로 읽음
        pdf_binary = await pdf_data.read()
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"Report_{current_time}.pdf"

        # PDF 파일 저장
        file_path = f"/var/www/web-services/backend/upload/{file_name}"  # 저장 경로를 적절히 수정하세요.
        with open(file_path, "wb") as f:
            f.write(pdf_binary)

        return JSONResponse(content={"message": "PDF saved successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
    # 여기서 PDF 파일을 저장하거나 원하는 처리를 수행합니다.
    # contents에는 PDF 파일의 바이너리 데이터가 들어 있습니다.
    
    return {"status": "success"}

if __name__ == "__main__":
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # ssl_context.load_cert_chain(certfile="/etc/letsencrypt/live/www.clubblaclist.kro.kr/fullchain.pem", keyfile="/etc/letsencrypt/live/www.clubblacklist.kro.kr/privkey.pem")

    import uvicorn
    # uvicorn main:app --reload

    uvicorn.run(app, host="0.0.0.0", port=8000)

