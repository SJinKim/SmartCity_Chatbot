import { TextField, Box, Stack, InputAdornment } from '@mui/material'
import SendIcon from '@mui/icons-material/Send';
import PropTypes from 'prop-types'

/**
 * formats and creates prompt for chat app
 * 
 * @component
 * @param {Object} props 
 * @returns {JSX.Element} renders prompt
 */
const Prompt = (props) => {
    return (
        <Box
            component='form'
            onSubmit={props.sendMessage}
            sx={{
                position: 'relative',
                left: '50%',
                width: '90%',
                transform: 'translate(-50%, 50%)',
            }}
        >   
            {/** the prompt */}
            <Stack spacing={2} direction='row'>
                <TextField
                    fullWidth
                    id='prompt'
                    placeholder="Ihre Nachricht an Smart City Chatbot..."
                    value={props.newMessage}
                    onChange={props.handleNewMessage}
                    autoComplete='off'
                    sx={{
                        '& .MuiOutlinedInput-root': {
                            '&.Mui-focused fieldset': {
                                borderColor: '#3B4159', // Custom focus color
                            },
                            borderRadius: '25px'
                        },
                    }}
                    InputProps={{
                        endAdornment:
                            <InputAdornment position="end">
                                <SendIcon position='end' />
                            </InputAdornment>,
                    }}
                />
            </Stack>
        </Box>
    )
}

Prompt.propTypes = {
    sendMessage: PropTypes.func.isRequired,
    newMessage: PropTypes.string.isRequired,
    handleNewMessage: PropTypes.func.isRequired
}

export default Prompt