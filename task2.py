from PIL import Image
import requests
from io import BytesIO
import os
import logging

logging.basicConfig(filename='image_processing.log', level=logging.INFO)


def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except requests.exceptions.RequestException as e:
        logging.error(
            f"Ошибка при загрузке изображения с URL: {url}. Ошибка: {str(e)}")
        return None


def resize_image(image, max_size=1000):
    try:
        width, height = image.size
        if width > max_size or height > max_size:
            if width > height:
                new_width = max_size
                new_height = int(max_size * width / max(width, height))
            else:
                new_width = int(max_size * width / max(width, height))
                new_height = max_size
            return image.resize((new_width, new_height), Image.LANCZOS)
        return image
    except Exception as e:
        logging.error(
            f"Произошла ошибка при изменении размера изображения: {str(e)}")
        return None


def save_image(image, file_name):
    try:
        image.save(file_name, "JPEG")
        logging.info(f"Изображение успешно сохранено как {file_name}.")
    except Exception as e:
        logging.error(f"Произошла ошибка при сохранении изображения: {str(e)}")


def process_image(url, output_folder="images", max_size=1000):
    os.makedirs(output_folder, exist_ok=True)
    image = download_image(url)
    if image:
        image = resize_image(image, max_size)
        if image:
            file_name = os.path.join(output_folder,
                                     f"download_{url.split('/')[-1]}")
            save_image(image, file_name)


if __name__ == "__main__":
    url_list = [
        'https://w.forfun.com/fetch/94/94e2c09615bf9c615289fb4a5e8b94f5.jpeg',
        'https://i.pinimg.com/originals/87/48/07/874807f8cb45e17f44312eb761261ad9.jpg'
    ]
    for url in url_list:
        process_image(url)
