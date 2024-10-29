from fastapi import APIRouter
from typing import Optional, List

from participants.models import Participant, participants
from participants.services import create_participant, participants_list

router = APIRouter()


@router.post("/api/clients/create")
async def create(participant: Participant) -> None:
    return await create_participant(participant)


@router.get("/api/list")
async def get_participants(
        gender: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        sort_by_registration: Optional[bool] = False,
        user_email: Optional[str] = None,
        max_distance_km: Optional[float] = None,
) -> List[Participant]:
    return await participants_list(gender, first_name, last_name, sort_by_registration, user_email, max_distance_km)
