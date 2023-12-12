import { Button, TextField, Box, Stack } from '@mui/material'


const Prompt = (props) => {

    return (

        <Box
            component='form'
            onSubmit={props.sendMessage}
            sx={{
                position: 'absolute',
                bottom: '50px',
                left: '50%',
                width: '90%',
                transform: 'translate(-50%, 50%)'
            }}
        >
            <Stack spacing={2} direction='row'>
                <TextField
                    fullWidth
                    id='prompt'
                    label='prompt'
                    value={props.newMessage}
                    onChange={props.handleNewMessage}
                />
                <Button type='submit' variant='contained'>Send</Button>
            </Stack>
        </Box>

    )
}

export default Prompt