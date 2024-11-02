import os
from PIL import Image

# Функция для сжатия изображения до нужного размера (в КБ)
def compress_image(image_path, target_size_kb, step=5, min_quality=10):
    original_size_kb = os.path.getsize(image_path) / 1024
    
    # Если оригинальный размер меньше или равен целевому, пропускаем сжатие
    if original_size_kb <= target_size_kb:
        print(f"File {os.path.basename(image_path)} is already {original_size_kb:.2f} KB, skipping compression.")
        return
    
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img_width, img_height = img.size
        scaling_factor = 1.0
        
        while True:
            # Сжимаем с начальным качеством
            img.save(image_path, format="JPEG", quality=85, optimize=True)
            compressed_size_kb = os.path.getsize(image_path) / 1024
            
            if compressed_size_kb <= target_size_kb:
                break
            
            # Уменьшаем размер изображения для дополнительного сжатия
            scaling_factor *= 0.9
            new_width = int(img_width * scaling_factor)
            new_height = int(img_height * scaling_factor)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        
        for quality in range(85, min_quality - 1, -step):
            img.save(image_path, format="JPEG", quality=quality, optimize=True)
            compressed_size_kb = os.path.getsize(image_path) / 1024
            
            if compressed_size_kb <= target_size_kb or quality == min_quality:
                break
        
        print(f"Compressed {os.path.basename(image_path)} to {compressed_size_kb:.2f} KB")

# Функция для обхода всех папок и сжатия изображений
def compress_images_in_directory(directory, target_size_kb=300):
    for root, _, files in os.walk(directory):
        print(f"Entering directory: {root}")
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file_name)
                compress_image(image_path, target_size_kb)

# Запуск обработки всех папок в текущей директории
compress_images_in_directory('./')
