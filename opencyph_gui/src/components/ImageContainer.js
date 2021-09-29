import React from "react";
import styled from "styled-components";

const ImageDiv = styled.div`
  padding: 10px;
  display: flex;
  background: #fff;
  justify-content: center;
  align-items: center;
  border-radius: 15px;
  box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  height: auto;
  width: 90%;
  :hover {
    box-shadow: 2px 4px 16px rgba(0, 0, 0, 0.16);
    transform: scale(1.01, 1.01);
  }
`;

const ImageContainer = (props) => {
  return (
    <ImageDiv>
      <img
        src={props.url}
        style={{ maxWidth: "100%", height: "auto", objectFit: "cover" }}
      ></img>
    </ImageDiv>
  );
};

export default ImageContainer;
