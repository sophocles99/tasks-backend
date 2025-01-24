import uvicorn

def run_server():
    uvicorn.run("tasks_backend.app:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    run_server()
