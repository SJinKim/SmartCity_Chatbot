import { Box, CircularProgress, Stack, Typography } from '@mui/material'
import { TextMsg } from './MsgTypes'
import PropTypes from 'prop-types'
import { useEffect, useRef } from 'react'


const Chatbox = (props) => {
  const chat = props.chat

  const chatbox = useRef(null);
  useEffect(() => {
    chatbox.current.scrollIntoView({ block: 'end', behavior: 'smooth' })
  }, [chat.chatHistory])

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
    <>
      <Typography
        variant='h4'
        sx={{
          pt: 2,
          margin: 'auto',
          color: 'grey'
        }}>
        CHAT {chat.id}
      </Typography>
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

        <Stack spacing={3} ref={chatbox}>
          {chat.chatHistory.map(el => {
            return <TextMsg key={el.timestamp} el={el} />
          })}
          {typingIndicator()}
        </Stack>
      </Box>
    </>
  )
}

Chatbox.propTypes = {
  chat: PropTypes.object.isRequired,
}


export default Chatbox