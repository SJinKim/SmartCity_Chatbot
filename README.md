# Smart-City-Chatbot (LegalBot) 📄➜📚🤖➜🪄📝➜✉️

This repository provides a user-friendly AI chatbot assistant to support German legal inquiries. The chatbot generates legal notices (`Bescheide`) based on user-uploaded case files (`Sachverhalte`), offers customization options before finalizing the file, and has potential for further expansion and integration.

## Features 
![](https://i.postimg.cc/zXWRQ7QT/SCB-preview.png)

📌 The chatbot is still under development and based on a dataset of German federal laws and the state laws of Baden-Württemberg.

🖊️  **Smart Legal Assistance**: 
The chatbot analyzes the uploaded case file (`Sachverhalte`) in `DOCX` or `PDF` format and offers context-aware responses leveraging OpenAI's GPT-3.5 language model. 

🖊️  **Automated Notice Generation**: 
The chatbot generates draft notices (`Bescheide`) based on the uploaded case file and the user's input. The draft notice includes the decision of the authority, the legal justification for the decision, and information on legal remedies.

🖊️  **Customization**: 
The user can review and edit the generated draft notice before finalizing it through customization options such as adding additional information or changing the existing content.

🖊️  **Downloadable**: 
The user can manually download the generated legal notice in text format (`DOCX`).


## Walkthrough (Tips)
🏃 Ask the chatbot any question you like

🏃 Upload case file by clicking on the upload button
- now chatbot creates a legal notice for you
- you will get the created legal notice as a message
      
🏃 Adjust the created legal notice according to the desired adjustments
- for best adjustment results use phrases like:
- input: "Ändere mir den Bescheid [mention the part to be adjusted] [state your desired adjustment]"
         
🏃 Ask questions about the uploaded case file or generated legal notice if you like
- for best results use the specific words in your question: "Sachverhalt" or "Bescheid"
      
🏃 Download generated legal notice by clicking the download button


## Disclaimer
📌 The chatbot is not a substitute for legal advice from a qualified attorney.

This chatbot uses AI to generate legal notices from case files uploaded by users. The chatbot is not a legal advisor and does not ensure the accuracy or validity of the notices or information. Users must verify the notices and information with their own legal counsel or other sources. The chatbot and its creators are not liable for any harm or loss from using the chatbot or the information. Users agree to these terms by using the chatbot.


## Installation 

### Prerequisites

#### Linux (Python v3.10.12)
- Install Python version via Ubuntu 22.04 using WSL2: `https://learn.microsoft.com/en-us/windows/wsl/` (Installation Guide).
   - If you encounter error code 0x80370102, run `wsl --set-default-version 1` in CMD as Administrator.
   - To use WSL with VSCode: `https://code.visualstudio.com/docs/remote/wsl` (WSL Extension).
- Node.js v18.7.1:
    - How to install Node.js, nvm and npm on WSL2: 
    `https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl`

Open WSL to run:
- `sudo apt update` and `sudo apt upgrade` before creating a virtual environment.
- `python3.10-venv` with `sudo apt install python3.10-venv`.
- `python3-pip` with `apt install python3-pip`.

#### Windows (Python v3.11.7)
- Install Python version: `https://www.python.org/downloads/release/python-3117/`.
   - Installation Guide: `https://docs.python.org/3/using/windows.html`.
-  Node.js v18.7.1:
   - How to install: `https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-overview`

#### 📌 Place Azure OpenAI "API key" and "endpoint" in environment file (.env)
1. Navigate to project's `backend folder` and open the `.env` file.
2. Replace only these following placeholders (e.g. "YOUR_AZURE_OPENAI_KEY") with your actual credential values:
```
AZURE_OPENAI_KEY="YOUR_AZURE_OPENAI_KEY"
AZURE_OPENAI_ENDPOINT="YOUR_AZURE_ENDPOINT_URL"
```
3. Save the file ✅


### Getting Started (setup for development environment)

#### Backend

##### WSL (Linux-Terminal)
1. Clone the GitHub repository `git clone https://github.com/SJinKim/SmartCity_Chatbot.git`.
   - If you encounter an error, run `git config --system core.protectNTFS false` in CMD as Administrator.
2. Navigate to the directory where you want to install the project `cd <your-home-directory>`.
3. Navigate to project directory `cd SmartCity_Chatbot`.
4. Navigate to backend folder `cd backend`.
5. Create a virtual environment `python3 -m venv <venv-directory-name>`.
6. Activate the created virtual environment `source <venv-directory-name>/bin/activate`.
7. Install the required packages `pip3 install -r requirements.unix.txt`.
8. Check if your `.env` file (containing the Azure OpenAI credentials) is in the root directory of backend folder.
9. Start backend server `uvicorn main:app` / optional `uvicorn main:app --reload` to enable auto-reload.
10. Open browser via `http://127.0.0.1:8000` / to quit `Ctrl+C`.

##### PowerShell (Windows-Terminal)
1. Clone the GitHub repository `git clone https://github.com/SJinKim/SmartCity_Chatbot.git`.
   - If you encounter an error, run `git config --system core.protectNTFS false` in CMD as Administrator.
2. Navigate to the directory where you want to install the project `cd <your-home-directory>`.
3. Navigate to project directory `cd SmartCity_Chatbot`.
4. Navigate to backend folder `cd backend`.
5. Create a virtual environment `python -m venv <venv-directory-name>`.
6. Activate the created virtual environment `./<venv-directory-name>/Scripts/Activate.ps1`.
7. Install the required packages `pip install -r requirements.win.txt`.
8. Check if your `.env` file (containing the Azure OpenAI credentials) is in the root directory of backend folder.
9. Start backend server `uvicorn main:app` / optional `uvicorn main:app --reload` to enable auto-reload.
10. Open browser via `http://127.0.0.1:8000` / to quit `Ctrl+C`.


#### Frontend
📌 Assuming **Node.js(18.7.1), nvm and npm** are installed: 

1. Navigate to project directory `cd SmartCity_Chatbot`.
2. Navigate to frontend folder `cd frontend`.
3. Install node-modules `npm install`.
4. Start frontend server in development mode `npm run dev`.
5. Open browser via `http://localhost:5173/`.
6. Make production build `npm run build`.
7. Build and deploy to backend `npm run build:deploy`.


## Usage

### With Docker
📌 Assuming **Docker Desktop** is installed `https://www.docker.com/products/docker-desktop/`.
1. Start the docker daemon (by simply starting docker destop)
2. fill in "AZURE_OPENAI_KEY " and "AZURE_OPENAI_ENDPOINT" in the env file.
3. opens the Windows console, switch to the folder where docker-compose.yaml is located.
   relative path : `../SmartCity_Chatbot/backend/`
4. run `docker-compose up -d` in the console
5. open http://localhost:8000 in your web browser
6. use the application 

### Without Docker
📌 See "Installation" section.


## Dependencies
![](https://i.postimg.cc/9Q85M0YS/service-arch.png)

### Backend
- **Python** (Linux: `v3.10.12` | Windows: `v3.11.7`) `https://www.python.org/`
- **Azure OpenAi Service** (LLM-Model: `GPT 3.5 Turbo`, Embedding-Model: `text-embedding-ada-002`)
- **LangChain** `https://www.langchain.com/`
- **FastAPI** `https://fastapi.tiangolo.com/`

### Frontend
- **JavaScript** (`https://learn.microsoft.com/en-us/windows/dev-environment/javascript/`)
- **React** `https://react.dev/`
- **Material-UI** (MUI) `https://mui.com/`
- **Node.js** (`v18.7.1`) `https://nodejs.org/en`
- **Vite** `https://vitejs.dev/`
- **axios** `https://axios-http.com/`


## Contributing (Open Source)
- Pull requests are welcome, but for major changes, please open an issue first to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)

## Created By (Contact)

[![](https://i.postimg.cc/hhwyhr9L/SCB-frontent-a.png)](https://github.com/vasilevaana)
[![](https://i.postimg.cc/wMtykcC4/SCB-frontent-m.png)](https://github.com/comdyax)
[![](https://i.postimg.cc/Btt7qy1Z/SCB-backend-g.png)](https://github.com/Gii-DE)
[![](https://i.postimg.cc/ZCdfNdc1/SCB-backend-j.png)](https://github.com/Emmaliyt)
[![](https://i.postimg.cc/G4nXxmg9/SCB-backend-sj.png)](https://github.com/SJinKim)

© 2024 for the "Practical Lab for Bachelors" of the TUDa in cooperation with [[ui!] Urban Software Institute](https://www.ui.city/). 
