import Alert from '@mui/material/Alert'
import AlertTitle from '@mui/material/AlertTitle'
import { Stack, Button, Typography } from '@mui/material'

/**
 * component for displaying the Error Screen 
 * 
 * @returns {JSX.Element} react element, with ui-logo, a standard error
 *                        message and a button for reloading the react-app
 */
const ErrorScreen = () => {
    return (
        <Stack sx={{
            display: 'flex',
            alignItems: 'center', // This will align the image vertically
            justifyContent: 'center', // This will align the image horizontally
            height: '100%', // Take the full height of the grid cell
            width: '100%', // Take the full width of the grid cell}} spacing={2}>
            gap: 4
        }} spacing={2}>
            < img src="../../../images/ui_transparent.png"
                alt="Logo"
                style={{ maxHeight: '50vh', maxWidth: '50vh' }}
            />
            {/** The Alert field with a Error Message */}
            <Alert sx={{
                width: '60%'
            }}
                severity="error">
                <AlertTitle>Ups. Da ist etwas schiefgegangen</AlertTitle>
                Es tut uns leid, es gab ein Problem beim Herstellen einer Verbindung
                mit unserem Server. Bitte überprüfen Sie Ihre Netzwerkverbindung und
                versuchen Sie es erneut. Wenn das Problem weiterhin besteht, wenden
                Sie sich bitte an den Support.
            </Alert>
            {/** reload the app on click */}
            <Button
                variant="contained"
                onClick={() => window.location.reload()}
                sx={{
                    mt: 200,
                    bgcolor: '#3B4159',
                    color: 'white',
                    '&:hover': {
                        bgcolor: 'rgba(59, 65, 89, 0.8)', // A slightly lighter color on hover
                    },
                    width: '15%'
                }}
            >
                <Typography>Erneut versuchen</Typography>
            </Button>
        </Stack>

    )
}

export default ErrorScreen