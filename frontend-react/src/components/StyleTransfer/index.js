import React, { useEffect, useRef, useState, setState } from 'react';
import { Link } from 'react-router-dom';
import DataService from "../../services/DataService";
import styled from 'styled-components'

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


const StyleTransfer = (props) => {

    console.log("================================== Home ======================================");


    

    const inputRef = useRef(null);
    // const [setInputImage, inputImage] = useState(null);


    const [inputImage, setInputImage] = useState(null);
    const [imgID, setImgID] = useState("1");
    const [matchedImgUriInput, setMatchedImgUriInput] = useState(null);
    const [matchedImgUriOuput, setMatchedImgUriOuput] = useState(null);
    const [inputFile, setInputFile] = useState(null);

    const [isLoading, setIsLoading] = useState(false);

    const [latentMask, setLatentMask] = useState(null);

    // Handlers
    const handleImageUploadClick = () => {
      inputRef.current.click();
    }

    const handleUploadImg = (event) => {
        console.log(event.target.files);
        setInputImage(URL.createObjectURL(event.target.files[0]));

        setInputFile( event.target.files[0])
        changeStyleImg(event.target.files[0])


    }

    const changeStyleImg = (fileImge) => {
      var formData = new FormData();
      formData.append("file", fileImge);
      setIsLoading(true)

      DataService.ApplyST(formData, selectedStyle)
      .then(function (response) {
          console.log(response.data);
          setMatchedResponse(response.data);
      })
      
    }

    const setMatchedResponse = (data) => {
      const matches = data
      console.log(matches)
      // Update our state
      setMatchedImgUriOuput(`data:image/png;base64, ${matches.matched_img}`)
      // setLatentMask(matches.matched_latent)
      setImgID(matches.start_files_id)

      setIsLoading(false)
    }

    const resetExperiment = (event) => {
      // Component States
      // setInputImage(null);
      setImgID(null);
      setInputImage(null);
      setMatchedImgUriInput(null);
      setMatchedImgUriOuput(null);
      setIsLoading(false)
      setInputFile(null)
      // inputImage.current.value = null;

      // TODO: Set sliders to default!
    }


    const styles = [
      "candy",
      "composition 6",
      "feathers",
      "la_muse",
      "mosaic",
      "starry night",
      "the scream",
      "the wave",
      "udnie",
    ]

    const [selectedStyle, setSelectedStyle] = useState("mosaic");

    const handleChange = (e) => {
      setSelectedStyle(e.target.value);

      if (inputFile !== null){
        changeStyleImg(inputFile)

      }

    };


    return (
      <MainContainer>
        <MainTitle>Welcome to the Style Manipulation</MainTitle>
        <DescrContainer>Simply select a style you want transfered and upload an image</DescrContainer>
        <div>
          <select value={selectedStyle} onChange={handleChange}>
          {styles.map((style, index) => (
            <option key={index} value={style}>{style}</option>

          ))}

          </select>
        </div>
        <MainUi>

          <ImgUploadDeck>
            {matchedImgUriOuput == null
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
              : <ImgResult src={inputImage}></ImgResult>
            }
              
            </ImgUploadDeck>
          <DisplayResultDeck>
              <ImgResult src={matchedImgUriOuput}></ImgResult>
          </DisplayResultDeck>
        </MainUi>
        <ResetButtonContainer>
            <RestetAllButton 
            type="button" 
            onClick={(event) => resetExperiment(event)}
            
              >Reset experiment</RestetAllButton>

          </ResetButtonContainer>
      </MainContainer>

    );
};

export default StyleTransfer;




const MainTitle = styled.h1`
  text-align: center;

`
const DescrContainer = styled.div`
  position: relative;
  padding: 0;
  margin: 0;
  border: 0;

  & + & {
    margin-top: 24px;
  }

  &:nth-last-of-type(2) {
    margin-top: 32px;
  }

  &:last-of-type {
    text-align: center;
  }
`




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


