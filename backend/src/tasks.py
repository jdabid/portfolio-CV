from src.worker import app


@app.task(name="tasks.ping")
def ping() -> str:
    return "pong"
