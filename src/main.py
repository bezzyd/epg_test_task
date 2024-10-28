from fastapi import FastAPI


app = FastAPI(
    title='EPG Test Task'
)


@app.get("/")
async def root():
    return
