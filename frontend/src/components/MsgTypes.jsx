import { Box, Stack, Typography } from "@mui/material"
import { useTheme } from "@mui/material/styles"
import PropTypes from 'prop-types'


/**
 * formats the bubble
 * 
 * @component
 * @param {Object} el chat object to be formatted
 * @returns {JSX.Element} renders formatted bubble
 */
const TextMsg = ({ el }) => {
  const theme = useTheme();

  // title of the bubble
  const getName = () => {
    return el.incoming ? "SmartCity Chatbot" : "Nutzer"
  }

  /**
   * formats datetime for the bubble
   * @returns {string} formated datetime
   */
  const getFormattedTimestamp = () => {
    const timestamp = new Date(el.timestamp);
    return `${timestamp.toLocaleDateString()} ${timestamp.toLocaleTimeString()}`
  }

  return (
    <Box>
      {/** bubble header */}
      <Stack
        direction="column"
        alignItems={el.incoming ? "flex-end" : "flex-start"} // bubble is right or left of screen
        mt={0}
        mb={0} // Adjust as needed for bottom margin
        mx={1}
      >
        <Typography variant="caption" color={theme.palette.text}>
          {getName()}
        </Typography>
      </Stack>
      {/** bubble */}
      <Stack
        direction="row"
        justifyContent={el.incoming ? "flex-end" : "flex-start"} // text right or left align in bubble
      >
        <Box
          p={1.5}
          sx={{
            bgcolor: el.incoming // background color depending on incoming or outgoing message
              ? '#DAD9DF'
              : '#F1F8CC',
            width: "max-content",
            borderRadius: "10px",
            m: 0,
          }}
        >
          {/** text message */}
          <Typography
            variant="body2"
            color={theme.palette.text} // color of text
            style={{ whiteSpace: 'pre-line' }}
          >
            {el.message}
          </Typography>
        </Box>
      </Stack>
      {/** bubble footer */}
      <Stack
        direction="row"
        justifyContent={el.incoming ? "flex-end" : "flex-start"} // alignment of datetime
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
  el: PropTypes.shape({
    message: PropTypes.string.isRequired, // the message for a bubble
    incoming: PropTypes.bool.isRequired, // if message is from server or user
    timestamp: PropTypes.number.isRequired // datetime of generation
  }).isRequired
}

export { TextMsg };
