import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';

import styled from 'styled-components'


const StyleTransfer = (props) => {

    console.log("================================== Home ======================================");






    return (
      <MainContainer>
        <MainTitle>Welcome to the Style Transfer App</MainTitle>
        <DescrContainer>With this app you can change images you upload. </DescrContainer>


      </MainContainer>

    );
};

export default StyleTransfer;



const MainContainer = styled.div`
  margin: "auto";
  width: "60%";
  padding: "10px";
`


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


