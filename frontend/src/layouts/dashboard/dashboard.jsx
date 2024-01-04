import { Box, Stack, Grid, Button, Typography } from "@mui/material"
import Chatbox from "../../components/Chatbox"
import Prompt from '../../components/Prompt'
import Upload from '../../components/Upload'
import PropTypes from 'prop-types'
import { useTheme } from '@mui/material/styles'
import { Download } from "@mui/icons-material"
import DownloadButton from "../../components/Download"
import NewChatButton from "../../components/NewChat"
import Images from "../../../images/ui!.png"

const DashboardLayout = (props) => {

    const theme = useTheme();

    const handleAnleitungButtonClick = () => {
        const anleitungMessage = {
            type: "msg-static",
            message: "Anleitung: here is how to use the chat",
            incoming: false,
            outgoing: true,
            timestamp: Date.now(),
            id: props.messages.length
        };

        props.sendMessage(anleitungMessage);
    };

    return (
        <Box sx={{
            flexGrow: 1,
            height: '97vh', display: 'flex',
            overflow: 'hidden'
        }}>
            <Grid container spacing={0}>
                <Grid item xs={1.5}
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
                        <Stack spacing={2}  sx={{ mt: 0.5, p: 2 }}>
                            {/* Add top content here, like other buttons or list items */}
                            <NewChatButton />
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
                        <DownloadButton />
                        <Upload handleNewFile={props.handleNewFile} />

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
                <Grid item xs={10.5}>
                    <Stack
                        sx={{ height: '100vh', overflow: 'auto' }}
                    >
                        <Chatbox
                            messages={props.messages}
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
    );


}

DashboardLayout.propTypes = {
    handleNewFile: PropTypes.func.isRequired,
    messages: PropTypes.array.isRequired,
    sendMessage: PropTypes.func.isRequired,
    newMessage: PropTypes.string.isRequired,
    handleNewMessage: PropTypes.func.isRequired
}


export default DashboardLayout;
