import axios from 'axios'

const baseURI = '/api/message'

const fileUploadURI = '/api/upload'

const fileDownloadURI = '/api/files'

const sendMessage = (message) => {
    const req = axios.post(baseURI, message)
    return req.then(response => response.data)
}

const getMessages = () => {
    const req = axios.get(baseURI)
    return req.then(response => response.data)
}

const uploadFile = async (file) => {
    const response = await axios.post(fileUploadURI, file)
    return response.data
}

const downloadFile = async (filename) => {
    const response = await axios.get(`${fileDownloadURI}/${filename}`,
    {responseType: 'blob'})
    return response.data
}


export default { sendMessage, getMessages, uploadFile, downloadFile }