import { useEffect, useState } from 'react'
import messageService from './services/messages'
import DashboardLayout from './layouts/dashboard/dashboard'

const App = () => {
  const [newMessage, setNewMessage] = useState('')
  const [activeChat, setActiveChat] = useState(0)
  const [chats, setChats] = useState([])
  const [incomingMessage, setIncomingMessage] = useState()

  useEffect(() => {
    if (incomingMessage !== undefined) {
      const id = Number(incomingMessage.client_id)
      const message = {
        message: incomingMessage.message,
        incoming: true,
        timestamp: Date.now()
      }
      const chat = chats.find(chat => chat.id === id)
      chat.isTyping = false
      chat.chatHistory = chat.chatHistory.concat(message)
      setChats([...chats])
    }
  }, [incomingMessage])


  const createNewChat = async (id, message) => {
    const socket = await new WebSocket(`ws://localhost:8000/api/chat/${id}`)
    const newChat = {
      id: id,
      socket: socket,
      chatHistory: [],
      isTyping: false
    }

    if (message !== undefined) {
      newChat.chatHistory = newChat.chatHistory.concat({
        message: message,
        incoming: true,
        timestamp: Date.now()
      })
    }

    socket.onmessage = (event) => {
      const messageData = JSON.parse(event.data)
      setIncomingMessage(messageData)
    }
    return newChat
  }

  const handleNewTab = async (id) => {
    if (id > chats.length) {
      const message = 'Hallo, wie kann ich Ihnen helfen?'
      const newChat = await createNewChat(id, message)
      setChats(chats.concat(newChat))
    }
    setActiveChat(id)
  }

  const handleTabDelete = (id) => {
    const chatToClose = chats.find(chat => chat.id === id)
    chatToClose.socket.send("close")
    if (chats.length > 1) {
      const tmpChats = chats.filter(chat => chat.id !== id)
      setChats(tmpChats)
      setActiveChat(Math.max(...tmpChats.map(chat => chat.id)))
    } else {
      setChats([])
      setActiveChat(0)
    }
  }

  const handleNewMessage = (event) => {
    setNewMessage(event.target.value)
  }

  const sendMessage = async (event) => {
    event.preventDefault()
    if (newMessage !== '') {
      const outgoingMesssage = {
        message: newMessage,
        incoming: false,
        timestamp: Date.now()
      }
      if (activeChat === 0) {
        const newChat = await createNewChat(1)
        newChat.chatHistory = newChat.chatHistory.concat(outgoingMesssage)
        newChat.isTyping = true
        setChats(chats.concat(newChat))
        setActiveChat(1)
        newChat.socket.onopen = () => {
          newChat.socket.send(outgoingMesssage.message)
        }
      } else {
        const chat = chats.find(chat => chat.id === activeChat)
        chat.chatHistory = chat.chatHistory.concat(outgoingMesssage)
        chat.isTyping = true
        setChats([...chats])
        const socket = chats.find(chat => chat.id === activeChat).socket
        await socket.send(outgoingMesssage.message)
      }
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
    const message = {
      message: response.message,
        incoming: true,
        timestamp: Date.now()
    }
    if(activeChat === 0) {
        const newChat = await createNewChat(1, message)
        setChats(chats.concat(newChat))
        setActiveChat(1)
    }
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
  }

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

  return (
    <>
      < DashboardLayout
        chats={chats}
        activeChat={activeChat}
        sendMessage={sendMessage}
        handleNewMessage={handleNewMessage}
        newMessage={newMessage}
        handleNewFile={handleNewFile}
        handleFileDownload={handleFileDownload}
        handleNewTab={handleNewTab}
        handleTabDelete={handleTabDelete}
        handleAnleitungButtonClick={handleAnleitungButtonClick} // Pass the function as a prop
      />
    </>
  )
}

export default App
