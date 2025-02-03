import os

import uvicorn

RELOAD = os.environ.get("RELOAD", False)

def run_server():
    uvicorn.run("tasks_backend.app:app", host="localhost", port=8000, reload=RELOAD)


if __name__ == "__main__":
    run_server()
