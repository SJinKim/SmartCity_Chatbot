import { Button } from '@mui/material'
import PropTypes from 'prop-types'
import { ThemeConsumer } from 'styled-components'

const NewChatButton = (handleClick) => {
    return (
        <>
            <Button
            variant="contained"
            onClick={handleClick}
            sx={{
              bgcolor: '#3B4159',
              color: 'white',
              '&:hover': {
                bgcolor: 'rgba(59, 65, 89, 0.8)', // A slightly lighter color on hover
              },
              width: '100%' }}// Make the button full width
                
              

            >
                Neue Chat
               
            </Button>
        </>
    )
}



export default NewChatButton