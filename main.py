import logging
import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from fastapi import FastAPI, File, UploadFile,HTTPException
from urllib.parse import quote, unquote
from fastapi.responses import FileResponse
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import ssl
from datetime import datetime

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
    "https://34.197.212.64",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 실제 배포 시에는 원하는 Origin을 명시합니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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

