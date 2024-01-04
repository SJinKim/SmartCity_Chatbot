import { Button } from '@mui/material'
import PropTypes from 'prop-types'

const DownloadButton = (props) => {
    return (
        <>
            <Button
                component='label'
                variant='contained'
                onClick={props.handleFileDownload}
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