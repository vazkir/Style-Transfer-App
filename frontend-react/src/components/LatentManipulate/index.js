import React, { useEffect, useRef, useState } from 'react';
import { withStyles } from '@material-ui/core';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import styled from 'styled-components'
import LoadingOverlay from 'react-loading-overlay';

import DataService from "../../services/DataService";
import styles, { SliderDeck } from './Styles';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import {
  MainContainer,
  StatusPanel,
  MainUi,
  ImgUploadDeck,
  DropZone,
  FileInput,
  ImgPreview,
  ImgHelp,
  SlidersContainer,
  SlideWrapper,
  SliderTitle,
  SliderButtonContainer,
  SubmitSlidersButton,
  DisplayResultDeck,
  ImgResult,
  ResetButtonContainer,
  RestetAllButton,
} from "./Styles";


function valuetext(value) {
  return `${value}°C`;
}


const LatentManipulate = (props) => {
    const { classes } = props;

    console.log("================================== Latent Manipulate ======================================");

    const defaultIndicatorText = "Let's get started!"
    const sliderIndicatorText = "You can now use the sliders to change the matched latent img"


    const latentNames = [
      'Age',
      'Gender',
      'Bla bla',
      'Something',
      'Anothat one'
    ]

    // Component States
    const [indicator, setIndicator] = useState(defaultIndicatorText);
    const inputRef = useRef(null);
    // const [setInputImage, inputImage] = useState(null);


    const [inputImage, setInputImage] = useState(null);
    const [imgID, setImgID] = useState(null);
    const [matchedImgUriInput, setMatchedImgUriInput] = useState(null);
    const [matchedImgUriOuput, setMatchedImgUriOuput] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const [latentMask, setLatentMask] = useState(null);

    // Setup Component
    useEffect(() => {

    }, []);

    // Handlers
    const handleImageUploadClick = () => {
      inputRef.current.click();
    }

    const handleUploadImg = (event) => {
        console.log(event.target.files);
        setInputImage(URL.createObjectURL(event.target.files[0]));

        var formData = new FormData();
        formData.append("file", event.target.files[0]);
        setIndicator("Matchinhg input image to latent representation.....")
        setIsLoading(true)

        DataService.GetLatentMatch(formData)
            .then(function (response) {
                console.log(response.data);
                setMatchedResponse(response.data);
            })
    }


    const setMatchedResponse = (data) => {
      const matches = data

      // Update our state
      setMatchedImgUriInput(`data:image/png;base64, ${matches.matched_img}`)
      // setLatentMask(matches.matched_latent)
      setImgID(matches.latent_id)

      setIndicator(`Done matching: ${sliderIndicatorText}`)
      setIsLoading(false)
    }


    const handleMutateImg = (event) => {
      console.log(event.target.files);
      setIndicator("Updating latent space based on slider......")
      setIsLoading(true)

      var formData = new FormData();
      formData.append("latent_id", imgID);
      DataService.GetMutatedLatentImg(formData)
          .then(function (response) {
              console.log(response.data);
              setChangedLatentResponse(response.data);
          })
    }

    const setChangedLatentResponse = (data) => {
      const matches = data

      // Update our state
      setMatchedImgUriOuput(`data:image/png;base64, ${matches.changed_img}`)
      setIndicator(sliderIndicatorText)
      setIsLoading(false)
    }


    const resetExperiment = (event) => {
          // Component States
      setIndicator(defaultIndicatorText);
      // setInputImage(null);
      setImgID(null);
      setInputImage(null);
      setMatchedImgUriInput(null);
      setMatchedImgUriOuput(null);
      setIsLoading(false)
      // inputImage.current.value = null;

      // TODO: Set sliders to default!
    }

    const StyledLoader = styled(LoadingOverlay)`
      width: 100%;
      height: 100%;
      overflow: scroll;
      .MyLoader_overlay {
        background: rgba(172, 172, 172, 0.8);
      }
      &.MyLoader_wrapper--active {
        overflow: hidden;
      }
    `;

    return (
        <MainContainer>
          <StatusPanel><h2>{indicator}</h2></StatusPanel>
          <StyledLoader
            active={isLoading}
            spinner
            text={"Loading...."}
            classNamePrefix='MyLoader_'
          >
            <MainUi>

              <ImgUploadDeck>
              {matchedImgUriInput == null
                ? 
                <DropZone onClick={() => handleImageUploadClick()}>
                  <FileInput
                      type="file"
                      accept="image/*"
                      capture="camera"
                      on
                      autocomplete="off"
                      tabindex="-1"
                      ref={inputRef}
                      onChange={(event) => handleUploadImg(event)}
                  />
                  <ImgPreview src={inputImage}></ImgPreview>
                  <ImgHelp>Click to take a picture or upload...</ImgHelp>
                </DropZone>
                : <ImgResult src={matchedImgUriInput}></ImgResult>
              }
                
              </ImgUploadDeck>
              <SliderDeck>
                <SlidersContainer>
                  {latentNames.map((row, index) => (
                    <SlideWrapper key={index}>
                      <SliderTitle>{row}</SliderTitle>
                      <Slider
                        aria-label="Age"
                        defaultValue={5}
                        getAriaValueText={valuetext}
                        valueLabelDisplay="auto"
                        step={1}
                        marks
                        min={0}
                        max={10}
                      />
                    </SlideWrapper>
                  ))}

                </SlidersContainer>
                <SliderButtonContainer>
                  <SubmitSlidersButton 
                    type="button"
                    onClick={(event) => handleMutateImg(event)}  
                  >Submit Values</SubmitSlidersButton>
                </SliderButtonContainer>
              </SliderDeck>
              <DisplayResultDeck>
                  <ImgResult src={matchedImgUriOuput}></ImgResult>
              </DisplayResultDeck>

            </MainUi>
          </StyledLoader>

          <ResetButtonContainer>
            <RestetAllButton 
            type="button" 
            onClick={(event) => resetExperiment(event)}
            
              >Reset experiment</RestetAllButton>

          </ResetButtonContainer>


        {/* <UploadContainer>
            <Slider
              aria-label="Age"
              defaultValue={5}
              getAriaValueText={valuetext}
              valueLabelDisplay="auto"
              step={1}
              marks
              min={0}
              max={10}
            />
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

        </ModelContainer> */}
      </MainContainer>

    );
};

export default LatentManipulate;






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


