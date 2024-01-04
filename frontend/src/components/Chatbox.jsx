import { Box, Stack } from '@mui/material'
import { TextMsg } from './MsgTypes'
import PropTypes from 'prop-types'
import { useEffect, useRef } from 'react'


const Chatbox = (props) => {
  const chatbox = useRef(null);
  useEffect(() => {
    chatbox.current.scrollIntoView({ block: 'end', behavior: 'smooth' })
  }, [props.messages])
  return (
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
      <Stack spacing={3} ref={chatbox} >
        {
          props.messages.map(el => {
            switch (el.type) {
              case "msg":
                //TODO: Clean up
                switch (el.subtype) {
                  case "doc":
                    //doc msg
                    break;
                  case "reply":
                    //reply msg
                    break;
                  default:
                    // text msg
                    return <TextMsg key={el.id} el={el} />
                }
                break;
              case "msg-static":
                // Instructional message
                return (
                  <Box
                    key={el.id}
                    sx={{
                      textAlign: el.incoming ? "left" : "right",
                      mb: 1,
                    }}
                  >
                    <Typography
                      variant="caption"
                      color={el.incoming ? "textSecondary" : "primary"}
                    >
                      {el.incoming ? "Nutzer" : "SmartCity Chatbot"}
                    </Typography>
                    <Box
                      p={1.5}
                      sx={{
                        backgroundColor: el.incoming
                          ? "grey.300"
                          : "primary.main",
                        width: "max-content",
                        borderRadius: 1.5,
                        m: 0,
                      }}
                    >
                      <Typography
                        variant="body2"
                        color={el.incoming ? "textPrimary" : "#fff"}
                      >
                        {el.message}
                      </Typography>
                    </Box>
                  </Box>
                );
              default:
                return <></>;
            }
          })
        }
      </Stack>
    </Box>
  )
}

Chatbox.propTypes = {
  messages: PropTypes.array.isRequired
}


export default Chatbox