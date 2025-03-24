import requests

champion_ids = [
    266, 103, 84, 166, 12, 32, 34, 1, 523, 22,
    136, 268, 432, 200, 53, 63, 201, 51, 164, 69,
    31, 42, 122, 131, 36, 119, 245, 60, 28, 81,
    9, 114, 105, 3, 41, 86, 150, 79, 104, 887,
    120, 74, 420, 39, 427, 40, 59, 24, 126, 202,
    222, 145, 429, 43, 30, 38, 55, 10, 141, 85,
    121, 203, 240, 96, 897, 7, 64, 89, 876, 127,
    236, 117, 99, 54, 90, 57, 11, 902, 21, 82,
    25, 267, 75, 111, 518, 76, 895, 56, 20, 2,
    61, 516, 80, 78, 555, 246, 133, 497, 33, 421,
    526, 888, 58, 107, 92, 68, 13, 360, 113, 235,
    147, 875, 35, 98, 102, 27, 14, 15, 72, 37,
    16, 50, 517, 134, 223, 163, 91, 44, 17, 412,
    18, 48, 23, 4, 29, 77, 6, 110, 67, 45,
    161, 711, 254, 234, 112, 8, 106, 19, 498, 101,
    5, 157, 777, 83, 350, 154, 238, 221, 115, 26,
    142, 143
]

def download_champion_icon(champion_id):
    url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champion_id}.png"
    response = requests.get(url)
    
    if response.status_code == 200:
        filename = f"{champion_id}.png"
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"아이콘 {champion_id}.png 파일이 성공적으로 다운로드되었습니다.")
    else:
        print(f"아이콘 {champion_id} 다운로드 실패 (상태 코드: {response.status_code})")

if __name__ == "__main__":
    for champion_id in champion_ids:
        download_champion_icon(champion_id)
