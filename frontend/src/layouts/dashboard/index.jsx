import { Box, Stack } from "@mui/material";
import React from "react";
import { Outlet } from "react-router-dom";
import Bubble from "../../components/Bubbles";
import Button from '@mui/material/Button';


const DashboardLayout = () => {


  return (
    <>
      <Stack
        direction="row" alignItems={"center"} justifyContent={"space-between"}
      >
        <Box sx={
          { backgroundColor: "green", height: "100vh", width: "17%" }
        }>

          <Button variant="contained" color="primary">
            Anleitung
          </Button>


        </Box>


        <Box
          sx={{ position: "relative", height: "100vh", width: "83%", backgroundColor: "white", m: 2, overflowY: "scroll" }}
        >
          <Bubble />


        </Box>
        <Outlet />
      </Stack>
    </>
  );
};


export default DashboardLayout;
