import { Box, Stack, Grid, Button, Typography } from "@mui/material"
import Chatbox from "../../components/Chatbox"
import Prompt from '../../components/Prompt'
import Upload from '../../components/Upload'
import Download from "../../components/Download"
import PropTypes from 'prop-types'
import { useTheme } from '@mui/material/styles'
import NewChatButton from "../../components/NewChat"
//import Images from "../../../images/ui!.png"

const DashboardLayout = (props) => {

    const theme = useTheme()

    const handleAnleitungButtonClick = () => {
        const anleitungMessage = {
            type: "msg-static",
            message: "Anleitung: here is how to use the chat",
            incoming: false,
            outgoing: true,
            timestamp: Date.now(),
            id: props.messages.length
        }

        props.sendMessage(anleitungMessage)
    }

    return (
        <Box sx={{
            margin: 0,
            flexGrow: 1,
            height: '100vh', display: 'flex',
            overflow: 'hidden'
        }}>
            <Grid container spacing={0}>
                {/** This is the Menu Container -> Refactor in new Dashboard Component? */}
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
                        <img src="../../../images/ui!.png" alt="Logo" style={{ maxHeight: '40%', maxWidth: '40%' }} />
                        <Typography
                            sx={{
                                color: 'white',
                                marginLeft: theme.spacing(1), // Add some spacing between the logo and text
                                fontSize: '0.875rem', // Adjust font size as needed
                                whiteSpace: 'nowrap' // Prevent wrapping to a new line
                            }}>
                            urban software institute
                        </Typography>
                    </Box>
                    {/* Top content */}
                    <Box sx={{
                        // flexGrow: 1,
                        backgroundColor: "#BED702",
                        height: "98vh",
                    }}>
                        <Stack spacing={2} sx={{ mt: 0.5, p: 2 }}>
                            {/* Add top content here, like other buttons or list items */}
                            <NewChatButton
                                handleNewTab={props.handleNewTab}
                                handleTabDelete={props.handleTabDelete}
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
                        <Button variant="contained" color="primary"
                            onClick={handleAnleitungButtonClick}
                            sx={{
                                bgcolor: '#3B4159',
                                color: 'white',
                                '&:hover': {
                                    bgcolor: 'rgba(59, 65, 89, 0.8)' // A slightly lighter color on hover
                                }
                            }}
                        >
                            Anleitung
                        </Button>


                    </Stack>
                </Grid>
                <Grid item xs={10.2}>
                    <Stack
                        sx={{ height: '92vh' }}
                    >
                        <Chatbox
                            messages={props.messages}
                            chatId={props.chatId}
                            isTyping={props.isTyping}
                        />
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
    messages: PropTypes.array.isRequired,
    sendMessage: PropTypes.func.isRequired,
    newMessage: PropTypes.string.isRequired,
    handleNewMessage: PropTypes.func.isRequired,
    handleFileDownload: PropTypes.func.isRequired,
    handleNewTab: PropTypes.func.isRequired,
    handleTabDelete: PropTypes.func.isRequired,
    chatId: PropTypes.number,
    isTyping: PropTypes.bool.isRequired
}


export default DashboardLayout;
