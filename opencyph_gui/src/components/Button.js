import React from "react";
import styled from "styled-components";

const StyledButton = styled.button`
  background: #fff;
  border-radius: 10em;
  border: 0px;
  box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  margin: 8px 8px 8px 0px;
  cursor: pointer;
  font-size: 18px;
  padding: 10px 18px;
  justify-content: center;
  align-items: center;
  display: flex;
  color: #000;
  float: ${(props) => (props.float ? "left" : "right")};
  :hover {
    background-color: #555;
    color: #fff;
  }
`;

const Button = (props) => {
  return (
    <StyledButton
      name={props.buttonLabel}
      onClick={(event) => props.handleClick(event, props.i)}
    >
      {props.children}
      {props.float}
    </StyledButton>
  );
};

export default Button;
