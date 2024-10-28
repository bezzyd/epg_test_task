import uvicorn
from fastapi import FastAPI

from participants.models import Participant
from participants.services import create_participant


app = FastAPI(
    title='EPG Test Task'
)


@app.post("/api/clients/create")
async def create(participant: Participant):
    return await create_participant(participant)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
