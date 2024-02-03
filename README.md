# SmartCity_Chatbot

## How to install and start project in developement mode (without docker) 

## prerequisites

1. Linux - Testet with Ubuntu 22.04:
    - for example with WSL2: https://learn.microsoft.com/en-us/windows/wsl/install
2. Python 3.10.12 -> already installed on ubuntu 22.04

## get started:
open linux terminal:

1. cd to directory where to install the project: `cd <your-home-dir-name>`
2. clone repository: `git clone https://github.com/SJinKim/SmartCity_Chatbot.git`
3. cd in to Project: `cd SmartCity_Chatbot`
4. cd in backend folder: `cd backend`
5. create virtual environment: `python3 -m venv <venv-dir-name>`
6. activate venv: `source venv/bin/activate`
7. install requirements: `pip install -r requirements.txt`
8. place the .env file (File with the openai api keys) in the backend folder 
9. start project: `uvicorn main:app --reload`
10. open browser

