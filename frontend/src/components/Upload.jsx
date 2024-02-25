import { Button } from '@mui/material'
import PropTypes from 'prop-types'

/**
 * formats and implements the upload button
 * 
 * @component
 * @param {Function} handleNewFile event handler
 * @returns {JSX.Element} renders the upload button
 */
const UploadButton = ({ handleNewFile }) => {
    return (
        <>
            <Button
                component='label'
                variant='contained'
                sx={{
                    bgcolor: '#3B4159',
                    color: 'white',
                    '&:hover': {
                        bgcolor: 'rgba(59, 65, 89, 0.8)' // A slightly lighter color on hover
                    }
                }}

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
                    onChange={handleNewFile}
                />
            </Button>
        </>
    )
}

UploadButton.propTypes = {
    handleNewFile: PropTypes.func.isRequired
}

export default UploadButton