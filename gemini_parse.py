import google.generativeai as genai
import os
from pathlib import Path
from PIL import Image
import time

class GeminiImageParser:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.current_key_index = 0
        self.model = None
        self.initialize_model()

    def initialize_model(self):
        genai.configure(api_key=self.api_keys[self.current_key_index])
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')

    def rotate_api_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        print(f"Переключаем на API ключ #{self.current_key_index + 1}")
        self.initialize_model()
        time.sleep(1)  

    def parse_images(self, input_folder, output_file):
        try:
            output_dir = os.path.dirname(output_file)
            if output_dir:
                Path(output_dir).mkdir(parents=True, exist_ok=True)

            supported_extensions = ['.png', '.jpg', '.jpeg', '.webp']
            image_files = sorted([
                f for f in os.listdir(input_folder)
                if os.path.splitext(f)[1].lower() in supported_extensions
            ])

            if not image_files:
                print("Не найдено изображений для обработки.")
                return


            with open(output_file, 'w', encoding='utf-8') as out_file:
                for idx, img_file in enumerate(image_files, 1):
                    image_path = os.path.join(input_folder, img_file)
                    print(f"Обработка {idx}/{len(image_files)}: {img_file}...", end=" ", flush=True)

                    success = False
                    attempts = 0
                    max_attempts = len(self.api_keys) * 2  

                    while not success and attempts < max_attempts:
                        try:
                            img = Image.open(image_path)
                            if img.mode != 'RGB':
                                img = img.convert('RGB')

                            response = self.model.generate_content([
                                "Извлеки весь текст с изображения дословно, без изменений, "
                                "без пояснений и форматирования. Только оригинальный текст.",
                                img
                            ])

                            out_file.write(f"=== {img_file} ===\n")
                            out_file.write(response.text.strip())
                            out_file.write("\n\n")
                            print("Успешно")
                            success = True

                        except Exception as e:
                            attempts += 1
                            if "quota" in str(e).lower() or "limit" in str(e).lower():
                                print("Лимит исчерпан.", end=" ")
                                self.rotate_api_key()
                            else:
                                print(f"Ошибка: {str(e)}")
                                break

                    if not success:
                        print("Не удалось обработать после всех попыток")

            print(f"\nГотово! Результаты сохранены в: {os.path.abspath(output_file)}")

        except Exception as e:
            print(f"Критическая ошибка: {str(e)}")

if __name__ == "__main__":
    API_KEYS = [
        "AIzaSyBEDWHjsiwkCp-wOrIkrqbaFUAXHhsSKiU",
        "AIzaSyDTL_bSkpcTzJCbAnraHFECXrEH2pqhCmU",
        "AIzaSyD2h9apYcUTsTp86BE36lbuGehsZRX3QnM"
    ]

    INPUT_FOLDER = "contentt"  
    OUTPUT_FILE = "output/parsed_text.txt"  

    parser = GeminiImageParser(api_keys=API_KEYS)
    parser.parse_images(input_folder=INPUT_FOLDER, output_file=OUTPUT_FILE)
