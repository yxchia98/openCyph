import React from "react";
import styled from "styled-components";

const OptionsContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: start;
  padding: 25px;
  display: flex;
  background: #fff;
  align-items: start;
  border-radius: 15px;
  box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.08);
  width: clamp(40%, 400px, 100%);
  margin: 10px 10px;
`;

const Title = styled.span`
  font-size: 28px;
  line-height: 1.14286;
  font-weight: 600;
  letter-spacing: 0.007em;
  margin-bottom: 10px;
`;

const HugeContainer = (props) => {
  return (
    <OptionsContainer>
      <Title>{props.type}</Title>
      {props.children}
    </OptionsContainer>
  );
};

export default HugeContainer;
