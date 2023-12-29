import { useEffect, useState } from 'react'
import messageService from './services/messages'
import DashboardLayout from './layouts/dashboard/dashboard'

const App = () => {
  const [newMessage, setNewMessage] = useState('')
  const [messages, setMessages] = useState([])

  useEffect(() => {
    //Only for Development with json-server (to get message History from db.json)
    messageService
      .getMessages()
      .then(messageHistory => {
        setMessages(messageHistory)
      })
  }, [])

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
      messageService
        .sendMessage(message)
        .then(returnedMessage => {
          setMessages(messages.concat(returnedMessage))
          setNewMessage('')
        })
        .catch(error =>
          console.log(error)
        )
    }
  }

  //TODO Function for sending file to backend
  const handleNewFile = (event) => {
    const file = event.target.files[0]
    const formData = new FormData()
    formData.append(
      "Sachverhalt",
      file,
      file.name
    )
    const conMsg = {
      type: "msg-static",
      message: `Möchten Sie die Datei ${file.name} hochladen?`,
      incoming: false,
      outgoing: true,
      timestamp: Date.now(),
      id: messages.length
    }
    //Only for Development with json-server (to get message History from db.json)
    messageService
    .sendMessage(conMsg)
    .then(returnedMessage => {
      setMessages(messages.concat(returnedMessage))
    })
    
    messageService.uploadFile(file)


  }

  return (
    <>
      < DashboardLayout
        messages={messages}
        sendMessage={sendMessage}
        handleNewMessage={handleNewMessage}
        newMessage={newMessage}
        handleNewFile={handleNewFile}
      />
    </>
  )
}

export default App
