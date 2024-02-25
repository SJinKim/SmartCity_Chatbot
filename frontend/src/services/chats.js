
/**
 * creates a socket connection
 * 
 * @param {number} id the chat id 
 * @returns {Promise<WebSocket>} socket on on successfull connection to server, else error
 */
const websocketConnection = (id) => {
    const socket = new WebSocket(`ws://localhost:8000/api/chat/${id}`)

    return new Promise((resolve, reject) => {
        socket.onopen = () => {
            resolve(socket)
        }
        socket.onerror = (error) => {
            reject(error)
        }
    })
}

/**
 * creates a new chat with the given id and an optional first message
 * 
 * @param {number} id chat id 
 * @param {string} message text message 
 * @param {Function} onMessageCallback callback function to handler for Message event
 * @param {Function} onErrorCallback callback function to handler for Error event
 * @returns {Object} a chat object if socket connection was successfull
 */
const createNewChat = async (id, message, onMessageCallback, onErrorCallback) => {
    try {
        const socket = await websocketConnection(id)

        socket.onmessage = (event) => {
            const msgData = JSON.parse(event.data)
            onMessageCallback(msgData)
        }

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
        return newChat
    } catch (error) {
        onErrorCallback()
        return
    }
}


export default createNewChat