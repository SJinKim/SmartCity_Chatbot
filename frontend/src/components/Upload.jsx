import { Button } from '@mui/material'
import PropTypes from 'prop-types'

const UploadButton = (props) => {
    return (
        <>
            <Button
                component='label'
                variant='contained'
            >
                Hochladen
                <input
                    hidden
                    id='upload-file'
                    accept='
                    .txt,
                    .pdf,
                    .doc,
                    .docx,
                    .xml'
                    type='file'
                    onChange={props.handleNewFile}
                />
            </Button>
        </>
    )
}

UploadButton.propTypes = {
    handleNewFile: PropTypes.func.isRequired
}

export default UploadButton