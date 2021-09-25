import React from "react";
import "./App.css";
import ButtonChooser from "./components/ButtonChooser";
import ImageContainer from "./components/ImageContainer";
import DragAndDrop from "./components/DragAndDrop";
import styled from "styled-components";
import Button from "./components/Button";
import { FileUpload } from "tabler-icons-react";
import { useState, useReducer } from "react";

const OptionsContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
`;

function App() {
  const [optionObject, setOptionsObject] = useState({
    filetype: "plaintext",
    numBits: "2",
  });

  const reducer = (state, action) => {
    switch (action.type) {
      case "SET_DROP_DEPTH":
        return { ...state, dropDepth: action.dropDepth };
      case "SET_IN_DROP_ZONE":
        return { ...state, inDropZone: action.inDropZone };
      case "ADD_FILE_TO_LIST":
        return { ...state, fileList: state.fileList.concat(action.files) };
      default:
        return state;
    }
  };
  const [payloadData, payloadDispatch] = React.useReducer(reducer, { dropDepth: 0, inDropZone: false, fileList: [] });
  const [coverData, coverDispatch] = React.useReducer(reducer, { dropDepth: 0, inDropZone: false, fileList: [] });

  function handleSubmit() {
    fetch("http://localhost:9999/", {
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(optionObject),
    })
      .then((response) => response.json())
      .then((json) => console.log(json));
  }

  return (
    <div className='App'>
      <h1>Steganography</h1>
      <OptionsContainer>
        <ButtonChooser
          buttons={["plaintext", "mp3", "mp4", "mylife"]}
          whenClick={(e) => setOptionsObject({ ...optionObject, filetype: e.target.name })}
          title='File Type'
          defaultIndex='0'
        />
        <ButtonChooser
          buttons={["8", "7", "6", "5", "4", "3", "2", "1"]}
          whenClick={(e) => setOptionsObject({ ...optionObject, numBits: e.target.name })}
          title='Number of Bits'
          defaultIndex='6'
        />
      </OptionsContainer>
      <div className='beforeAfter'>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <DragAndDrop data={payloadData} dispatch={payloadDispatch}>
            <Button>
              <FileUpload style={{ marginRight: "10px" }}></FileUpload>
              Upload Payload
            </Button>
            <ImageContainer url='https://www.google.com/logos/doodles/2021/autumn-2021-northern-hemisphere-6753651837109082-law.gif'></ImageContainer>
          </DragAndDrop>
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <DragAndDrop data={coverData} dispatch={coverDispatch}>
            <Button>
              <FileUpload style={{ marginRight: "10px" }}></FileUpload>
              Upload Cover Object
            </Button>
            <ImageContainer url='https://www.google.com/logos/doodles/2021/autumn-2021-northern-hemisphere-6753651837109082-law.gif'></ImageContainer>
          </DragAndDrop>
        </div>
      </div>
      {JSON.stringify(optionObject)}
      <ul className='dropped-files'>
        {payloadData.fileList.map((f) => {
          return <li key={f.name}>Payload Data File: {f.name}</li>;
        })}
      </ul>
      <ul className='dropped-files'>
        {coverData.fileList.map((f) => {
          return <li key={f.name}>Cover Object File: {f.name}</li>;
        })}
      </ul>
      <Button handleClick={handleSubmit}>Encode</Button>
    </div>
  );
}

export default App;
