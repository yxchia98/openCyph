import React from "react";
import styled from "styled-components";

const StyledButton = styled.button`
  background: #fff;
  border-radius: 10em;
  width: 100%;
  height: 55px;
  border: 0px;
  box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  margin: 10px 8px;
  cursor: pointer;
  font-size: 22px;
  padding: 5px 20px;
  justify-content: center;
  align-items: center;
  display: flex;
  color: #000;
  :hover {
    background-color: #555;
    color: #fff;
  }
`;

const Button = (props) => {
  return (
    <StyledButton name={props.buttonLabel} onClick={(event) => props.handleClick(event, props.i)}>
      {props.children}
    </StyledButton>
  );
};

export default Button;
