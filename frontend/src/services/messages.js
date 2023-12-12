import axios from 'axios'

const baseURI = 'http://localhost:3001/message'

const sendMessage = (message) => {
    const req = axios.post(baseURI, message)
    return req.then(response => response.data)
}

const getMessages = () => {
    const req = axios.get(baseURI)
    return req.then(response => response.data)
}


export default { sendMessage, getMessages }