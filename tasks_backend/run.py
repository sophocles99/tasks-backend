import os

import uvicorn
from dotenv import load_dotenv

load_dotenv(override=True)
RELOAD = os.environ.get("RELOAD", "False").lower() == "true"


def run_server():
    uvicorn.run("tasks_backend.app:app", host="localhost", port=8000, reload=RELOAD)


if __name__ == "__main__":
    run_server()
