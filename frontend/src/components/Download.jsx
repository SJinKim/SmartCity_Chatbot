import { Button } from '@mui/material'
import PropTypes from 'prop-types'

/**
 * component for rendering donwload button
 * 
 * @component
 * @param {Function} handleFileDownload event handler for managing the download
 * @returns {JSX.Element} a react component that renders the download button
 */
const DownloadButton = ({ handleFileDownload }) => {
    return (
        <Button
            component='label'
            variant='contained'
            onClick={handleFileDownload}
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
    )
}

DownloadButton.propTypes = {
    handleFileDownload: PropTypes.func.isRequired //event handler
}

export default DownloadButton