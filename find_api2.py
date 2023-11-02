import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import shutil

# 웹 페이지 URL
# web_page_url = ""
def findApi(url):
    try:
        shutil.rmtree('js_files')
    except: pass
    os.makedirs("js_files", exist_ok=True)
# 웹 페이지를 다운로드
    web_page_url = url
    response = requests.get(web_page_url)

    if response.status_code == 200:
        # BeautifulSoup을 사용하여 웹 페이지를 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 웹 페이지 내에서 JavaScript 파일 경로를 찾음
        js_files = []
        for script_tag in soup.find_all('script', src=True):
            js_url = urljoin(web_page_url, script_tag['src'])
            js_files.append(js_url)
        
        # JavaScript 파일을 다운로드할 디렉토리 경로
        download_directory = "js_files"
        os.makedirs(download_directory, exist_ok=True)
        
        # JavaScript 파일 다운로드 및 API URL 검색 및 상태 코드 확인
        for js_url in js_files:
            js_filename = os.path.basename(js_url)
            js_path = os.path.join(download_directory, js_filename)
            
            print(f"다운로드 중: {js_url}")
            
            js_content = requests.get(js_url).text
            
            # JavaScript 파일 내에서 API URL을 검색
            api_urls = re.findall(r'["\'](http[s]?://(?:[a-zA-Z0-9.-]+)(?::[0-9]+)?(?:/[^"]*)?)', js_content)
            
            # API URL을 확인하고 상태 코드 검사
            for api_url in api_urls:
                try:
                    api_response = requests.get(api_url)
                    if api_response.status_code == 200:
                        print(f"{js_filename} 파일에서 발견된 유효한 API URL: {api_url}")
                except requests.exceptions.RequestException as e:
                    print(f"API URL 연결 오류: {e}")
            
            with open(js_path, 'w', encoding='utf-8') as js_file:
                js_file.write(js_content)
            
            print(f"{js_filename} 다운로드 완료")
            
        print("모든 JavaScript 파일 다운로드 완료")
    else:
        print("웹 페이지를 다운로드할 수 없습니다.")
