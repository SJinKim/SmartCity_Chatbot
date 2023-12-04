# React + Vite

Frontend for SmartCity Chatbot created with vite https://vitejs.dev/

---

## Prerequisites

1. Linux or WSL2 (Ubuntu): 
    - How to install WSL2: 
    https://learn.microsoft.com/en-us/windows/wsl/install
2. Node.js v18.7.1:
    - How to install Node.js, nvm and npm on WSL2: 
    https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl

---

## Get started

1. create a working directory and clone repository:
    `mkdir chatbot && cd chatbot`
    `git clone https://github.com/SJinKim/SmartCity_Chatbot.git`

2. install node-modules:
     `npm install`

3. start server in development mode:
    `npm run dev`
    open browser on http://localhost:5173/

4. make production build:
    `npm run build`

---

## Dependencies

- axios: Promise based HTTP client

## Development Dependencies

- json-server: acts as server during development
    - to run the server:
        1. open a second terminal window and navigate to your working directory
        2. type: `npm run server`
    - view in browser: http://localhost:3001/
    - terminate the server after use with: ctrl + c 

- jest: test library for unit tests



    

