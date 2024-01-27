import asyncio
import shutil
from fastapi import FastAPI, UploadFile, File, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import yaml

from internal.US7_generierung import erstelleBescheid, erstelleGutachten, write_path_to
from internal.US1_loadQA_AzureChat import qa_chain, load_file

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
def upload_file(Sachverhalt: UploadFile = File(...)):
    #hier file = Sachverhalt in unserem Fall
    filePath = f"./input_docs/{Sachverhalt.filename}"
    with open(filePath, 'w+b') as file:
        shutil.copyfileobj(Sachverhalt.file, file)
    
    gutachten = erstelleGutachten(sachverhalt=load_file(filePath), gutachten_path="./output_docs/Gutachten.docx")
    message_str = erstelleBescheid(sachverhalt=load_file(filePath), gutachten_result=gutachten, bescheid_path="./output_docs/Bescheid.docx")

    write_path_to(key='message_str', item=message_str)
    write_path_to(key='erstellt', item=True)
    return {
        'file': Sachverhalt.filename,
        'content': Sachverhalt.content_type,
        'path': filePath,
        'message': f"Sie haben die Datei {Sachverhalt.filename} erfolgreich hochgeladen"
    }


# Path to chat websocket
@app.websocket("/api/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    loop = asyncio.get_event_loop()

    async def receive_messages():
        try:
            while True:
                message = await websocket.receive_text()
            
                # Check for termination command
                if message.lower() == "exit":
                    break

                response = qa_chain(query=message)                                        
                await websocket.send_text(response)
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            await websocket.close()
    
    async def send_messages():
        #load yaml file
        with open('./internal/config.yaml') as file:
            config = yaml.safe_load(file)
        try:
            while True:
                if config["erstellt"]:
                    response = config["message_str"]
                    write_path_to(key='erstellt', item=False)
                    await websocket.send_text(response)

                await asyncio.sleep(1)

        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            await websocket.close()
    try:
        await asyncio.gather(receive_messages(), send_messages())
    except Exception as e:
        print(f"WebSocket error: {e}")


# Path to the file to be downloaded 
app.mount('/api/files', StaticFiles(directory='output_docs'), name='sachverhalt')

# Path for the React-App
app.mount("/", StaticFiles(directory="dist/", html=True), name="dist")



