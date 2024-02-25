
/**
 * formats the ui logo for start screen
 * 
 * @component
 * @returns {JSX.Element} react component that renders start screen
 */
const StartScreen = () => {
    return (
        <div style={{
            display: 'flex',
            alignItems: 'center', // This will align the image vertically
            justifyContent: 'center', // This will align the image horizontally
            height: '100%', // Take the full height of the grid cell
            width: '100%' // Take the full width of the grid cell
        }}>
            {/** load ui logo */}
            <img src="../../../images/ui_transparent.png" alt="Logo" style={{ maxHeight: '50vh', maxWidth: '50vh' }} />
        </div>
    )
}

export default StartScreen