import re
import requests

# 예시 HTML 코드
response = requests.get("")
html_content = response.text

# URL 패턴 및 정규표현식
url_pattern = r""

# 정규표현식을 사용하여 URL 추출
urls = re.findall(url_pattern, html_content)

# 각 URL에 대해 크롤링하여 내용 가져오기
for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        # 여기서부터 가져온 내용에 대한 처리를 진행할 수 있습니다.
        # 예시로 가져온 내용을 출력합니다.
            # 개인정보 패턴 및 정규 표현식
        email_pattern = r'[\w\.-]+@[\w\.-]+'
        phone_pattern = r'\d{3}-\d{4}-\d{4}'
        rrn_pattern = r'\d{6}-\d{7}'
        name_pattern = r'[가-힣]{2,3}'

        # 정규 표현식을 사용하여 개인정보 검출
        email = re.findall(email_pattern, content)
        phone = re.findall(phone_pattern, content)
        rrn = re.findall(rrn_pattern, content)
        name = re.findall(name_pattern, content)

        # 검출된 개인정보 출력
        print('URL:', url)
        print('이메일:', email)
        print('전화번호:', phone)
        print('주민등록번호:', rrn)
        print('이름:', name)
        print()
