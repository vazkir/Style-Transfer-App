import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';

import styled from 'styled-components'
import {
  CardWrapper,
  CardHeader,
  CardHeading,
  CardBody,
  CardIcon,
  CardFieldset,
  CardInput,
  CardOptionsItem,
  CardOptions,
  CardOptionsNote,
  CardButton,
  CardLink
} from "./Card";

const Home = (props) => {

    console.log("================================== Home ======================================");






    return (
//       <MainContainer>
//         <MainTitle>Welcome to the Style Transfer App</MainTitle>
//         <DescrContainer>With this app you can change images you upload. </DescrContainer>
// 
// 
//       </MainContainer>
      <CardWrapper>
        <CardHeader>
          <CardHeading>Welcome to the Style Transfer App</CardHeading>
        </CardHeader>

        <CardBody>
        <DescrContainer>With this app you can change images you upload. </DescrContainer>


          <CardFieldset>

            <CardOptions>
              <CardOptionsItem>
                <CardIcon className="fab fa-google" big />
              </CardOptionsItem>

              <CardOptionsItem>
                <CardIcon className="fab fa-twitter" big />
              </CardOptionsItem>

              <CardOptionsItem>
                <CardIcon className="fab fa-facebook" big />
              </CardOptionsItem>
            </CardOptions>
          </CardFieldset>

          <CardFieldset>
            <Link style={{ textDecoration: 'none' }} to="/laten_manipulate" >

              <CardButton type="button">Feature manipulation</CardButton>
            </Link>
          </CardFieldset>

          <CardFieldset>
            <Link style={{ textDecoration: 'none' }} to="/style_transfer" >

              <CardButton  type="button" disabled={false}>Style Manipulation</CardButton>
            </Link>

          </CardFieldset>
        </CardBody>
      </CardWrapper>
    );
};

export default Home;



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


