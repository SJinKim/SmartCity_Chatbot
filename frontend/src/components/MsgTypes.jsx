import React from "react";
import { Box, Divider, Stack, Typography } from '@mui/material';
import { useTheme } from '@mui/material/styles';


const TextMsg = ({el}) => {
    const theme = useTheme();

    return(
        <Stack direction="row" justifyContent={el.incoming ? "start" : "end"}>
            
            <Box p = {1.5} 
            sx={{
                backgroundColor: el.incoming ? theme.palette.primary.light : theme.palette.primary.main,
                bottom: '50px',
                left: '50%',
                width: 'max-content',
                borderRadius: '1.5',
                
            }}
            >
                <Typography variant= "body2"
                    color={el.incoming ? theme.palette.text : "#fff"}
                >
                    {el.message}
                </Typography>
            </Box>

       </Stack>
    )
}

export { TextMsg };