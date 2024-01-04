import { Button } from '@mui/material'
import PropTypes from 'prop-types'
import { ThemeConsumer } from 'styled-components'

const DownloadButton = (props) => {
    return (
        <>
            <Button
                
                variant='contained'
                href={props.fileUrl} // Link to the file you want to download
                download={props.fileName} // Suggested filename to save as
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



export default DownloadButton