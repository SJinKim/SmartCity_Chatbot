import shutil
from fastapi import FastAPI, UploadFile, File, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI

import yaml

from backend.US7_generierung import erstelleBescheid, erstelleGutachten, write_path_to
from backend.US1_loadQA_AzureChat import qa_chain

load_dotenv()

#Simple method to get ai answer -> just for development
def get_ai_answer(user_message):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professor for computer science"},
            {"role": "user", "content": user_message}
        ]
    )
    content = completion.choices[0].message.content
    return content

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
def upload_file(file: UploadFile = File(...)):
    #hier file = Sachverhalt in unserem Fall
    fileExt = file.filename.split(".").pop() #eg: docx, pdf...etc
    filePath = f"uploadedFiles/{file.filename}.{fileExt}"
    with open(filePath, 'w+b') as file:
        shutil.copyfileobj(file.file, file)
    # TODO call method from backend Team: Sachverhalt Vectore Store
    message_str = erstelleBescheid(sachverhalt=filePath, prüfungsergebnis=erstelleGutachten(sachverhalt=filePath, gutachten_path="downloadFiles"), bescheid_path="downloadFiles")
    # safe str in yaml file
    write_path_to(key='message_str', item=message_str)
    return {
        'file': file.filename,
        'content': file.content_type,
        'path': filePath,
        'message': f"Sie haben die Datei {file.filename} erfolgreich hochgeladen"
    }


# Path to chat websocket
@app.websocket("/api/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    #load yaml file
    with open('config.yaml') as file:
        config = yaml.safe_load(file)
    try:
        while True:
            message = await websocket.receive_text()
            if config["erstellt"]:
                response = config["message_str"]
                write_path_to(key='erstellt', item=False)
            # Check for termination command
            if message.lower() == "exit":
                break
            # TODO call the correct method for chatbot
            # Allgemeine Fragen
            response = qa_chain(query=message)
            await websocket.send_text(response)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()


# Path to the file to be downloaded 
app.mount('/api/files', StaticFiles(directory='downloadFiles'), name='sachverhalt')
app.mount('/api/files1', StaticFiles(directory='gutachtenBescheid'), name='sachverhalt')

# Path for the React-App
app.mount("/", StaticFiles(directory="dist/", html=True), name="dist")



