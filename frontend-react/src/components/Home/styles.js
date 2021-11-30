
const styles = theme => ({
    root: {
        flexGrow: 1,
        minHeight: "100vh"
    },
    grow: {
        flexGrow: 1,
    },
    main: {

    },
    container: {
        backgroundColor: "#ffffff",
        // paddingTop: "30px",
        paddingBottom: "20px",
    },
    buttonContainer: {
      backgroundColor: "#ffffff",
      paddingTop: "30px",
      paddingBottom: "20px",
    },
    switchInput: {
      width: 0,
      height: 0,
      visibility: "hidden",
    },
    switchLabel :{
      display: "block",
      width: "500px",
      height: "150px",
      backgroundColor: "#477a85",
      borderRadius: "100px",
      position: "relative",
      cursor: "pointer",
      transition: "0.5s",
      boxShadow: "0 0 20px #477a8550",
    },
    dropzone: {
        flex: 1,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginLeft: "20px",
        marginReft: "20px",
        marginBottom: "20px",
        borderWidth: "2px",
        borderRadius: "2px",
        borderColor: "#cccccc",
        borderStyle: "dashed",
        backgroundColor: "#fafafa",
        outline: "none",
        transition: "border .24s ease-in-out",
        cursor: "pointer",
        // backgroundImage: "url('https://storage.googleapis.com/public_colab_images/ai5/mushroom.svg')",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
        minHeight: "400px",
    },
    fileInput: {
        display: "none",
    },
    preview: {
        width: "100%",
    },
    help: {
        color: "#302f2f"
    },
    safe: {
        color: "#31a354",
    },
    poisonous: {
        color: "#de2d26",
    },
});

export default styles;