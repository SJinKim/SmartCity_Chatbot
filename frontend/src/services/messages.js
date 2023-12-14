import axios from 'axios'

const baseURI = 'http://localhost:3001/message'

const fileUploadURI = ''

const sendMessage = (message) => {
    const req = axios.post(baseURI, message)
    return req.then(response => response.data)
}

const getMessages = () => {
    const req = axios.get(baseURI)
    return req.then(response => response.data)
}

const uploadFile = (file) => {
    const req = axios.post(fileUploadURI, file)
    return req.then(response => response.data)
}


export default { sendMessage, getMessages, uploadFile }