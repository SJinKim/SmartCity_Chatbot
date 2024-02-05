# SmartCity Chatbot

## Installation and Starting the Project in Dev Mode (Without Docker)

### Prerequisites

1. **Linux** - Tested with Ubuntu 22.04:
   - For example, using WSL2: Installation Guide
   - If you encounter error code 0x80370102, run `wsl --set-default-version 1` in cmd/Admin-mode.
   - Python 3.10.12 is already installed on Ubuntu 22.04.
3. Run `sudo apt update` and `sudo apt upgrade` before creating a virtual environment.
4. Install `python3.10-venv` with `sudo apt install python3.10-venv`.
5. Install `python3-pip` with `apt install python3-pip`.

### Getting Started

Open the Linux terminal (WSL) with Python version 3.10.12.

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

Open the Windows terminal (PowerShell) with Python version 3.11.7.

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


