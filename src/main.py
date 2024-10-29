import uvicorn
from fastapi import FastAPI

from participants.routes import router as participants_router
from evaluations.routes import router as evaluations_router

app = FastAPI()

app.include_router(participants_router)
app.include_router(evaluations_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
