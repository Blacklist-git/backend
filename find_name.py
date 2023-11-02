import glob

def findName():
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

    # 텍스트 파일 처리
    text_files = glob.glob('re/resres2/find*.txt')

    # savedData_file =  open('full_name.txt', 'w', encoding='utf-8')
    saveData = ""

    for text_file_path in text_files:
        found_names = set()
        count = 0
        with open(text_file_path, 'r', encoding='utf-8') as text_file:
            first_line = text_file.readline().replace('\n', '')
            text = text_file.read()

            for name in combined_names:
                if name in text and len(name) >= 3:
                    found_names.add(name)
                    count = count + 1

        # 발견된 이름 저장
        if found_names:
            print(f"type: {type(text_file_path)}")
            print(text_file_path)
            print(f"type: {type(first_line)}")
            print(f"type: {type(count)}")
            saveData = text_file_path+','+first_line+','+str({count})+','
            for name in found_names:
                saveData =saveData + name+" "
                print(saveData)
            print(f"type: {type(str(saveData))}")
        return saveData

            #   파일에 텍스트 저장하기
        #     savedData_file.write(f"파일 '{text_file_path}'에서 찾은 이름:\nurl : {first_line}발견한 이름 수 : {count}\n\n")
        #     for name in found_names:
        #         savedData_file.write(name + '\n')
        # savedData_file.write(name + '\n\n\n')
