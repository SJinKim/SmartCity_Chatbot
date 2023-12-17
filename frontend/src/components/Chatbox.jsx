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
                overflowY: "scroll"
            }}>
            <Stack spacing={3} ref={chatbox}>
                {
                    props.messages.map(el => {
                        switch (el.type) {
                            case "msg":
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
                                return <TextMsg key={el.id} el={el} />
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