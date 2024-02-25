import { Button, Typography, Stack, Divider } from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import PropTypes from 'prop-types'


/**
 * react component for formatting and creating a new chat button
 * 
 * @component
 * @param {Function} handleNewTab 
 * @param {Function} handleTabDelete 
 * @param {Object} chats 
 * @returns {JSX.Element} renders the chat buttons
 */
const NewChatButton = ({ handleNewTab, handleTabDelete, chats }) => {

  // callback for event handler for creating new chat
  const newChatWindow = () => {
    const newId = chats.length > 0 ? chats[chats.length - 1].id + 1 : 1
    handleNewTab(newId)
  }

  // callback for event handler for deleting chat
  const deleteChat = (id) => {
    handleTabDelete(id)
  }

  return (
    <>
      {/** open new chat tab */}
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
        }}
      >
        <Typography>Neuer Chat</Typography>
      </Button>
      {/** for each open chat render a button with select and delet event */}
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
  handleNewTab: PropTypes.func.isRequired, // event handler for creating or opening a chat
  handleTabDelete: PropTypes.func.isRequired, // event handler for deleting a chat
  chats: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number.isRequired // chat id
  })).isRequired // list of chats that are open at the current state
}



export default NewChatButton