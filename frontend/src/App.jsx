import { useEffect, useState } from 'react'
import Prompt from './components/Prompt'
import messageService from './services/messages'

import DashboardLayout from './layouts/dashboard'




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
        message: newMessage,
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

  return (
    <>
     
     <DashboardLayout/>
     
   
    <Prompt sendMessage={sendMessage} handleNewMessage={handleNewMessage} newMessage={newMessage} />
     
    </>
  )
}

export default App
