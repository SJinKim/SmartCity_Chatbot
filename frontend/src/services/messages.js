import axios from 'axios'

const baseURI = '/api/message'

const fileUploadURI = '/api/upload'

const fileDownloadURI = '/api/files'

/**
 * sends message to backend as html post -> not used
 * 
 * @param {string} message to be send to backend 
 * @returns {JSON} the response obejct
 */
const sendMessage = (message) => {
    const req = axios.post(baseURI, message)
    return req.then(response => response.data)
}

/**
 * gets messages from backend -> not used
 * 
 * @returns {JSON} the response object
 */
const getMessages = () => {
    const req = axios.get(baseURI)
    return req.then(response => response.data)
}

/**
 * makes html post request to backend for formdata file
 * 
 * @param {Object} file 
 * @returns {JSON} response message from backend
 */
const uploadFile = async (file) => {
    const response = await axios.post(fileUploadURI, file)
    return response.data
}

/**
 * makes get request to backend for file download
 * 
 * @param {string} filename 
 * @returns {JSON} the donwloaded byte stream from backend
 */
const downloadFile = async (filename) => {
    const response = await axios.get(`${fileDownloadURI}/${filename}`,
        { responseType: 'blob' })
    return response.data
}

export default { sendMessage, getMessages, uploadFile, downloadFile }