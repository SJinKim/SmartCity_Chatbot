import { Box, Stack, Typography } from "@mui/material"
import { useTheme } from "@mui/material/styles"
import PropTypes from 'prop-types'

const TextMsg = ({ el }) => {
  const theme = useTheme();

  const getName = () => {
    return el.incoming ? "SmartCity Chatbot" : "Nutzer"
  }

  const getFormattedTimestamp = () => {
    const timestamp = new Date(el.timestamp);
    return `${timestamp.toLocaleDateString()} ${timestamp.toLocaleTimeString()}`
  }

  return (
    <Box>
      <Stack
        direction="column"
        alignItems={el.incoming ? "flex-end" : "flex-start"}
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
        justifyContent={el.incoming ? "flex-end" : "flex-start"}
      >
        <Box
          p={1.5}
          sx={{
            bgcolor: el.incoming
              ? '#DAD9DF'  //theme.palette.primary.light
              : '#F1F8CC', //theme.palette.primary.main,
            width: "max-content",
            borderRadius: "10px",
            m: 0,
          }}
        >
          <Typography
            variant="body2"
            color={ theme.palette.text} //el.incoming ? theme.palette.text :"#fff"
            style={{whiteSpace: 'pre-line'}}
          >
              {el.message}
          </Typography>
        </Box>
      </Stack>
      <Stack
        direction="row"
        justifyContent={el.incoming ? "flex-end" : "flex-start"}
        mt={0}
        mb={1} // Adjust as needed for bottom margin
        mx={1}
      >
        <Typography variant="caption" color={theme.palette.text}>
          {getFormattedTimestamp()}
        </Typography>
      </Stack>
    </Box>
  )
}

TextMsg.propTypes = {
  el: PropTypes.object.isRequired,
}

export { TextMsg };
