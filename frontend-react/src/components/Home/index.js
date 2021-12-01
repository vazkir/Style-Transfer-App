import React, { useEffect, useRef, useState } from 'react';
import { withStyles } from '@material-ui/core';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import styled from 'styled-components'

import DataService from "../../services/DataService";
import styles from './styles';

const Home = (props) => {
    const { classes } = props;

    console.log("================================== Home ======================================");

    const inputFile = useRef(null);

    // Component States
    const [image, setImage] = useState(null);
    const [imgID, setImgID] = useState(null);
    const [matchedImgUriInput, setMatchedImgUriInput] = useState(null);
    const [matchedImgUriOuput, setMatchedImgUriOuput] = useState(null);

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
      setMatchedImgUriInput(`data:image/png;base64, ${matches.matched_img}`)
      // setLatentMask(matches.matched_latent)
      setImgID(matches.latent_id)
    }


    const setChangedLatentResponse = (data) => {
      const matches = data

      // Update our state
      setMatchedImgUriOuput(`data:image/png;base64, ${matches.changed_img}`)
    }


    const handleUploadImg = (event) => {
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


    const handleMutateImg = (event) => {
      console.log(event.target.files);


      var formData = new FormData();
      formData.append("latent_id", imgID);
      DataService.GetMutatedLatentImg(formData)
          .then(function (response) {
              console.log(response.data);
              setChangedLatentResponse(response.data);
          })
    }

    return (
        <div className={classes.root}>

        <UploadContainer>
          
            <Container maxWidth="md" className={classes.buttonContainer}>
              <Subtitle>Matched image</Subtitle>

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
                        onChange={(event) => handleUploadImg(event)}
                    />
                    <div><img className={classes.preview} src={image} /></div>
                    <div className={classes.help}>Click to take a picture or upload...</div>
                </div>
            </Container>
        </UploadContainer>
        <ModelContainer>
          <Subtitle>Changing the image</Subtitle>
          <FlexContainer>
            <InputLatentContainer>
              <div><img className={classes.preview} src={matchedImgUriInput} /></div>
            </InputLatentContainer>
            <SwitchContainer>
              <button onClick={(event) => handleMutateImg(event)}>Make person older</button>
            </SwitchContainer>
            <OutputLatentContainer>
              <div><img className={classes.preview} src={matchedImgUriOuput} /></div>
            </OutputLatentContainer>
          </FlexContainer>

        </ModelContainer>
      </div>

    );
};

export default withStyles(styles)(Home);



const UploadContainer = styled.div`
  /* flexGrow: 1, */
  height: "30vh";
`

const ModelContainer = styled.div`
  /* flexGrow: 1, */
  height: "70vh";
`

const FlexContainer = styled.div`
  /* flexGrow: 1, */
  height: "70vh";
  background-color: "#ffffff";
  padding-top: "30px";
  padding-bottom: "20px";
  display: flex;
  flex-wrap: wrap;

`
const InputLatentContainer = styled.div`

  flex: 1 1 40%;


`

const SwitchContainer = styled.div`

flex: 1 1 20%;
background-color: "red";


`

const OutputLatentContainer = styled.div`

flex: 1 1 40%;


`

const Subtitle = styled.h2`
  text-align: center;

`


