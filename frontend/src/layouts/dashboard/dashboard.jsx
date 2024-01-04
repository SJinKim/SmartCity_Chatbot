import { Box, Stack, Grid, Button } from "@mui/material"
//import { Outlet } from "react-router-dom"
import Chatbox from "../../components/Chatbox"
import Prompt from '../../components/Prompt'
import Upload from '../../components/Upload'
import Download from "../../components/Download"
import PropTypes from 'prop-types'

const DashboardLayout = (props) => {

    return (
        <Box sx={{
            flexGrow: 1,
        }}>
            <Grid container spacing={0}>
                <Grid item xs={1.5}>
                    <Box sx={{
                        backgroundColor: "green",
                        height: "98vh",
                    }}>
                        <Stack spacing={2}>
                            <Button variant="contained" color="primary">
                                Anleitung
                            </Button>

                            <Upload handleNewFile={props.handleNewFile} />
                            <Download handleFileDownload={props.handleFileDownload} />
                        </Stack>
                    </Box>
                </Grid>
                <Grid item xs={10.5}>
                    <Stack>
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
    )
}

DashboardLayout.propTypes = {
    handleNewFile: PropTypes.func.isRequired,
    messages: PropTypes.array.isRequired,
    sendMessage: PropTypes.func.isRequired,
    newMessage: PropTypes.string.isRequired,
    handleNewMessage: PropTypes.func.isRequired,
    handleFileDownload: PropTypes.func.isRequired
}


export default DashboardLayout;
