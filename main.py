import logging
import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from fastapi import FastAPI, File, UploadFile
from urllib.parse import quote, unquote
from fastapi.responses import FileResponse
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware


# 함수
from Save_all_text import Crawler
from find_name import findName
from Personal_Information_Detection import PatternMatcher
from find_api2 import findApi

app = FastAPI()
# os.chdir("/Users/baeyujeong/Desktop/api/")
logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
# logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시에는 원하는 Origin을 명시합니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/crawl/{url:path}/{option:path}")
def crawl_url(url: str, option:str):
    print(option)
    decoded_url = unquote(url)
    response_data = {"option":option, "nameData":"", "personalData":"", "url":decoded_url}
    if option == "website":
        Crawler(urls=[decoded_url]).run()
        nameData = findName()
        Personal_info = PatternMatcher().run()
        response_data = {"option":option, "nameData": nameData, "personalData":Personal_info, "url": decoded_url}
    elif option == "api":
        findApi(decoded_url)
        response_data = {"option":option, "content":"아직 준비 중 입니다."}
    return response_data

@app.post("/file/{option:path}")
def file_process(option:str):
    return {"option":option, "nameData":"이은혜", "personalData":"동래구 사직동 24", "url":"http://"}

# @app.post("/file/{option:path}")
# def file_process(option:str,file: any):
#     print("어멍머어ㅓ미친친침치닟",file)
#     return file

if __name__ == "__main__":
    import uvicorn
    # uvicorn main:app --reload

    uvicorn.run(app, host="0.0.0.0", port=8000)

