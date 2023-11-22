import glob
import re
import os

class findName():
    # 성
    last_name = set()
    with open('all_last_names.txt', 'r', encoding='utf-8') as name_file:
        for line in name_file:
            character = line.split()
            if character:
                last_name.update(character)

    # 이름
    word_list = set()
    with open('all_first_names.txt', 'r', encoding='utf-8') as word_file:
        for line in word_file:
            words = line.split()
            if words:
                word_list.update(words)

    # 합치기
    combined_names = set()
    for character in last_name:
        for word in word_list:
            combined = character + word
            combined_names.add(combined)

    @classmethod
    def crawl(cls):
        # 텍스트 파일 처리
        text_files = glob.glob('./re/resres2/find*.txt')

        saveData = ""
        found_names = set()

        for text_file_path in text_files:
            count = 0
            with open(text_file_path, 'r', encoding='utf-8') as text_file:
                first_line = text_file.readline().replace('\n', '')
                text = text_file.read()

                for name in cls.combined_names:  # cls를 통해 클래스 변수에 접근
                    if name in text and len(name) >= 3:
                        found_names.add(name)
                        count = count + 1

            # 발견된 이름 저장
            if found_names:
                saveData = saveData + text_file_path + ',' + first_line + ',' + str({count}) + ','
                for name in found_names:
                    saveData = saveData + name + " "
        return saveData, count
    
    @classmethod
    def filed(cls, file):
        found_names = set()
        file.file.seek(0)
        file_name = file.filename
        file_content = file.file.read().decode("utf-8")
        print(file_content)

        for name in cls.combined_names:
            if name in file_content and len(name) >= 3:
                print("1", name)
                found_names.add(name)

        # 발견된 이름 저장
        if found_names:
            print("dfs")
            for name in found_names:
                print("2", name)
                anonymized_name = re.sub(r'[가-힣]', '*', name)
                file_content = file_content.replace(name, anonymized_name)

            # 파일에 수정된 내용 쓰기
            os.makedirs("./csv", exist_ok=True)
            with open(f"./csv/{file_name}", 'w', encoding='utf-8') as output_file:
                output_file.write(file_content)

        print("dsdsf")
        print(file_content)

        return file_content

