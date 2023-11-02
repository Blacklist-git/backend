import logging
import os
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote
import shutil

class Crawler:
    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.file_counter = 1

    def download_url(self, url, base_url):
        # URL이 상대 URL이라면 기본 URL을 기반으로 절대 URL로 변환
        if not urlparse(url).scheme:
            url = "http://" + url
            url = urljoin(base_url, url)
        response = requests.get(url)
        response.encoding = 'utf-8'  # 명시적으로 UTF-8로 설정
        return response.text
    
    def download_text(self, text):
        soup = BeautifulSoup(text, 'html.parser', from_encoding="utf-8")
        extracted_text = ' '.join(soup.stripped_strings)
        return extracted_text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        for link in soup.find_all("a"):
            path = link.get("href")

            if path or path.startswith("/"):
                path = urljoin(url, path)
                yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url, base_url):
        html = self.download_url(url, base_url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        try:
            shutil.rmtree('re/resres2')
        except: pass
        parsed_url = urlparse(self.urls_to_visit[0])
        if not parsed_url.scheme:
            base_url = f"http://{parsed_url.path}"  # 기본 URL을 정의 (실제 URL로 바꿔주세요)
        else:
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"  # 기본 URL을 정의 (실제 URL로 바꿔주세요)
        print(parsed_url)
        print(base_url)
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            print(url)
            logging.info(f"Crawling: {url}")
            try:
                html = self.download_url(url, base_url)
                self.crawl(url, base_url)  # base_url을 전달
                # print(self.download_url(url, base_url))
                output_dir = "re/resres2"
                os.makedirs(output_dir, exist_ok=True)
                output_file_name = f"{output_dir}/find{self.file_counter}.txt"
                with open(output_file_name, "w", encoding="utf-8") as file:
                    # file.write(self.download_url(url, base_url))
                    file.write(f"URL : {url}\n\n")
                    file.write(self.download_text(html))
                self.file_counter += 1
            except Exception:
                logging.exception(f"Failed to crawl: {url}")
            finally:
                self.visited_urls.append(url)