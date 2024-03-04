import { useEffect, useState } from 'react'
import messageService from './services/messages'
import createNewChat from './services/chats'
import DashboardLayout from './layouts/dashboard/dashboard'
import ErrorScreen from './components/ErrorScreen'


/**
 * main component of the application
 * @component
 * @returns {JSX.Element} rendert application component
 */
const App = () => {
  const [newMessage, setNewMessage] = useState('')
  const [activeChat, setActiveChat] = useState(0)
  const [chats, setChats] = useState([])
  const [incomingMessage, setIncomingMessage] = useState()
  const [websocketError, setWebsocketError] = useState(false)

  /**
   * effect for handling new incoming message
   */
  useEffect(() => {
    if (incomingMessage !== undefined) {
      const id = Number(incomingMessage.client_id)
      const message = {
        message: incomingMessage.message,
        incoming: true,
        timestamp: Date.now()
      }
      // find the correct chat for incoming message via id
      const chat = chats.find(chat => chat.id === id)
      chat.isTyping = false
      chat.chatHistory = chat.chatHistory.concat(message)
      setChats([...chats])
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [incomingMessage])

  /**
   * handler for creating and opening a new chat
   * @param {number} id the chat id 
   */
  const handleNewTab = async (id) => {
    if (id > chats.length) {
      const message = 'Hallo, wie kann ich Ihnen helfen?'
      const newChat =
        await createNewChat(
          id,
          message,
          (msgData) => setIncomingMessage(msgData),
          () => setWebsocketError(true)
        )
      setChats(chats.concat(newChat))
    }
    setActiveChat(id)
  }

  /**
   * handler for deleting a chat
   * @param {number} id chat id to be deleted
   */
  const handleTabDelete = (id) => {
    const chatToClose = chats.find(chat => chat.id === id)
    if (chatToClose.socket.readyState === WebSocket.OPEN)
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

  // safe the messsage from the ui prompt to the state variable
  const handleNewMessage = (event) => {
    setNewMessage(event.target.value)
  }

  /**
   * handler for sending a new message to server
   * @param {Object} event 
   */
  const sendMessage = async (event) => {
    event.preventDefault()
    // do nothing if no message was typed in prompt
    if (newMessage !== '') {
      let socket = null
      const outgoingMesssage = {
        message: newMessage,
        incoming: false,
        timestamp: Date.now()
      }
      // create new chat if no chat is active
      if (activeChat === 0) {
        const newChat =
          await createNewChat(
            1,
            undefined,
            (msgData) => setIncomingMessage(msgData),
            () => setWebsocketError(true)
          )
        if (newChat !== undefined) {
          newChat.chatHistory = newChat.chatHistory.concat(outgoingMesssage)
          newChat.isTyping = true
          setChats([newChat])
          setActiveChat(1)
          socket = newChat.socket
        }
      }
      // find the chat for sending the message to the right socket connection
      // and append the message to the chat history
      else {
        const chat = chats.find(chat => chat.id === activeChat)
        chat.chatHistory = chat.chatHistory.concat(outgoingMesssage)
        chat.isTyping = true
        setChats([...chats])
        socket = chats.find(chat => chat.id === activeChat).socket
      }
      // send the message via socket, only if socket is ready and exists
      if (socket !== null && socket.readyState === WebSocket.OPEN) {
        socket.send(outgoingMesssage.message)
      }
      // set error state for rerendering to error screen, if socket not open
      else {
        setWebsocketError(true)
      }
      // delete message from the prompt in the ui
      setNewMessage('')
    }
  }

  /**
   * handler for uploading the selected text file to the server 
   * @param {Object} event 
   */
  const handleNewFile = async (event) => {
    const file = event.target.files[0]
    let formData = new FormData()
    formData.append(
      "sachverhalt",
      file,
      file.name
    )
    // try to send the constructed html form data message
    try {
      const response = await messageService.uploadFile(formData)
      // create new chat if no chat is active
      if (activeChat === 0) {
        const newChat =
          await createNewChat(
            1,
            response.message,
            (msgData) => setIncomingMessage(msgData),
            () => setWebsocketError(true)
          )
        newChat.isTyping = true
        setChats([newChat])
        setActiveChat(1)
      }
      // find active chat and append the response message from file upload 
      else {
        const message = {
          message: response.message,
          incoming: true,
          timestamp: Date.now()
        }
        const chat = chats.find(chat => chat.id === activeChat)
        chat.chatHistory = chat.chatHistory.concat(message)
        chat.isTyping = true
        setChats([...chats])
      }
    }
    // if upload fails set error state for rerendering to error screen 
    catch (error) {
      setWebsocketError(true)
    }
  }

  /**
   * handler for creating the message that explains the chatbot
   */
  const handleAnleitungButtonClick = async () => {
    const anleitungMessage = {
      message: `In diesem Chat können Sie Fragen zu Ihrem Bescheid stellen.\
                Der Chat wird Ihnen den entsprechenden Bescheid zusenden.\
                Sie haben die Möglichkeit, den Bescheid durch Klicken auf den \
                Button 'Herunterladen' herunterzuladen. Zusätzlich können \
                Sie eine Datei hochladen, indem Sie auf den Button 'Hochladen' \
                klicken. Der Chat verwendet diese Datei, um den entsprechenden \
                Bescheid zu finden. Um mehrere Chats zu öffnen, klicken Sie auf \
                den Button 'Neuer Chat'.`,
      incoming: true,
      timestamp: Date.now(),

    }
    // create new chat if no active chat exists
    if (activeChat === 0) {
      const newChat =
        await createNewChat(
          1,
          anleitungMessage.message,
          (msgData) => setIncomingMessage(msgData),
          () => setWebsocketError(true)
        )
      if (newChat !== undefined) {
        newChat.isTyping = false
        setChats([newChat])
        setActiveChat(1)
      }
    }
    // find active chat and append the message to chat history 
    else {
      const chat = chats.find(chat => chat.id === activeChat)
      chat.chatHistory = chat.chatHistory.concat(anleitungMessage)
      chat.isTyping = false
      setChats([...chats])
    }
  }

  /**
   *  downloads the bescheid from backend, if bescheid exists
   */
  const handleFileDownload = async (event) => {
    event.preventDefault()
    try {
      const response = await messageService.downloadFile()
      const file = new Blob(
        [response],
        { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
      const fileURL = URL.createObjectURL(file)
      const link = document.createElement('a');
      link.href = fileURL;
      link.setAttribute('download', 'bescheid.doc');
      document.body.appendChild(link);
      // Trigger the download
      link.click();
      // Clean up resources
      window.URL.revokeObjectURL(fileURL);
      document.body.removeChild(link);
    } catch (exc) {
      const excMsg = {
        message: 'Es ist noch keine Datei zum Download verfügbar',
        incoming: true,
        timestamp: Date.now(),
      }
      if (activeChat === 0) {
        const newChat =
          await createNewChat(
            1,
            excMsg.message,
            (msgData) => setIncomingMessage(msgData),
            () => setWebsocketError(true)
          )
        if (newChat !== undefined) {
          newChat.isTyping = false
          setChats([newChat])
          setActiveChat(1)
        }
      } else {
        const chat = chats.find(chat => chat.id === activeChat)
        chat.chatHistory = chat.chatHistory.concat(excMsg)
        chat.isTyping = false
        setChats([...chats])
      }
    }
  }

  return (
    <>
      {/* Display error screen if connection to server fails, else the chat ui */}
      {websocketError ?
        <ErrorScreen />
        :
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
          handleAnleitungButtonClick={handleAnleitungButtonClick}
        />
      }
    </>
  )
}

export default App
