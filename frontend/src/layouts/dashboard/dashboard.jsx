import { Box, Stack, Grid } from "@mui/material"
import Chatbox from "../../components/Chatbox"
import Prompt from '../../components/Prompt'
import Upload from '../../components/Upload'
import Download from "../../components/Download"
import Anleitung from "../../components/Anleitung"
import PropTypes from 'prop-types'
import { useTheme } from '@mui/material/styles'
import NewChatButton from "../../components/NewChat"
import StartScreen from "../../components/StartScreen"

/**
 * component for formatting the layout of the ui
 * 
 * @component
 * @param {*} props 
 * @returns {JSX.Element} the rendert 
 */
function DashboardLayout(props) {

    const theme = useTheme()

    return (
        <Box sx={{
            margin: 0,
            flexGrow: 1,
            height: '100vh', display: 'flex',
            overflow: 'hidden'
        }}>
            <Grid container spacing={0}>
                {/** This is the Menu Container */}
                <Grid item xs={1.8}
                    sx={{
                        display: 'flex',
                        flexDirection: 'column', // Stack children vertically
                        justifyContent: 'space-between', // Push footer to the bottom
                        backgroundColor: "#BED702",
                        height: "100%", // Take up full height of the parent
                    }}
                >
                    <Box sx={{
                        backgroundColor: '#3B4159',
                        padding: theme.spacing(0),
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                    }}>
                        {/* the logo comes here! */}
                        <img src="../../../images/logo-ui.png" alt="Logo" style={{ maxHeight: '100%', maxWidth: '100%' }} />


                    </Box>
                    {/* Top content */}
                    <Box sx={{
                        backgroundColor: "#BED702",
                        height: "98vh",
                    }}>
                        <Stack spacing={2} sx={{ mt: 0.5, p: 2 }}>
                            {/* Add top content here, like other buttons or list items */}
                            <NewChatButton
                                handleNewTab={props.handleNewTab}
                                handleTabDelete={props.handleTabDelete}
                                chats={props.chats}
                            />
                        </Stack>
                    </Box>
                    {/* Spacer to push the bottom content down */}
                    <Box sx={{
                        flexGrow: 1,
                        backgroundColor: "#BED702",
                        height: "98vh",
                    }} />

                    {/* This Stack will be pushed to the bottom */}
                    <Stack spacing={2} sx={{ p: 2, pb: 4 }}>
                        <Upload handleNewFile={props.handleNewFile} />
                        <Download handleFileDownload={props.handleFileDownload} />
                        <Anleitung handleAnleitungButtonClick={props.handleAnleitungButtonClick} />
                    </Stack>
                </Grid>
                {/** Chat UI */}
                <Grid item xs={10.2}>
                    <Stack sx={{ height: '92vh' }}>
                        {props.activeChat !== 0 ?
                            <Chatbox chat={props.chats.find(chat => chat.id === props.activeChat)} />
                            : <StartScreen />
                        }
                        <Prompt
                            sendMessage={props.sendMessage}
                            handleNewMessage={props.handleNewMessage}
                            newMessage={props.newMessage}
                        />
                    </Stack>
                </Grid>
            </Grid>
        </Box>
    )
}

DashboardLayout.propTypes = {
    handleNewFile: PropTypes.func.isRequired,
    sendMessage: PropTypes.func.isRequired,
    newMessage: PropTypes.string.isRequired,
    handleNewMessage: PropTypes.func.isRequired,
    handleFileDownload: PropTypes.func.isRequired,
    handleNewTab: PropTypes.func.isRequired,
    handleTabDelete: PropTypes.func.isRequired,
    handleAnleitungButtonClick: PropTypes.func.isRequired,
    chats: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.number.isRequired, // chat ID
            chatHistory: PropTypes.arrayOf(PropTypes.shape({
                message: PropTypes.string.isRequired, // the message for a bubble
                incoming: PropTypes.bool.isRequired, // if message is from server or user
                timestamp: PropTypes.number.isRequired // datetime of generation
            })).isRequired, // array of text messages in json format
            isTyping: PropTypes.bool.isRequired // typing indicator
        }).isRequired,
    ).isRequired,
    activeChat: PropTypes.number.isRequired
}


export default DashboardLayout;
