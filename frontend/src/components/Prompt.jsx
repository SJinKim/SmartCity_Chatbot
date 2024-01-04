import { Button, TextField, Box, Stack } from '@mui/material'
import PropTypes from 'prop-types'

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
            <Stack spacing={2} direction='row'>
                <TextField
                    fullWidth
                    id='prompt'
                    placeholder="Ihre Nachricht an SmartCity Chatbot..."
                    value={props.newMessage}
                    onChange={props.handleNewMessage}
                    sx={{
                        '& .MuiOutlinedInput-root': {
                          '&.Mui-focused fieldset': {
                            borderColor: '#3B4159', // Custom focus color
                          },
                        },
                      }}
                />
                <Button type='submit' variant='contained' sx={{
                    bgcolor: '#3B4159',
                    color: 'white',
                    '&:hover': {
                        bgcolor: 'rgba(59, 65, 89, 0.8)' // A slightly lighter color on hover
                    }
                }}>
                    Send
                </Button>
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