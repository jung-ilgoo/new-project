from PIL import Image

# JPEG 파일 열기
im = Image.open("input.jpg")

# PNG 형식으로 저장하기
im.save("output.png", "PNG")
