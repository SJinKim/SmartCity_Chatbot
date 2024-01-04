import { Button } from '@mui/material'
import PropTypes from 'prop-types'

const DownloadButton = (props) => {
    return (
        <>
            <Button
                component='label'
                variant='contained'
                onClick={props.handleFileDownload}
                sx={{
                    bgcolor: '#3B4159',
                    color: 'white',
                    '&:hover': {
                        bgcolor: 'rgba(59, 65, 89, 0.8)' // A slightly lighter color on hover
                    }
                }}
            >
                Herunterladen
            </Button>
        </>
    )
}

DownloadButton.propTypes = {
    handleFileDownload: PropTypes.func.isRequired
}

export default DownloadButton