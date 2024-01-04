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
                    label='prompt'
                    value={props.newMessage}
                    onChange={props.handleNewMessage}
                    autoComplete='off'
                />
                <Button type='submit' variant='contained'>
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