import { Box, CircularProgress, Stack, Typography } from '@mui/material'
import { TextMsg } from './MsgTypes'
import PropTypes from 'prop-types'
import { useEffect, useRef } from 'react'

/**
 * Component for displaying chatbubbles
 * 
 * @component
 * @param {Object} chat the chat to be displayed in the Window
 * @returns {JSX.Element} react element that renders the chat bubbles
 */
const Chatbox = ({ chat }) => {

  //Ref for automatic scrolling
  const chatbox = useRef(null);
  useEffect(() => {
    // automatic scrolling to newest bubble
    chatbox.current.scrollIntoView({ block: 'end', behavior: 'smooth' })
  }, [chat.chatHistory])

  /**
   * function for displaying if chatbot is typing
   * 
   * @returns {JSX.Element} typing indicator if user is waiting for response from server
   */
  const typingIndicator = () => {
    if (chat.isTyping === true)
      return (
        <Box sx={{
          display: 'flex',
          pr: 5,
          justifyContent: 'flex-end'
        }}>
          <CircularProgress sx={{ color: '#3B4159' }} />
        </Box>
      )
  }

  return (
    <> {/* title of the chat */}
      <Typography
        variant='h4'
        sx={{
          pt: 2,
          margin: 'auto',
          color: 'grey'
        }}>
        CHAT {chat.id}
      </Typography>
      {/* chatbox content */}
      <Box
        sx={{
          position: "relative",
          height: "80vh",
          width: "98%",
          backgroundColor: "white",
          m: 2,
          overflowY: "scroll",
          '&::-webkit-scrollbar': {
            display: 'none'  // Hide scrollbar for Chrome, Safari and Opera
          },
          scrollbarWidth: 'none', // Hide scrollbar for Firefox
          msOverflowStyle: 'none', // Hide scrollbar for IE 10+

        }}>

        {/* stack for displaying the bubbles */}
        <Stack spacing={3} ref={chatbox}>
          {chat.chatHistory.map(el => {
            return <TextMsg key={el.timestamp} el={el} />
          })}
          {/* display typing indicator */}
          {typingIndicator()}
        </Stack>
      </Box>
    </>
  )
}


Chatbox.propTypes = {
  chat: PropTypes.shape({
    id: PropTypes.number.isRequired, // chat ID
    chatHistory: PropTypes.arrayOf(PropTypes.shape({
      message: PropTypes.string.isRequired, // the message for a bubble
      incoming: PropTypes.bool.isRequired, // if message is from server or user
      timestamp: PropTypes.number.isRequired // datetime of generation
    })).isRequired, // array of text messages in json format
    isTyping: PropTypes.bool.isRequired // typing indicator
  }).isRequired,
}

export default Chatbox