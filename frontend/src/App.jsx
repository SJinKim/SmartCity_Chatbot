import { useEffect, useState } from 'react'
import messageService from './services/messages'
import DashboardLayout from './layouts/dashboard/dashboard'

const socket = new WebSocket("ws://localhost:8000/api/chat")

const App = () => {
  const [newMessage, setNewMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [chatHistory, setChatHistory] = useState([])
  const [chatId, setChatId] = useState(1)
  const [openChats, setOpenChats] = useState([1])
  const [isTyping, setIsTyping] = useState(false)

  useEffect(() => {
    setChatHistory(messages.filter(msg => {
      if (msg.chatId === chatId)
        return msg
    }))
  }, [chatId, messages])

  socket.onmessage = (event) => {
    const message = {
      type: "msg",
      message: event.data,
      incoming: false,
      outgoing: true,
      timestamp: Date.now(),
      id: messages.length,
      chatId: chatId
    }
    setMessages(messages.concat(message))
    setNewMessage('')
    setIsTyping(false)
  }

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
        id: messages.length,
        chatId: chatId
      }
      socket.send(JSON.stringify(message.message))
      setMessages(messages.concat(message))
      setNewMessage('')
      setIsTyping(true)
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
      id: messages.length,
      chatId: chatId
    }
    setMessages(messages.concat(conMsg))
    setIsTyping(true)
  }

  const handleAnleitungButtonClick = () => {
    const anleitungMessage = {
      type: "msg-static",
      message: "In diesem Chat können Sie Fragen zu Ihrem Bescheid stellen.\nDer Chat wird Ihnen den entsprechenden Bescheid zusenden. Sie haben die Möglichkeit, den Bescheid durch Klicken auf den Button 'Herunterladen' herunterzuladen. Zusätzlich können Sie eine Datei hochladen, indem Sie auf den Button 'Hochladen' klicken. Der Chat verwendet diese Datei, um den entsprechenden Bescheid zu finden.Um mehrere Chats zu öffnen, klicken Sie auf den Button 'Neuer Chat'.",
        incoming: false,
      outgoing: true,
      timestamp: Date.now(),
      id: messages.length,
      chatId: chatId
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
        id: messages.length,
        chatId: chatId
      }
      setMessages(messages.concat(conMsg))
    }
  }

  const handleNewTab = (id) => {
    setChatId(id)
    setOpenChats(openChats.concat(id))
  }

  // TODO
  const handleTabDelete = (id) => {
    setMessages(messages.filter(msg => {
      if (msg.chatId !== id)
        return msg
    }))
    const chats = openChats.filter(chat => {
      if (chat !== id)
        return chat
    })
    setOpenChats(chats)
    setChatId(chats.sort((a, b) => { a > b ? -1 : 1 })[chats.length - 1])
  }

  //TODO Wenn alle Chats Zu -> Start Screen UI Logo? -> Websocket close()
  //TODO Neues Socket für jedes Chat Tab?
  return (
    <>
      < DashboardLayout
        messages={chatHistory}
        sendMessage={sendMessage}
        handleNewMessage={handleNewMessage}
        newMessage={newMessage}
        handleNewFile={handleNewFile}
        handleFileDownload={handleFileDownload}
        handleNewTab={handleNewTab}
        handleTabDelete={handleTabDelete}
        chatId={chatId}
        isTyping={isTyping}
        handleAnleitungButtonClick={handleAnleitungButtonClick} // Pass the function as a prop
      />
    </>
  )
}

export default App
