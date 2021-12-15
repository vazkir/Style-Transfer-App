import React, { useEffect, useRef, useState, setState } from 'react';
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


    const defaultLatentValues = [
      {"name": "age", "value": 5},
      {"name": "eye_distance", "value": 5},
      // "eye_eyebrow_distance",
      {"name": "eye_ratio", "value": 5},
      {"name": "gender", "value": 5},
      {"name": "lip_ratio", "value": 5},
      {"name": "mouth_open", "value": 5},
      // "nose_mouth_distance",
      {"name": "nose_ratio","value": 5},
      // "nose_tip",
      // "pitch",
      // "roll",
      {"name": "smile", "value": 5},
      // "yaw"
    ]

    // Component States
    
    const listState = useState( [] );
    const [latentItems, setLatentItems] = useState(defaultLatentValues);

    const [indicator, setIndicator] = useState(defaultIndicatorText);
    const inputRef = useRef(null);
    // const [setInputImage, inputImage] = useState(null);


    const [inputImage, setInputImage] = useState(null);
    const [imgID, setImgID] = useState("1");
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
      console.log(matches)
      // Update our state
      setMatchedImgUriInput(`data:image/png;base64, ${matches.matched_img}`)
      // setLatentMask(matches.matched_latent)
      setImgID(matches.start_files_id)

      setIndicator(`Done matching: ${sliderIndicatorText}`)
      setIsLoading(false)
    }


    const scale = (number, inMin, inMax, outMin, outMax) => {
      return (number - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
    }



    const handleMutateImg = (event) => {
      console.log(event.target.files);
      setIndicator("Updating latent space based on slider......")
      setIsLoading(true)
      

      const newLatentItems = JSON.parse(JSON.stringify(latentItems));

      newLatentItems.map((latent, index) => {
        // console.log(latent)
        // console.log(latentName)
        latent.value = scale(latent.value , 0, 10, -1, 1)
      })

      const dataSend = {
        latent_id: imgID,
        values: newLatentItems
      }
      console.log(dataSend);

      DataService.GetMutatedLatentImg(dataSend)
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
      setLatentItems(defaultLatentValues)
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

    // useEffect(() => {
    //   console.log(latentItems);
    // }, [latentItems]);

    const handleSliderChange = (e, value, latentName) => {
      console.log(latentName)
      console.log(value)
      // const latentName = e.target.id
      // const copyOfObject = { ...quizAnswers }
      const newLatentItems = latentItems;

      newLatentItems.map((latent, index) => {
        // console.log(latent)
        // console.log(latentName)

        if(latent.name === latentName){
          newLatentItems[index].value = value;    
        }
      })

      setLatentItems([...newLatentItems])
      console.log(latentItems)

    }

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
                  <Typography id="label">Slider label</Typography>
                  {latentItems.map((latent, index) => (
                    <SlideWrapper key={index}>
                      <SliderTitle>{latent.name}</SliderTitle>
                      <Slider
                        aria-label={latent.name}
                        // defaultValue={5}
                        // getAriaValueText={valuetext}
                        // onChange={handleSliderChange}
                        onChangeCommitted={(e, val) => handleSliderChange(e, val, latent.name)}
                        // valueLabelDisplay="auto"
                        id={latent.name}
                        // key={index}
                        key={`slider-${index}`} /* fixed issue */
                        value={latent.value}
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


