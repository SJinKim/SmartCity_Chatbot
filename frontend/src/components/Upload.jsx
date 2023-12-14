import { Button } from '@mui/material'

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

export default UploadButton