import { Grid } from '@mui/material'

import { useEffect, useState } from 'react'
import Prompt from './components/Prompt'
import UploadButton from './components/Upload'
import messageService from './services/messages'

import DashboardLayout from './layouts/dashboard/index2'




const App = () => {
  const [newMessage, setNewMessage] = useState('')
  const [messages, setMessages] = useState([])

  //Only for Development with json-server (to get message History in db.json)
  useEffect(() => {
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
        incoming: false,
        outgoing: true,
        timestamp: Date.now(),
        id: messages.length + 1
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
    console.log(file.name);
    //Ask in Prompt for Confirmation with Message-Bubble and Button
    messageService.uploadFile(formData)
  }

  return (
    <>

      < DashboardLayout
        messages={messages}
        sendMessage={sendMessage}
        handleNewMessage={handleNewMessage}
        newMessage={newMessage}
      />



    </>
  )
}

export default App
