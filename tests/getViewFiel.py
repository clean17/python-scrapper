import os
import shutil

def find_html_jsp_files(directory, save_directory):
    matching_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.html', '.jsp')):
                full_path = os.path.join(root, file)
                matching_files.append(full_path)

    # 저장할 경로 없으면 생성
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for file in matching_files:
        destination = os.path.join(save_directory, os.path.basename(file))
        shutil.copy(file, destination)  # 저장

    print(f"Copied {len(matching_files)} files to {save_directory}")

directory_path = 'E:/project/MOJAMS-D/MOJAMS/src/main'
save_directory = 'E:/241023'
find_html_jsp_files(directory_path, save_directory)
