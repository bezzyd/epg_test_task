import os
from functools import lru_cache

from utils.helpers import overlay_watermark
from .models import Participant, participants

# путь к водяному знаку
WATERMARK_PATH = os.path.join('src/static/watermark.png')
# путь к директории, хранящей аватары участников
AVATAR_IMAGES_DIR = os.path.join('src/static/images')


async def create_participant(participant_data: Participant) -> Participant:

    # проверяем уникальность email
    if any(p['email'] == participant_data.email for p in participants):
        raise ValueError("email already registered")

    participant_data.hash_password()
    # добавляем участника в список
    participants.append(participant_data.dict())

    # накладываем водяной знак и обновляем поле avatar
    participant_data.avatar = await overlay_watermark(participant_data.avatar)

    return participant_data


@lru_cache(maxsize=128)
async def participants_list(
    gender: str,
    first_name: str,
    last_name: str,
    sort_by_registration,
) -> list[dict]:

    filtered_participants = participants

    # фильтрация по полу
    if gender:
        filtered_participants = [p for p in filtered_participants if p['gender'] == gender]

    # фильтрация по имени
    if first_name:
        filtered_participants = [p for p in filtered_participants if p['first_name'].lower() == first_name.lower()]

    # фильтрация по фамилии
    if last_name:
        filtered_participants = [p for p in filtered_participants if p['last_name'].lower() == last_name.lower()]

    # сортировка по дате регистрации
    if sort_by_registration:
        filtered_participants.sort(key=lambda x: x['registration_date'],reverse=True)

    return filtered_participants
