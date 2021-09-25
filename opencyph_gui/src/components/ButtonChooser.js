import React from "react";
import { useState } from "react";
import styled from "styled-components";

const ButtonGroupContainer = styled.div`
  display: flex;
  flex-flow: wrap;
  margin-bottom: 10px;
`;

const InputButton = styled.button`
  background: #fff;
  border-radius: 10em;
  border: 0px;
  box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  margin: 8px 10px 8px 0px;
  cursor: pointer;
  font-size: 16px;
  padding: 8px 14px;
  color: #000;

  ${(props) =>
    props.isActive &&
    `
    background-color: #313131;
    color: #fff;
  `}

  :hover {
    background-color: #555;
    color: #fff;
  }
`;

const Title = styled.span`
  font-size: 12px;
  text-transform: uppercase;
  font-weight: 600;
  color: #7b7b7b;
`;

const ButtonChooser = (props) => {
  const [selectedID, setSelectedID] = useState(+props.defaultIndex);
  const handleClick = (event, id) => {
    setSelectedID(id);
    props.whenClick(event);
  };
  return (
    <div>
      <Title>{props.title}</Title>
      <ButtonGroupContainer>
        {props.buttons.map((buttonLabel, i) => (
          <InputButton
            key={i}
            name={buttonLabel}
            onClick={(event) => handleClick(event, i)}
            isActive={i === selectedID ? "active" : ""}
          >
            {buttonLabel}
          </InputButton>
        ))}
      </ButtonGroupContainer>
    </div>
  );
};

export default ButtonChooser;
