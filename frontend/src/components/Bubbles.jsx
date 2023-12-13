import { Button, TextField, Box, Stack } from '@mui/material'
import React from 'react'
import { Chat_History } from '../services/ChatHistory'
import { TextMsg } from './MsgTypes'

const Bubble = () => {
    return(
        <Box> 
        <Stack spacing={3}>
            {
                Chat_History.map((el) => {
                    
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
                                   return  <TextMsg  el={el}/>
                                    
                            }
                                break;
                    
                        default:
                            return <></>;
                    } 
                })
            }
        </Stack>
        </Box>
    )

}

export default Bubble