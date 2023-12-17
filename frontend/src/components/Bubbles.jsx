import { Box, Stack } from '@mui/material'
import { Chat_History } from '../services/ChatHistory'
import { TextMsg } from './MsgTypes'


const Bubble = (props) => {
    return(
        <Box>
        <Stack spacing={3}>
            {
                //Chat_History.map((el) => {
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
                                   return  <TextMsg key={el.id} el={el}/>
                                   
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