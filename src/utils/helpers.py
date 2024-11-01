import re
import os
import requests
from typing import Tuple
from fastapi import HTTPException
from PIL import Image
from io import BytesIO
from geopy.distance import great_circle

WATERMARK_PATH = os.path.join('src/static/watermark.png')
AVATAR_IMAGES_DIR = os.path.join('src/static/images')


async def overlay_watermark(image_url: str) -> str:
    """Add watermark an avatar"""
    # загрузка аватарки реализована по ссылке, например
    # 'https://masterpiecer-images.s3.yandex.net/4d2ee26774cf11eeaead5696910b1137:upscaled'
    response = requests.get(image_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error loading image")

    # накладываем водяной знак
    avatar = Image.open(BytesIO(response.content))
    watermark = Image.open(WATERMARK_PATH)
    avatar.paste(watermark, (0, 0), watermark)

    # сохраняем измененное изображение
    format_path = await format_filename(image_url)
    result = os.path.join(AVATAR_IMAGES_DIR, f"{format_path}_watermark.png")
    avatar.save(result)

    return result


async def format_filename(filename: str) -> str:
    """Remove invalid characters from the file name"""
    # оставляем только буквы, цифры, подчеркивания, дефисы и точки, заменяем пробелы на нижнее подчеркивание
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename).replace(' ', '_')


async def calculate_distance(coord1: Tuple, coord2: Tuple) -> float:
    """Calculate the great-circle distance between two points"""
    return great_circle(coord1, coord2).kilometers
