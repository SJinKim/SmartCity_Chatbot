#from US3_sacherverhalt import execute_qa_chain
from internal.US7_generierung import write_path_to, erstelleBescheidBackground, add_to_path
from internal.US10_dbtest import test
from internal.US10_initialLLM import *
import yaml
import shutil
import asyncio
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks, FastAPI, UploadFile, File, WebSocket



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
        'message': f"Ihre Datei {Sachverhalt.filename} erfolgreich hochgeladen. Im nächsten Schritt wird Ihnen ein vorläufiger Bescheid erstellt. Dies kann einige Minuten dauern."
    }
    background_tasks.add_task(erstelleBescheidBackground, filePath)
    return response


# Path to chat websocket
@app.websocket("/api/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text('Hallo, wie kann ich Ihnen heute helfen?')

    try:
        while True:
            try:
                query = await asyncio.wait_for(websocket.receive_text(), timeout=2)
                
                # Check for termination command
                if query.lower() == "exit":
                    break
                # Process received Message
                # response = execute_qa_chain(message=query)


                chatHistory = add_to_path(key='chatHist', item=query)

                response = test(query, chatHistory)                          
                await websocket.send_text(response)
                # add response to yaml
                write_path_to(key='message_str', item=response)
                new = add_to_path(key='chatHist', item=response)
                print(new)
     
            # When no Message received, check if server wants to send a message
            except asyncio.TimeoutError as e:
                #load yaml file
                with open('./internal/config.yaml') as file:
                    config = yaml.safe_load(file)
                if config['erstellt'] is True:
                    response = config["message_str"]
                    write_path_to(key='erstellt', item=False)
                    await websocket.send_text(response)
                                                
    except Exception as e:
        print(f"WebSocket error: {e}")
        write_path_to(key='message_str', item='')
        write_path_to(key='chatHist', item=['init'])
    finally:
        await websocket.close()
        write_path_to(key='message_str', item='')
        write_path_to(key='chatHist', item=['init'])
        print('connection closed and message deleted')
        


# Path to the file to be downloaded 
app.mount('/api/files', StaticFiles(directory='output_docs'), name='sachverhalt')

# Path to ui logos
app.mount('/images', StaticFiles(directory='images'), name='images')

# Path for the React-App
app.mount("/", StaticFiles(directory="dist/", html=True), name="dist")