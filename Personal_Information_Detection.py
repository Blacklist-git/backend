import glob
import re

class PatternMatcher:
    def __init__(self):
        self.patterns = [
            # 시간남으면 디테일...해서 오탐 줄이기
            (r"(\d{6}[ ,-]-?[1-4]\d{6}|\d{6}[ ,-]?[1-4])", "주민등록번호로 추정되는 것"),  # 주민등록번호
            (r"([a-zA-Z]{1,2}\d{8})", "여권번호로 추정되는 것"),  # 여권번호
            (r"([01][0-9]{5}[[:space:]~-]+[1-8][0-9]{6}|[2-9][0-9]{5}[[:space:]~-]+[1256][0-9]{6])", "외국인등록번호로 추정되는 것"),  # 외국인등록번호
            (r"\d{2}-\d{2}-\d{6}-\d{2}", "drive_pattern"),  # 운전면허번호
            (r"([가-힣A-Za-z·\d~\-\.]{2,}(로|길).\d+|[가-힣A-Za-z·\d~\-\.]+(읍|동)\s[\d]+)", "도로명 주소"),  # 도로명주소
            (r"([가-힣A-Za-z·\d~\-\.]+(읍|동)\s[\d-]+|[가-힣A-Za-z·\d~\-\.]+(읍|동)\s[\d][^시]+)", "지번 주소"),  # 지번주소
            (r"^[12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])", "생년월일로 추정될 수 있는 날짜"),  # 날짜(yyyy-mm-dd)
            (r"^(19|20)\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[0-1])", "생년월일로 추정될 수 있는 날짜"),  # 날짜(yyyymmdd)
            (r"(\d{2,3}[ ,-]-?\d{2,4}[ ,-]-?\d{4})", "전화번호로 추정되는 것"),  # 전화번호
            (r"([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-])", "계좌번호로 추정되는 것"),  # 계좌번호
            (r"([\w!-_\.]+@[\w!-_\.]+\.[\w]{2,3})", "메일 주소로 추정되는 것"),  # 메일주소
            (r"\b[a-z0-9._%\+\-—|]+@[a-z0-9.\-—|]+\.[a-z|]{2,6}\b", "메일 주소로 추정되는 것")  # 메일주소
        ]

    def run(self):
        # 와일드카드 패턴을 사용하여 파일 목록 가져오기
        file_paths = glob.glob('re/resres2/find*.txt')
        print(file_paths)

        # 각 패턴별로 이름과 카운트를 유지
        pattern_counts = {pattern_name: 0 for _, pattern_name in self.patterns}
        print(pattern_counts)
        save_data = ""
        # 각 파일에서 패턴을 찾아서 출력 및 카운트
        # with open('./file.txt', 'w', encoding='utf-8') as saved_data_file:
        for file_path in file_paths:
            with open(file_path, "r", encoding="utf-8") as file:
                first_line = file.readline()
                text = file.read()
                save_data = save_data + first_line+"에서 찾은,"
                for pattern, pattern_name in self.patterns:
                    matches = re.finditer(pattern, text)
                    for match in matches:
                        if not (pattern_name+" : " + match.group()) in save_data:
                            save_data = save_data + pattern_name+" : " + match.group()+","
                            pattern_counts[pattern_name] += 1

        # 총 카운트 출력
        for pattern_name, count in pattern_counts.items():
            if count > 0 :
                save_data = save_data + pattern_name +"의 갯수는 : "+str(count)+","
            # with open('file.txt', 'a', encoding='utf-8') as saved_data_file:
            #     saved_data_file.write(f"{pattern_name}의 총 카운트: {count}\n")
        return save_data
