import { Box, Stack } from "@mui/material"

import { Outlet } from "react-router-dom"
import Bubble from "../../components/Bubbles"
import Prompt from '../../components/Prompt'
import Button from '@mui/material/Button'


const DashboardLayout = (props) => {


  return (
    <>
      <Stack
        direction="row"
        alignItems={"center"}
        justifyContent={"space-between"}
      >
        <Box sx={{
          backgroundColor: "green",
          height: "100vh",
          width: "20%"
        }}>
          <Button variant="contained" color="primary">
            Anleitung
          </Button>
        </Box>
        <Box
          sx={{
            position: "relative",
            height: "100vh",
            width: "100%",
            

          }}
        >
          <Stack>
            <Box sx={{
              position: "relative",
              height: "80vh",
              width: "83%",
              backgroundColor: "yellow",
              m: 2,
              overflowY: "scroll"
            }}>
              <Bubble />
            </Box>
            <Box sx={{
              position: "absolute",
              bottom: "50px",
              width: '83%',
              backgroundColor: 'blue'
            }}>
              <Prompt sendMessage={props.sendMessage} handleNewMessage={props.handleNewMessage} newMessage={props.newMessage} />
            </Box>

          </Stack>
        </Box >

        <Outlet />
      </Stack >
    </>
  );
};


export default DashboardLayout;
