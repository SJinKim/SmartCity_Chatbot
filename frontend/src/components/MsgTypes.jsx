import React from "react";
import { Box, Stack, Typography } from "@mui/material";
import { useTheme } from "@mui/material/styles";

const TextMsg = ({ el }) => {
  const theme = useTheme();

  const getName = () => {
    return el.incoming ? "Nutzer" : "SmartCity Chatbot";
  };

  const getFormattedTimestamp = () => {
    const timestamp = new Date(el.timestamp);
    return `${timestamp.toLocaleDateString()} ${timestamp.toLocaleTimeString()}`;
  };

  return (
    <Box>
      <Stack
        direction="column"
        alignItems={el.incoming ? "flex-start" : "flex-end"}
        mt={0}
        mb={0} // Adjust as needed for bottom margin
        mx={1}
      >
        <Typography variant="caption" color={theme.palette.text}>
          {getName()}
        </Typography>
      </Stack>
      <Stack
        direction="row"
        justifyContent={el.incoming ? "flex-start" : "flex-end"}
      >
        <Box
          p={1.5}
          sx={{
            backgroundColor: el.incoming
              ? theme.palette.primary.light
              : theme.palette.primary.main,
            width: "max-content",
            borderRadius: "1.5",
            m: 0,
          }}
        >
          <Typography
            variant="body2"
            color={el.incoming ? theme.palette.text : "#fff"}
          >
            {el.message}
          </Typography>
        </Box>
      </Stack>
      <Stack
        direction="row"
        justifyContent={el.incoming ? "flex-start" : "flex-end"}
        mt={0}
        mb={1} // Adjust as needed for bottom margin
        mx={1}
      >
        <Typography variant="caption" color={theme.palette.text}>
          {getFormattedTimestamp()}
        </Typography>
      </Stack>
    </Box>
  );
};

export { TextMsg };
