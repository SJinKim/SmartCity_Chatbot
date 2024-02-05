# Smart-City-Chatbot (LegalBot) 📝➜📚🤖➜📄

*kurze Introduction: evtl. mit Screenshot vom Aufbau und GIF als kurzes Preview*
A helpful AI Chatbot assistant for german legal inquiries. 

This repository contains the code for a chatbot that generates an official notice (`Bescheid`) based on the legal document (`Sachverhalt`) uploaded by the user. The chatbot leverages stored legal statutes from a database (using `LangChain`) including state and federal laws (`Landesgesetze` and `Bundesgesetze`) and utilizes the OpenAi's LLM model (`GPT 3.5`) for text generation.

## Features 

🖊️  **Legal Assistance**: 
The chatbot is context-aware and can answer questions based on the uploaded legal document (`Sachverhalt`) using the LLM model (`GPT 3.5`)

🖊️  **`Bescheid`-Generation**: 
The chatbot analyzes the uploaded legal document (in `DOCX` and `PDF`) and automatically generates a draft of the legal notice (`Bescheid`).

🖊️  **Manual Download**: 
The user can manually download the generated draft of the legal notice in both `DOCX` and `PDF` formats.

## Disclaimer

This chatbot uses AI to generate legal notices (`Bescheid`) from legal documents (`Sachverhalt`) uploaded by users. The chatbot is not a legal advisor and does not ensure the accuracy or validity of the notices or information. Users must verify the notices and information with their own legal counsel or other sources. The chatbot and its creators are not liable for any harm or loss from using the chatbot or the information. Users agree to these terms by using the chatbot.

## Installation 

*bsp für Design-Inspiration*
```bash
Starting the Project in Dev Mode (Without Docker)
```

### Prerequisites

1. **Linux** - Tested with Ubuntu 22.04:
   - For example, using WSL2: Installation Guide
   - If you encounter error code 0x80370102, run `wsl --set-default-version 1` in cmd/Admin-mode.
   - Python 3.10.12 is already installed on Ubuntu 22.04.
3. Run `sudo apt update` and `sudo apt upgrade` before creating a virtual environment.
4. Install `python3.10-venv` with `sudo apt install python3.10-venv`.
5. Install `python3-pip` with `apt install python3-pip`.

### Getting Started

Open the **Linux terminal** (WSL)

1. Navigate to the directory where you want to install the project: `cd <your-home-directory>`
2. Clone the repository: `git clone https://github.com/SJinKim/SmartCity_Chatbot.git`
   - If you encounter an error, run `git config --system core.protectNTFS false` in cmd/Admin-mode.
3. Change to the project directory: `cd SmartCity_Chatbot`
4. Navigate to the backend folder: `cd backend`
5. Create a virtual environment: `python3 -m venv <venv-directory-name>`
6. Activate the virtual environment: `source <venv-directory-name>/bin/activate`
7. Install the required packages: `pip3 install -r requirements.txt`
8. Place the `.env` file (containing the OpenAI API keys) in the backend folder.
9. Start the project: `uvicorn main:app --reload`
10. Open your browser / to stop: `Ctrl+C`
11. Clear the pip cache (if needed): `pip3 cache purge`

Open the **Windows terminal** (PowerShell)

1. Navigate to the directory where you want to install the project: `cd <your-home-directory>`
2. Clone the repository: `git clone https://github.com/SJinKim/SmartCity_Chatbot.git`
   - If you encounter an error, run `git config --system core.protectNTFS false` in cmd/Admin-mode.
3. Change to the project directory: `cd SmartCity_Chatbot`
4. Navigate to the backend folder: `cd backend`
5. Create a virtual environment: `python -m venv <venv-directory-name>`
6. Activate the virtual environment: `source <venv-directory-name>/Scripts/Activate.ps1`
7. Install the required packages: `pip install -r requirements.txt`
8. Place the `.env` file (containing the OpenAI API keys) in the backend folder.
9. Start the project: `uvicorn main:app --reload`
10. Open your browser / to stop: `Ctrl+C`
11. Clear the pip cache (if needed): `pip cache purge`

## Usage

*bsp für Design-Inspiration*
```python
import foobar

# returns 'words'
foobar.pluralize('word')
```

*bsp*
There are two ways to use the chatbot.

1. Web-Interface:
    - Open your browser and go to `http://localhost:5000`.
    - Enter your legal question in the chat window or upload your case file.
    - The chatbot responds with context-relevant information and generates a suitable notice draft from the case.
2. API-Endpoints:
    - Send a POST request to `http://localhost:5000/api/question` with the following parameters:
        - `question`: a string containing your legal question
        - `file`: an optional file containing your case details
    - The chatbot returns a JSON response with the following fields:
        - `status`: a string indicating the success or failure of the request
        - `answer`: a string containing the chatbot's answer to your question
        - `notice`: a string containing the chatbot's notice draft for your case

## Dependencies

### Backend

- `Python 3.10.12` (Linux) and `3.11.7` (Windows).
- LLM Model (`GPT 3.5 turbo`)
- Libraries: `OpenAi` and `LangChain`
- ...

### Frontend

- `JavaScript`
- `React`
- Libaries: `MUI` and `HTML`

## Contributing

*bsp für Inspiration*
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Created By (Contact)

This project was created by Team 13 of the "Practical Lab for Bachelors" of [TUDa](https://www.informatik.tu-darmstadt.de/fb20/index.en.jsp).

- *Github-Badges of members vllt in unterschiedliche Farben für Frontend und Backend*