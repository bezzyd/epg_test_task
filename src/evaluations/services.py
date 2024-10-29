from fastapi import HTTPException
from typing import Dict

from utils.mail_service import send_mail
from participants.models import Participant, participants


async def evaluate_participant(sender_id: int, recipient_id: int, evaluation) -> Dict[str, int]:
    """Evaluating other participant and check for mutual match"""
    # проверяем, чтобы у отправителя и получателя не совпадали айдишники
    if sender_id == recipient_id:
        raise HTTPException(status_code=400, detail="You cannot evaluate yourself")

    # проверяем, существует ли получатель оценки с данным id
    recipient = next((p for p in participants if p['id'] == recipient_id), None)

    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    # убедимся, что отправитель существует
    sender = next((p for p in participants if p['id'] == sender_id), None)

    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")

    # сохраняем оценку
    recipient['evaluations'].append(evaluation.dict())

    # проверяем оценки отправителя и если у него есть оценка от получателя, то это взаимная симпатия
    for evaluation in sender['evaluations']:
        if evaluation['sender_id'] == recipient_id:
            await send_mail(recipient['email'], sender['email'], sender['first_name'])
            await send_mail(sender['email'], recipient['email'], recipient['first_name'])

    return {
        "message": "Evaluation submitted successfully",
        "recipient_id": recipient_id,
    }
