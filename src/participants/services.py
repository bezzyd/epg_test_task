import os
import requests

from fastapi import HTTPException
from PIL import Image
from io import BytesIO

from .utils import format_filename
from .models import Participant, participants

WATERMARK_PATH = os.path.join('watermark.png')
AVATAR_IMAGES_DIR = os.path.join('images')


async def overlay_watermark(image_url: str) -> str:
    """
    Asynchronous function for watermarking an avatar
    """
    # загрузка аватарки, сейчас реализовано по ссылке, например
    # 'https://masterpiecer-images.s3.yandex.net/4d2ee26774cf11eeaead5696910b1137:upscaled'
    response = requests.get(image_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="error loading image")

    # накладываем водяной знак
    avatar = Image.open(BytesIO(response.content))
    watermark = Image.open(WATERMARK_PATH)
    avatar.paste(watermark, (0, 0), watermark)

    # сохраняем измененное изображение
    sanitize_path = await format_filename(image_url)
    result = os.path.join(AVATAR_IMAGES_DIR, f"{sanitize_path}_watermark.png")
    avatar.save(result)

    return result


async def create_participant(participant_data: Participant) -> Participant:
    participant_data.hash_password()
    # добавляем участника в список
    participants.append(participant_data.dict())

    # накладываем водяной знак и обновляем поле avatar
    participant_data.avatar = await overlay_watermark(participant_data.avatar)

    return participant_data
