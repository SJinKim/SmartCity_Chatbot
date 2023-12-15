import { Box, Stack, Grid } from "@mui/material"
import { Outlet } from "react-router-dom"
import Bubble from "../../components/Bubbles"
import Prompt from '../../components/Prompt'
import Button from '@mui/material/Button'


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
                        <Button variant="contained" color="primary">
                            Anleitung
                        </Button>
                    </Box>
                </Grid>
                <Grid item xs={10.5}>
                    <Stack>
                        <Box sx={{
                            position: "relative",
                            height: "80vh",
                            width: "98%",
                            backgroundColor: "white",
                            m: 2,
                            overflowY: "scroll"
                        }}>
                            <Bubble messages={props.messages} />
                        </Box>
                        <Box sx={{
                            position: "absolute",
                            bottom: "40px",
                            width: '87%',
                        }}>
                            <Prompt sendMessage={props.sendMessage} handleNewMessage={props.handleNewMessage} newMessage={props.newMessage} />
                        </Box>
                    </Stack>
                </Grid>
            </Grid>
        </Box>
    )
}


export default DashboardLayout;
