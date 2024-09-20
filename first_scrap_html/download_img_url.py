import requests

def download_image(url, file_name):
    # HTTP GET 요청을 통해 이미지 데이터를 가져옴
    response = requests.get(url)

    # HTTP 응답이 성공적인 경우
    if response.status_code == 200:
        # 바이너리 모드로 파일을 열고 이미지를 저장
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded: {file_name}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

# 이미지 URL
image_url = 'https://scontent-ssn1-1.cdninstagram.com/v/t51.29350-15/460487865_1333051514340515_9144768729695306591_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=18de74&_nc_ohc=zLIpgjDqnZoQ7kNvgGG9B8I&_nc_ht=scontent-ssn1-1.cdninstagram.com&edm=ANo9K5cEAAAA&_nc_gid=AdVQts1Og8mbaDPDAQ1Qile&oh=00_AYDxUDsUnwUDDdUNzAxhKBEf4OBpnYko8PzaltOsKQWY-A&oe=66F3097E'
# 저장할 파일명
file_name = 'downloaded_image.jpg'

# 이미지 다운로드
download_image(image_url, file_name)
