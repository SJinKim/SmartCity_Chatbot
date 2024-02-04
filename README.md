# SmartCity_Chatbot

## How to install and start project in developement mode (without docker) 

## prerequisites

1. Linux - Testet with Ubuntu 22.04:
- for example with WSL2: https://learn.microsoft.com/en-us/windows/wsl/install
- if Error 0x80370102, run `wsl --set-default-version 1` in cmd/admin
2. Python 3.10.12 -> already installed on ubuntu 22.04
3. run `sudo apt update` and `sudo apt upgrade` before creating a venv
4. run `sudo apt install python3.10-venv`
5. run `apt install python3-pip`

## get started:
open linux terminal (wsl): Python Version 3.10.12

1. cd to directory where to install the project: `cd <your-home-dir-name>`
2. clone repository: `git clone https://github.com/SJinKim/SmartCity_Chatbot.git`
if error, run `git config --system core.protectNTFS false` in cmd/admin
3. cd in to Project: `cd SmartCity_Chatbot`
4. cd in backend folder: `cd backend`
5. create virtual environment: `python3 -m venv <venv-dir-name>`
6. activate venv: `source <venv-dir-name>/bin/activate`
7. install requirements: `pip3 install -r requirements.txt`
8. place the .env file (File with the openai api keys) in the backend folder 
9. start project: `uvicorn main:app --reload`
10. open browser / to close: `Strg+c`
11. clear pip cache (if needed): `pip3 cache purge`

open windows terminal (powershell): Python Version 3.11.7

1. cd to directory where to install the project: `cd <your-home-dir-name>`
2. clone repository: `git clone https://github.com/SJinKim/SmartCity_Chatbot.git`
if error, run `git config --system core.protectNTFS false` in cmd/admin
3. cd in to Project: `cd SmartCity_Chatbot`
4. cd in backend folder: `cd backend`
5. create virtual environment: `python -m venv <venv-dir-name>`
6. activate venv: `source <venv-dir-name>/Scripts/Activate.ps1`
7. install requirements: `pip install -r requirements.txt`
8. place the .env file (File with the openai api keys) in the backend folder 
9. start project: `uvicorn main:app --reload`
10. open browser / to close: `Strg+c`
11. clear pip cache (if needed): `pip cache purge`

