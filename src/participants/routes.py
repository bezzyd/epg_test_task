from fastapi import APIRouter
from participants.models import Participant, participants
from participants.services import create_participant, participants_list

router = APIRouter()


@router.post("/api/clients/create")
async def create(participant: Participant):
    return await create_participant(participant)


@router.get("/api/list")
async def get_participants(
        gender: str = None,
        first_name: str = None,
        last_name: str = None,
        sort_by_registration: bool = False
) -> list[Participant]:
    return await participants_list(gender, first_name, last_name, sort_by_registration)
