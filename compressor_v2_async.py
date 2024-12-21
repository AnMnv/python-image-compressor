import os
from PIL import Image, ImageFile
import asyncio
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm  # Прогресс-бар

ImageFile.LOAD_TRUNCATED_IMAGES = True  # Для обработки поврежденных изображений

# Функция для сжатия изображения до нужного размера (в КБ)
def compress_image(image_path, target_size_kb, step=5, min_quality=10):
    original_size_kb = os.path.getsize(image_path) / 1024

    if original_size_kb <= target_size_kb:
        return f"File {os.path.basename(image_path)} is already {original_size_kb:.2f} KB, skipping compression."

    try:
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

        return f"Compressed {os.path.basename(image_path)} to {compressed_size_kb:.2f} KB"
    except Exception as e:
        return f"Error processing {image_path}: {e}"

# Асинхронная функция для обработки изображений
async def process_image_async(image_path, target_size_kb, executor, progress_bar):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, compress_image, image_path, target_size_kb)
    progress_bar.update(1)
    return result

# Асинхронная функция для обхода всех папок и обработки изображений
async def compress_images_in_directory_async(directory, target_size_kb=500):
    image_paths = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file_name))

    # Создаем пул процессов для выполнения в фоне
    with ProcessPoolExecutor() as executor:
        with tqdm(total=len(image_paths), desc="Compressing Images") as progress_bar:
            tasks = [
                process_image_async(image_path, target_size_kb, executor, progress_bar)
                for image_path in image_paths
            ]
            results = await asyncio.gather(*tasks)

    # Выводим результат после завершения
    # for result in results:
    #     print(result)

# Запуск асинхронной обработки
if __name__ == "__main__":
    directory = './'
    target_size_kb = 500
    asyncio.run(compress_images_in_directory_async(directory, target_size_kb))
