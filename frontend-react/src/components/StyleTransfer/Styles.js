import React from "react";

import styled, { css } from "styled-components";

export const MainContainer = styled.div`
  margin: auto;
  width: 80vw;
  padding: 25px; // Inside
  background: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

export const StatusPanel = styled.div`
  width: 100%;
  text-align: center;
`;
export const MainUi = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 100%;
`;
export const ImgUploadDeck = styled.div`
  width: 45%;
  min-height: 50%;
  display: flex;
  justify-content: center;
  align-items: center;

  /* padding: 10px; */
`;

export const DisplayResultDeck = styled.div`
  width: 45%;
  min-height: 50%;
  display: flex;
  justify-content: center;
  align-items: center;

  /* padding: 10px; */
`;

export const DropZone = styled.div`
  /* flex: 1; */
  display: flex;
  flex-direction: column;
  align-items: center;
  /* margin-left: 20px;
  margin-right: 20px; */
  /* margin-bottom: 20px; */
  border-width: 2px;
  border-radius: 2px;
  border-color: #cccccc;
  border-style: dashed;
  background-color: #4546;
  outline: none;
  transition: border .24s ease-in-out;
  cursor: pointer;
  // backgroundImage: "url('https://storage.googleapis.com/public_colab_images/ai5/mushroom.svg')",
  background-repeat: no-repeat;
  background-position: center;

`;




export const FileInput = styled.input`
  display: none;
`;

export const ImgPreview = styled.img`
  max-height:30vh;
  width: 100%;
`;

export const ImgResult = styled.img`
  max-height:30vh;
  width: 100%;
`;



export const ImgHelp = styled.div`
  color: #302f2f;
`;



export const SliderDeck = styled.div`
  width: 20%;
  display: flex;
  flex-direction: column;
  aling-items: top;
`;


export const SlidersContainer = styled.div`
  /* height: 75%; */
  padding-bottom: 25px;
`;


export const SlideWrapper = styled.div`
  display: flex;
  flex-direction: column;

  
`;
export const SliderTitle = styled.h4`
  margin: 0;
  padding: 0;
  text-align: center;
`;



export const SliderButtonContainer = styled.div`
  height: 15%;
  /* margin-top: 35px; */
  margin-top: 15px;
`;

export const SubmitSlidersButton = styled.button`
  /* display: block; */
  width: 100%;
  height: 100%;
  padding: 12px 0;
  font-family: inherit;
  font-size: 14px;
  font-weight: 700;
  color: #fff;
  background-color: #00cc99;
  border: 0;
  border-radius: 35px;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.02, 0.01, 0.47, 1);

  &:hover {
    box-shadow: 0 15px 15px rgba(0, 0, 0, 0.16);
    transform: translate(0, -5px);
  }
`;




export const ResetButtonContainer = styled.div`
  justify-content: center;
  width: 100%;
  padding-top:45px;
`;

export const RestetAllButton = styled.button`
  /* display: block; */
  width: 100%;
  height: 100%;
  padding: 12px 0;
  font-family: inherit;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  background-color: #e5195f;
  border: 0;
  border-radius: 35px;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.02, 0.01, 0.47, 1);

  &:hover {
    box-shadow: 0 15px 15px rgba(0, 0, 0, 0.16);
    transform: translate(0, -5px);
  }
`;
