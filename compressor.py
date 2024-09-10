import os
from PIL import Image

# Путь к директории с изображениями
input_dir = './'
output_dir = './output_directory'

# Создание выходной директории, если она не существует
os.makedirs(output_dir, exist_ok=True)

# Функция для сжатия изображения до нужного размера (в КБ)
def compress_image(image_path, output_path, target_size_kb, step=5, min_quality=10):
    # Получение размера оригинального файла
    original_size_kb = os.path.getsize(image_path) / 1024
    
    # Если оригинальный размер меньше или равен целевому, просто копируем файл
    if original_size_kb <= target_size_kb:
        print(f"File {os.path.basename(image_path)} is already {original_size_kb:.2f} KB, copying without compression.")
        if not os.path.exists(output_path):
            os.rename(image_path, output_path)
        return
    
    with Image.open(image_path) as img:
        # Сначала уменьшим размеры изображения
        img = img.convert("RGB")
        img_width, img_height = img.size
        scaling_factor = 1.0
        
        while True:
            # Пробуем сохранить изображение с начальным качеством и размером
            temp_output = output_path + ".temp.jpg"
            
            # Удаляем временный файл, если он существует
            if os.path.exists(temp_output):
                os.remove(temp_output)
            
            img.save(temp_output, format="JPEG", quality=85, optimize=True)
            compressed_size_kb = os.path.getsize(temp_output) / 1024
            
            if compressed_size_kb <= target_size_kb:
                break
            
            # Уменьшаем размер изображения для большего сжатия
            scaling_factor *= 0.9
            new_width = int(img_width * scaling_factor)
            new_height = int(img_height * scaling_factor)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Теперь уменьшаем качество изображения
        for quality in range(85, min_quality - 1, -step):
            if os.path.exists(temp_output):
                os.remove(temp_output)

            img.save(temp_output, format="JPEG", quality=quality, optimize=True)
            compressed_size_kb = os.path.getsize(temp_output) / 1024
            
            if compressed_size_kb <= target_size_kb or quality == min_quality:
                # Удаляем конечный файл, если он уже существует
                if os.path.exists(output_path):
                    os.remove(output_path)
                
                os.rename(temp_output, output_path)
                break
        
        print(f"Compressed {os.path.basename(image_path)} to {compressed_size_kb:.2f} KB")

# Проход по всем файлам в директории
for file_name in os.listdir(input_dir):
    # Проверка расширения файла (png, jpg, jpeg)
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + ".jpg")
        
        # Сжатие изображения до нужного размера (например, 20 КБ)
        compress_image(input_path, output_path, target_size_kb=200)