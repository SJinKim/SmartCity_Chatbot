"""
    This is the main/start function of the server including the routes
"""
import asyncio
import shutil
from fastapi import BackgroundTasks, FastAPI, UploadFile, File, WebSocket, WebSocketException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import yaml

from internal.us3_sacherverhalt import qa_chain
from internal.us7_generierung import write_path_to, erstelle_bescheid_background

load_dotenv()

app = FastAPI()

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
async def upload_file(background_tasks: BackgroundTasks, sachverhalt: UploadFile = File(...)):
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


# Path to chat websocket
@app.websocket("/api/chat")
async def websocket_endpoint(websocket: WebSocket):
    """this functions accepts a websocket connection to establish a
    bidirectional connection between the server(ai) and the client

    Args:
        websocket (WebSocket): the websocket
    """
    await websocket.accept()
    await websocket.send_text("Hallo, wie kann ich Ihnen heute helfen?")

    try:
        while True:
            try:
                message = await asyncio.wait_for(websocket.receive_text(), timeout=2)

                # Check for termination command
                if message.lower() == "exit":
                    break
                # Process received Message
                response = qa_chain(query=message)
                await websocket.send_text(response)

            # When no Message received, check if server wants to send a message
            except asyncio.TimeoutError as e:
                print(f"asyncio timeout: {e}")
                # load yaml file
                with open("./internal/config.yaml", encoding='utf-8') as file:
                    config = yaml.safe_load(file)
                if config["erstellt"] is True:
                    response = config["message_str"]
                    write_path_to(key="erstellt", item=False)
                    await websocket.send_text(response)

    except WebSocketException as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()


# Path to the file to be downloaded
app.mount("/api/files", StaticFiles(directory="output_docs"), name="sachverhalt")

# Path to ui logos
app.mount("/images", StaticFiles(directory="images"), name="images")

# Path for the React-App
app.mount("/", StaticFiles(directory="dist/", html=True), name="dist")
