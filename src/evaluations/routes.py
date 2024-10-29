from fastapi import APIRouter

from .services import evaluate_participant
from .models import Evaluation

router = APIRouter()


@router.post("/api/clients/{id}/match")
async def create_evaluate(id: int, evaluation: Evaluation):
    return await evaluate_participant(evaluation.sender_id, id, evaluation)
