
const createSocket = () => {

    // TODO change code for socket variable, that the url for the socket is not hardcoded
    //e.g.
    //const socket = new WebSocket(((window.location.protocol === "https:") 
    //  ? "wss://" : "ws://") + window.location.host + "/api/chat")
    return new WebSocket("ws://localhost:8000/api/chat")

}

const onMessage = (socket, setMessages, setNewMessage, messages) => {
    socket.onmessage = (event) => {
        const message = {
            type: "msg",
            message: event.data,
            incoming: false,
            outgoing: true,
            timestamp: Date.now(),
            id: messages.length
        }
        setMessages(messages.concat(message))
        setNewMessage('')
    }
}

export default { createSocket, onMessage }
