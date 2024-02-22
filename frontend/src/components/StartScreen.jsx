

const StartScreen = () => {
    return (
        //<h1>Hello there!</h1>
        <div style={{
            display: 'flex',
            alignItems: 'center', // This will align the image vertically
            justifyContent: 'center', // This will align the image horizontally
            height: '100%', // Take the full height of the grid cell
            width: '100%' // Take the full width of the grid cell
        }}>

        <img src="../../../images/ui_transparent.png" alt="Logo" style={{ maxHeight: '50vh', maxWidth: '50vh' }} />
        </div>
    )
}

export default StartScreen