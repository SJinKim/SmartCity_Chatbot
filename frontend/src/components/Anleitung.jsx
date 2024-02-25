import PropTypes from 'prop-types'
import { Button } from '@mui/material'

/**
 * formats and renders Anleitungs button
 * 
 * @param {Function} handleAnleitungButtonClick the on click event handler  
 * @returns {JSX.Element} renders button
 */
const Anleitung = ({ handleAnleitungButtonClick }) => {
    return (
        <Button variant="contained" color="primary"
            onClick={handleAnleitungButtonClick} // Use the function from props
            sx={{
                bgcolor: '#3B4159',
                color: 'white',
                '&:hover': {
                    bgcolor: 'rgba(59, 65, 89, 0.8)' // A slightly lighter color on hover
                }
            }}
        >
            Anleitung
        </Button>
    )
}

Anleitung.propTypes = {
    handleAnleitungButtonClick: PropTypes.func.isRequired // event handler
}

export default Anleitung