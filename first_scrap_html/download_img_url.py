import requests
import os

if not os.path.exists('html'):
    os.makedirs('html')

def download_image(url, post_key, image_index):
    # HTTP GET 요청을 통해 이미지 데이터를 가져옴
    file_name = f"{post_key}_{image_index}.jpg"
    save_path = os.path.join('html', file_name)

    response = requests.get(url)
    # HTTP 응답이 성공적인 경우
    if response.status_code == 200:
        # 바이너리 모드로 파일을 열고 이미지를 저장
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded: {file_name}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

# 이미지 URL
image_url = 'https://scontent-ssn1-1.cdninstagram.com/v/t51.29350-15/461157166_3300053360127164_4550902849778238088_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=18de74&_nc_ohc=2PF1ila3LBkQ7kNvgHJw5es&_nc_ht=scontent-ssn1-1.cdninstagram.com&edm=ANo9K5cEAAAA&_nc_gid=APg-kIAMf2HC2htf3j09cCR&oh=00_AYBFQD4Dog5nAvdO9efLZK94Vys6ZGl_UFMxLZgnEnneXA&oe=66FC23F4'
# 저장할 파일명
key = 'xxzl2n1_bd1'
image_index = 0

# 이미지 다운로드
download_image(image_url, key, image_index)
