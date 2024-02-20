import { Button, Typography, Stack, Divider } from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import PropTypes from 'prop-types'

const NewChatButton = ({ handleNewTab, handleTabDelete, chats }) => {

  const newChatWindow = () => {
    const newId = chats.length > 0 ? chats[chats.length - 1].id + 1 : 1
    handleNewTab(newId)
  }

  const deleteChat = (id) => {
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
      {chats.map((chat) => {
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
  handleTabDelete: PropTypes.func.isRequired,
  chats: PropTypes.array.isRequired
}



export default NewChatButton