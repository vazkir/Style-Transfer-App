import React, { useEffect, useRef, useState } from 'react';
import { withStyles } from '@material-ui/core';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';

import DataService from "../../services/DataService";
import styles from './styles';

const Home = (props) => {
    const { classes } = props;

    console.log("================================== Home ======================================");

    const inputFile = useRef(null);

    // Component States
    const [image, setImage] = useState(null);
    const [matchedImgUri, setMatchedImgUri] = useState(null);
    const [latentMask, setLatentMask] = useState(null);

    // Setup Component
    useEffect(() => {

    }, []);

    // Handlers
    const handleImageUploadClick = () => {
        inputFile.current.click();
    }

    const setMatchedResponse = (data) => {
      const matches = data

      // Update our state
      setMatchedImgUri(`data:image/png;base64, ${matches.matched_img}`)
      setLatentMask(matches.matched_latent)
    }

    const handleOnChange = (event) => {
        console.log(event.target.files);
        setImage(URL.createObjectURL(event.target.files[0]));

        var formData = new FormData();
        formData.append("file", event.target.files[0]);
        DataService.GetLatentMatch(formData)
            .then(function (response) {
                console.log(response.data);
                setMatchedResponse(response.data);
            })
    }

    return (
        <div className={classes.root}>
            <main className={classes.main}>
            {/* <Container maxWidth="md" className={classes.container}>
              <input className={classes.switchInput} type="checkbox" name="switch" id="switch"/>
              <label className={classes.switchLabel} for="switch"></label>
            </Container> */}

                <Container maxWidth="md" className={classes.buttonContainer}>
                    <div className={classes.dropzone} onClick={() => handleImageUploadClick()}>
                        <input
                            type="file"
                            accept="image/*"
                            capture="camera"
                            on
                            autocomplete="off"
                            tabindex="-1"
                            className={classes.fileInput}
                            ref={inputFile}
                            onChange={(event) => handleOnChange(event)}
                        />
                        <div><img className={classes.preview} src={image} /></div>
                        <div className={classes.help}>Click to take a picture or upload...</div>
                    </div>
                    <h2>Matched image</h2>
                    <div><img className={classes.preview} src={matchedImgUri} /></div>
                </Container>
            </main>
        </div>
    );
};

export default withStyles(styles)(Home);