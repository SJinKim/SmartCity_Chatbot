import { useState } from 'react'
import messageService from './services/messages'
import DashboardLayout from './layouts/dashboard/dashboard'
import chatWebsocket from './services/chatWebsocket'

const socket = chatWebsocket.createSocket()

const App = () => {
  const [newMessage, setNewMessage] = useState('')
  const [messages, setMessages] = useState([])

  chatWebsocket.onMessage(socket, setMessages, setNewMessage, messages)

  const handleNewMessage = (event) => {
    setNewMessage(event.target.value)
  }

  const sendMessage = (event) => {
    event.preventDefault()
    if (newMessage !== '') {
      const message = {
        type: "msg",
        message: newMessage,
        incoming: true,
        outgoing: false,
        timestamp: Date.now(),
        id: messages.length
      }
      socket.send(JSON.stringify(message.message))
      setMessages(messages.concat(message))
      setNewMessage('')
    }
  }

  const handleNewFile = async (event) => {
    const file = event.target.files[0]
    let formData = new FormData()
    formData.append(
      "Sachverhalt",
      file,
      file.name
    )
    const response = await messageService.uploadFile(formData)
    const conMsg = {
      type: "msg-static",
      message: response.message,
      incoming: false,
      outgoing: true,
      timestamp: Date.now(),
      id: messages.length
    }
    setMessages(messages.concat(conMsg))
  }

  const handleAnleitungButtonClick = () => {
    const anleitungMessage = {
        type: "msg-static",
        message: "In diesem Chat können Sie Fragen zu Ihrem Bescheid stellen. Der Chat wird Ihnen den entsprechenden Bescheid zusenden. Sie haben die Möglichkeit, den Bescheid durch Klicken auf den Button 'Herunterladen' herunterzuladen. Zusätzlich können Sie eine Datei hochladen, indem Sie auf den Button 'Hochladen' klicken. Der Chat verwendet diese Datei, um den entsprechenden Bescheid zu finden. Um mehrere Chats zu öffnen, klicken Sie auf den Button 'Neuer Chat'.",
        incoming: false,
        outgoing: true,
        timestamp: Date.now(),
        id: messages.length
    };
    // Directly use setMessages to add the new message
    setMessages(messages.concat(anleitungMessage));
};

  const handleFileDownload = async (event) => {
    event.preventDefault()
    try {
      const response = await messageService.downloadFile('Bescheidvorlage.pdf')
      const file = new Blob(
        [response],
        { type: 'application/pdf' })
      const fileURL = URL.createObjectURL(file)
      window.open(fileURL)
    } catch (exc) {
      const conMsg = {
        type: "msg-static",
        message: 'Es ist noch keine Datei zum Download verfügbar',
        incoming: false,
        outgoing: true,
        timestamp: Date.now(),
        id: messages.length
      }
      setMessages(messages.concat(conMsg))
    }
  }

  const handleClick = (event) => {
    event.preventDefault()
  }

  return (
    <>
      < DashboardLayout
        messages={messages}
        sendMessage={sendMessage}
        handleNewMessage={handleNewMessage}
        newMessage={newMessage}
        handleNewFile={handleNewFile}
        handleFileDownload={handleFileDownload}
        handleClick={handleClick}
        handleAnleitungButtonClick={handleAnleitungButtonClick} // Pass the function as a prop
      />
    </>
  )
}

export default App
