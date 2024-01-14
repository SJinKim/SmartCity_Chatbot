import { Button, Typography, Stack, Divider } from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import PropTypes from 'prop-types'
import { useState } from 'react'

const NewChatButton = ({ handleNewTab, handleTabDelete }) => {
  const [chatTabs, setChatTabs] = useState([{ id: 1 }])

  const newChatWindow = () => {
    const newId = chatTabs.length > 0 ? chatTabs[chatTabs.length - 1].id + 1 : 1
    setChatTabs(chatTabs.concat({ id: newId }))
    handleNewTab(newId)
  }

  const deleteChat = (id) => {
    setChatTabs(chatTabs.filter(tab => {
      if (tab.id !== id)
        return tab
    }))
    handleTabDelete(id)
  }

  return (
    <>
      <Button
        variant="contained"
        onClick={newChatWindow}
        sx={{
          bgcolor: '#3B4159',
          color: 'white',
          '&:hover': {
            bgcolor: 'rgba(59, 65, 89, 0.8)', // A slightly lighter color on hover
          },
          width: '100%'
        }}// Make the button full width
      >
        <Typography>Neuer Chat</Typography>
      </Button>
      {chatTabs.map((chat) => {
        return (
          <div key={chat.id}>
            <Button
              variant="contained"
              sx={{
                bgcolor: '#3B4159',
                color: 'white',
                '&:hover': {
                  bgcolor: 'rgba(59, 65, 89, 0.8)', // A slightly lighter color on hover
                },
                width: '100%'
              }}// Make the button full width
            >
              <Stack direction='row' spacing={2} divider={<Divider orientation="vertical" flexItem />}>
                <Typography onClick={() => handleNewTab(chat.id)}>Chat {chat.id}</Typography>
                <DeleteIcon onClick={() => deleteChat(chat.id)} />
              </Stack>
            </Button>

          </div>
        )
      })}

    </>
  )
}

NewChatButton.propTypes = {
  handleNewTab: PropTypes.func.isRequired,
  handleTabDelete: PropTypes.func.isRequired
}



export default NewChatButton