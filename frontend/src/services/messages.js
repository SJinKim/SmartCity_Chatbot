import axios from 'axios'

const baseURI = '/api/message'

const fileUploadURI = '/api/upload'

const fileDownloadURI = '/api/files'

const sendMessage = (message) => {
 //   console.log("Sending message:", message);
    const req = axios.post(baseURI, message)
    return req.then(response => response.data)
              /*  return req
                    .then((response) => {
                        setMessages((prevMessages) => [...prevMessages, response.data]);
                        return response.data;
                    })
                    .catch((error) => {
                        console.error("Error sending message:", error);
                        setMessages((prevMessages) => [...prevMessages, message]);
                        throw error;
                    });*/

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

const handleAnleitungButtonClick = (props) => {
    console.log("Anleitung button clicked");
    const anleitungMessage = {
      type: "msg-static",
      message: "Anleitung: here is how to use the chat",
      incoming: false,
      outgoing: true,
      timestamp: Date.now(),
      id: props.messages.length
    };
  
    console.log("Sending Anleitung message:", anleitungMessage);
    props.sendMessage(anleitungMessage);
  };


export default { sendMessage, getMessages, uploadFile, downloadFile, handleAnleitungButtonClick }