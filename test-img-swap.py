import os
import shutil

# 원본 파일과 대상 디렉토리 설정
source_file = r"E:\project\테스트 파일\5.png"
target_directory = r"E:\laris_data\FILE\ARCHIVES_REP\2024\08\29\534\THUMB"

# 대상 디렉토리의 모든 파일 순회
for filename in os.listdir(target_directory):
    target_file_path = os.path.join(target_directory, filename)

    # 파일이 실제 파일인지 확인
    if os.path.isfile(target_file_path):
        # 파일을 덮어씀 (내용을 source_file로 대체)
        shutil.copy2(source_file, target_file_path)

print("모든 파일이 대체되었습니다.")
