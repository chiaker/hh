import base64
import requests
import json
from pprint import pprint
from PIL import Image, ImageOps
import io

def encode_file(file_path):
    """Кодирует файл в base64 с предварительной инверсией цветов"""
    with Image.open(file_path) as img:
        inverted_img = ImageOps.invert(img.convert('RGB'))

        img_byte_arr = io.BytesIO()
        inverted_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

    return base64.b64encode(img_byte_arr).decode("utf-8")

data = {
    "mimeType": "png",
    "languageCodes": ["ru", "en"],
    "content": encode_file("/content/contentt/wagon_card_K001RF02400.png")
}

url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {:s}".format("t1.9euelZrHmZyTkoyXmpqMksiWx46JkO3rnpWajp3NmIqKnZSNmZ2Qx4vOx4_l8_cPR3Q_-e85Hncg_t3z9091cT_57zkedyD-zef1656VmsqNnZfPl5qRkMiTjZyZyMyY7_zF656VmsqNnZfPl5qRkMiTjZyZyMyY.mkxxdQdu2zQsro9POVScMvklQvQU3jjKeDsIwxzUBtLgJ7qzxsGFPVAN1ZVXI9_ZIQAdAiqTD-vhVgQq1B3lAQ"),
    "x-folder-id": "b1g2u2btrr3vk1kdi3nj",
    "x-data-logging-enabled": "true"
}

response = requests.post(url=url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print("Распознавание успешно!")

    full_text = ""
    for block in result.get("result", {}).get("textAnnotation", {}).get("blocks", []):
        for line in block.get("lines", []):
            for word in line.get("words", []):
                full_text += word.get("text", "") + " "
            full_text += "\n" 

    print("\nРаспознанный текст:")
    print(full_text)

    with open("ocr_result.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    print("\nТекст сохранен в ocr_result.txt")

    print("\nПолный ответ API:")
    pprint(result)
else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)
