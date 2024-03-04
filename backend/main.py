"""
    This is the main/start function of the server including the routes
"""

import asyncio
import shutil
import json
from typing import Dict
from fastapi import (
    BackgroundTasks,
    FastAPI,
    UploadFile,
    File,
    WebSocket,
    WebSocketException,
)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import yaml

from internal.us7_generierung import (
    write_path_to,
    erstelle_bescheid_background,
    add_to_path,
    get_value_from_config,
)
from internal.us10_interaktion import multiple_prompt_chain
from internal.utils import is_result_bescheid

load_dotenv()

app = FastAPI()

session_manager: Dict[str, WebSocket] = {}

origins = ["http://localhost:8000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Path for uploading Files
@app.post("/api/upload")
async def upload_file(
    background_tasks: BackgroundTasks, sachverhalt: UploadFile = File(...)
):
    """This Route recieves a pdf or txt file (sachverhalt) from the client, and triggers
    the a backroundtask to create a bescheid.

    Args:
        background_tasks (BackgroundTasks): triggering the creation of the bescheid
        Sachverhalt (UploadFile, optional): the file to be uploaded

    Returns:
        _type_: json
        sends a response message to the client
    """

    file_path = f"./input_docs/{sachverhalt.filename}"
    with open(file_path, "w+b") as file:
        shutil.copyfileobj(sachverhalt.file, file)

    response = {
        "file": sachverhalt.filename,
        "content": sachverhalt.content_type,
        "path": file_path,
        "message": f"""Sie haben die Datei {sachverhalt.filename} erfolgreich hochgeladen. \
        Im nächsten Schritt wird Ihnen ein vorläufiger Bescheid erstellt. Dies kann einige \
        Minuten dauern.""",
    }
    background_tasks.add_task(erstelle_bescheid_background, file_path)
    return response


# Download
@app.get("/api/download")
# download function implementieren


# Path to chat websocket
@app.websocket("/api/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    this functions accepts a websocket connection to establish a
    bidirectional connection between the server(ai) and the client

    Args:
        websocket (WebSocket): the socket connection
        client_id (str): id of the client
    """
    await websocket.accept()
    session_manager[client_id] = websocket

    try:
        while True:
            try:
                message = await asyncio.wait_for(websocket.receive_text(), timeout=2)

                # Check for termination command
                if message.lower() == "close":
                    break
                # Process received Message
                # response = qa_chain(query=message)
                current_msg = get_value_from_config("message_str")
                response = multiple_prompt_chain(
                    user_query=message, original_bescheid=current_msg
                )
                return_message = {"client_id": client_id, "message": response}
                await websocket.send_text(json.dumps(return_message))

                # add response to yaml
                is_bescheid = is_result_bescheid(response)
                if is_bescheid:
                    write_path_to(key="message_str", item=response)
                else:
                    print("not a bescheid only general answer!")
                add_to_path(key="chatHist", item=response)
            # When no Message received, check if server wants to send a message
            except asyncio.TimeoutError:  # as e:
                # print(f"asyncio timeout: {e}")
                # load yaml file
                with open("./internal/config.yaml", encoding="utf-8") as file:
                    config = yaml.safe_load(file)
                if config["erstellt"] is True:
                    res = config["message_str"]
                    write_path_to(key="erstellt", item=False)
                    return_message = {"client_id": client_id, "message": res}
                    await websocket.send_text(json.dumps(return_message))
                    continue

    except WebSocketException as e:
        print(f"WebSocket error: {e}")
        write_path_to(key="message_str", item="")
        write_path_to(key="chatHist", item=["init"])
        write_path_to(key="sachverhalt", item="")
    finally:
        del session_manager[client_id]
        print(session_manager)
        await websocket.close()
        if len(session_manager) == 0:
            write_path_to(key="message_str", item="")
            write_path_to(key="chatHist", item=["init"])
            write_path_to(key="sachverhalt", item="")


# Path to the file to be downloaded
app.mount("/api/files", StaticFiles(directory="output_docs"), name="sachverhalt")

# Path to ui logos
app.mount("/images", StaticFiles(directory="images"), name="images")

# Path for the React-App
app.mount("/", StaticFiles(directory="dist/", html=True), name="dist")
