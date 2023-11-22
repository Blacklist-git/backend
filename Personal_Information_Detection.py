import glob
import re
import phonenumbers
import os


class PatternMatcher:
    def __init__(self):
        self.patterns = [
            (r"\d{2}([0]\d|[1][0-2])([0][1-9]|[1-2]\d|[3][0-1])[-]*[1-4]\d{6}",
             "주민등록번호"),  # 주민등록번호
            (r"([a-zA-Z]{1,2}\d{8})", "여권번호"),  # 여권번호
            # 외국인등록번호
            (r"([01][0-9]{5}[[:space:]~-]+[1-8][0-9]{6}|[2-9][0-9]{5}[[:space:]~-]+[1256][0-9]{6])", "외국인등록번호"),
            (r"\d{2}-\d{2}-\d{6}-\d{2}", "drive_pattern"),  # 운전면허번호
            # 도로명주소
            (r"([가-힣A-Za-z·\d~\-\.]{2,}(로|길).\d+|[가-힣A-Za-z·\d~\-\.]+(읍|동)\s[\d]+)", "도로명 주소"),
            # 지번주소
            (r"([가-힣A-Za-z·\d~\-\.]+(읍|동)\s[\d-]+|[가-힣A-Za-z·\d~\-\.]+(읍|동)\s[\d][^시]+)", "지번 주소"),
            (r"^[12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])",
             "생년월일"),  # 날짜(yyyy-mm-dd)
            # 날짜(yyyymmdd)
            (r"^(19|20)\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[0-1])",
             "생년월일"),
            (r"(\d{2,3}[ ,\-]?\d{3,4}[ ,\-]?\d{4})", "전화번호"),  # 전화번호
            # (r"([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-])", "계좌번호로 추정되는 것"),  # 계좌번호
            # (r"([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-])",
            #  "계좌번호로 추정되는 것"),  # 계좌번호
            (r"([\w!-_\.]+@[\w!-_\.]+\.[\w]{2,3})", "이메일"),  # 메일주소
            # 메일주소
            (r"\b[a-z0-9._%\+\-—|]+@[a-z0-9.\-—|]+\.[a-z|]{2,6}\b", "이메일")
        ]

    def preprocess_phone_number(self, phone_number):
        cleaned_number = ''.join(
            char for char in phone_number if char.isdigit())
        return cleaned_number

    def run(self, file_path):
        # 와일드카드 패턴을 사용하여 파일 목록 가져오기
        # 각 패턴별로 이름과 카운트를 유지
        pattern_counts = {pattern_name: 0 for _, pattern_name in self.patterns}
        save_data = ""
        # 각 파일에서 패턴을 찾아서 출력 및 카운트
        # with open('./file.txt', 'w', encoding='utf-8') as saved_data_file:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            # save_data = save_data + first_line+"에서 찾은,"
            for pattern, pattern_name in self.patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    if pattern_name == "전화번호":
                        cleaned_number = self.preprocess_phone_number(match.group())
                        parsed_number = phonenumbers.parse("+82" + cleaned_number)
                        if phonenumbers.is_valid_number(parsed_number):
                            if not (pattern_name + " : " + match.group()) in save_data:
                                save_data = save_data + pattern_name + " : " + match.group() + ","
                                pattern_counts[pattern_name] += 1
                    elif not (pattern_name+" : " + match.group()) in save_data:
                        save_data = save_data + pattern_name+" : " + match.group()+","
                        pattern_counts[pattern_name] += 1

        # 총 카운트 출력
        totalCount = 0
        for pattern_name, count in pattern_counts.items():
            if count > 0 :
                save_data = save_data + pattern_name +"의 갯수는 : "+str(count)+","
                totalCount += count
            # with open('file.txt', 'a', encoding='utf-8') as saved_data_file:
            #     saved_data_file.write(f"{pattern_name}의 총 카운트: {count}\n")
        return save_data, totalCount

    def filed(self, file_path):  # file_path로 수정
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            print("ddd", file_content)

        for pattern, pattern_name in self.patterns:
            matches = re.finditer(pattern, file_content)
            for match in matches:
                if pattern_name == "전화번호로 추정되는 것":
                    cleaned_number = self.preprocess_phone_number(match.group())
                    parsed_number = phonenumbers.parse("+82" + cleaned_number)
                    if phonenumbers.is_valid_number(parsed_number):
                        if not (pattern_name + " : " + match.group()) in file_content:
                            # CSV에서 asterisk (*)로 대체
                            file_content = file_content.replace(match.group(), '*')
                elif not (pattern_name + " : " + match.group()) in file_content:
                    # CSV에서 asterisk (*)로 대체
                    file_content = file_content.replace(match.group(), '*')

        os.makedirs("./csv", exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(file_content)

        return file_content
    

