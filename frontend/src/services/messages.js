import axios from 'axios'

const baseURI = 'http://localhost:3001/message'

const fileUploadURI = 'http://localhost:5173'

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

const uploadFile = (file) => {
    const req = axios
        .post(fileUploadURI, file, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    return req.then(response => response.data)
}
const handleAnleitungButtonClick = () => {
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


export default { sendMessage, getMessages, uploadFile, handleAnleitungButtonClick }