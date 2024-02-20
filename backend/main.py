import asyncio
import json
import shutil
from fastapi import BackgroundTasks, FastAPI, UploadFile, File, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import yaml
from typing import Dict

from internal.US7_generierung import write_path_to, erstelleBescheidBackground
from internal.US1_loadQA_AzureChat import qa_chain

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Path for uploading Files
@app.post('/api/upload')
async def upload_file(background_tasks: BackgroundTasks, Sachverhalt: UploadFile = File(...)):
    
    filePath = f"./input_docs/{Sachverhalt.filename}"
    with open(filePath, 'w+b') as file:
        shutil.copyfileobj(Sachverhalt.file, file)
    
    response = {
        'file': Sachverhalt.filename,
        'content': Sachverhalt.content_type,
        'path': filePath,
        'message': f"Sie haben die Datei {Sachverhalt.filename} erfolgreich hochgeladen. Im nächsten Schritt wird Ihnen ein vorläufiger Bescheid erstellt. Dies kann einige Minuten dauern."
    }
    background_tasks.add_task(erstelleBescheidBackground, filePath)
    return response

session_manager: Dict[str, WebSocket] = {}

# Path to chat websocket
@app.websocket("/api/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()

    session_manager[client_id] = websocket

    try:
        while True:
            try:
                message = await asyncio.wait_for(websocket.receive_text(), timeout=2)

                if message.lower() == "close":
                    break
                
                # Process received Message
                response = qa_chain(query=message)      
                return_message = {"client_id": client_id, "message": response}                                 
                await websocket.send_text(json.dumps(return_message))
     
            # When no Message received, check if server wants to send a message
            except asyncio.TimeoutError as e:
                #load yaml file
                with open('./internal/config.yaml') as file:
                    config = yaml.safe_load(file)
                if config['erstellt'] is True:
                    response = config["message_str"]
                    write_path_to(key='erstellt', item=False)
                    return_message = {"client_id": client_id, "message": response}                                  
                    await websocket.send_text(json.dumps(return_message))
                    continue
                                                
    except Exception as e:
        print(f"Websocket connection closed {client_id}")
        
    finally:
        del session_manager[client_id]
        print(session_manager)
        await websocket.close()


# Path to the file to be downloaded 
app.mount('/api/files', StaticFiles(directory='output_docs'), name='sachverhalt')

# Path to ui logos
app.mount('/images', StaticFiles(directory='images'), name='images')

# Path for the React-App
app.mount("/", StaticFiles(directory="dist/", html=True), name="dist")



