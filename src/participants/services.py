import os
from fastapi import HTTPException
from aiocached import cached
from typing import List, Dict

from utils.helpers import overlay_watermark, calculate_distance
from .models import Participant, participants

# путь к водяному знаку
WATERMARK_PATH = os.path.join('src/static/watermark.png')
# путь к директории, хранящей аватары участников
AVATAR_IMAGES_DIR = os.path.join('src/static/images')


async def create_participant(participant_data: Participant) -> Participant:

    # проверяем уникальность email
    if any(p['email'] == participant_data.email for p in participants):
        raise HTTPException(status_code=409, detail='Email already registered')

    participant_data.hash_password()

    # накладываем водяной знак и обновляем поле avatar
    participant_data.avatar = await overlay_watermark(participant_data.avatar)

    # добавляем участника в список
    participants.append(participant_data.dict())

    return participant_data


@cached(ttl=60)
async def participants_list(
    gender: str,
    first_name: str,
    last_name: str,
    sort_by_registration,
    user_email: str,
    max_distance_km: float,
) -> List[Dict]:

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
        filtered_participants.sort(key=lambda x: x['registration_date'], reverse=True)

    # поиск других юзеров по расстоянию
    if max_distance_km is not None:
        user_participant = next((p for p in filtered_participants if p['email'] == user_email), None)

        if not user_participant:
            raise HTTPException(
                status_code=404,
                detail="User not found, you must registered first and provide your email"
            )

        user_coords = (user_participant['latitude'], user_participant['longitude'])

        participants_within_distance = []

        for participant in participants:
            # исключаем самого пользователя из списка
            if participant['email'] != user_email:
                distance = await calculate_distance(user_coords, (participant['latitude'], participant['longitude']))
                if distance <= max_distance_km:
                    participants_within_distance.append(participant)

        filtered_participants = participants_within_distance

    return filtered_participants
