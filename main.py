import logging
import jwt
from urllib.parse import urljoin, urlparse
from fastapi import FastAPI, File, UploadFile,HTTPException
from urllib.parse import quote, unquote
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import ssl
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from db_connection import database, users
from security import create_jwt_token, hash_password, verify_password
# from jose import JWTError
from fastapi import Depends, HTTPException, status
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from io import BytesIO
import os


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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_user(username: str):
    user = await database.fetch_one(users.select().where(users.c.username == username))
    return user

@app.on_event("startup")
async def startup_db_client():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()

@app.post("/server/register")
async def register(data:dict):
    hashed_password = hash_password(data.get("pwSend"))
    query = users.insert().values( username=data.get("idSend"), hashed_password=hashed_password)
    await database.execute(query)


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
    existing_user = await database.fetch_one(users.select().where(users.c.username == data.get("idSend")))
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return {"message": "Username available"}

@app.post("/server/website")
def crawl_url(data:dict):
    try:
        shutil.rmtree('re/resres2')
    except: pass
    url = data.get("url")
    option = data.get("option")
    decoded_url = unquote(url)
    response_data = {"option":option, "nameData":"", "personalData":"", "url":decoded_url}
    Crawler(urls=[decoded_url]).run()
    nameData = findName().crawl()
    Personal_info = PatternMatcher().run()
    Personal_info = Personal_info.replace("URL : "+url+"에서 찾은", "")
    response_data = {"option":option, "nameData": nameData, "personalData":Personal_info, "url": decoded_url}
    return response_data

@app.post("/server/api")
def api_url():
    return {"option":"api", "nameData":"이은혜 오승민", "personalData":"동래구 사직동 24", "url":"http://"}

@app.post("/server/csv")
async def file_process(file: UploadFile = File(...)):
    try:
        file_name = file.filename
        file_content = findName.filed(file)
        print(file_content.decode("utf-8"))

        return findName.filed(file)

    except Exception as e:
        return f"파일을 읽는 중 오류 발생: {str(e)}"
    
@app.get("/server/download")
def download_file():
    file_path = "../csv/testdata.csv"

    # 파일이 존재하는지 확인
    if not os.path.exists(file_path):
        return Response(content="File not found", status_code=404)

    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")

    # 파일 다운로드
    headers = {
        "Content-Disposition": f"attachment; filename={os.path.basename(file_path)}",
        "Content-Type": "text/csv",
    }

    return StreamingResponse(iter([file_content]), headers=headers)


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


