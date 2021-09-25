import React from "react";
import "./App.css";
import ButtonChooser from "./components/ButtonChooser";
import ImageContainer from "./components/ImageContainer";
import DragAndDrop from "./components/DragAndDrop";
import styled from "styled-components";
import Button from "./components/Button";
import { Confetti } from "tabler-icons-react";
import { useState, useReducer } from "react";
import PayloadContainer from "./components/PayloadContainer";
import CoverContainer from "./components/CoverContainer";
import { FireworkSpinner } from "react-spinners-kit";

const ENDPOINT_URL = "http://localhost:9999";

function App() {
  const [optionObject, setOptionsObject] = useState({
    payloadType: "plaintext",
    coverType: "image",
    coverNumBits: "2",
  });

  const [isUploading, setIsUploading] = useState(false);

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
  const [payloadData, payloadDispatch] = useReducer(reducer, {
    dropDepth: 0,
    inDropZone: false,
    fileList: [],
  });
  const [coverData, coverDispatch] = useReducer(reducer, {
    dropDepth: 0,
    inDropZone: false,
    fileList: [],
  });

  function handleSubmit() {
    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", payloadData.fileList[0]);

    fetch(`${ENDPOINT_URL}/uploadFile`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((response) => {
        console.log("Success:", response);
        setIsUploading(false);
      })
      .catch((error) => {
        console.error("Error yo:", error);
        setIsUploading(false);
      });
  }

  return (
    <div className="App">
      <h1>Steganography</h1>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "center",
          flexFlow: "wrap",
        }}
      >
        <PayloadContainer
          setOptionsObject={setOptionsObject}
          optionObject={optionObject}
          payloadData={payloadData}
          payloadDispatch={payloadDispatch}
        ></PayloadContainer>
        <CoverContainer
          setOptionsObject={setOptionsObject}
          optionObject={optionObject}
          coverData={coverData}
          coverDispatch={coverDispatch}
        ></CoverContainer>
      </div>

      <div style={{ margin: "20px 40px" }}>
        {JSON.stringify(optionObject)}
        <Button handleClick={handleSubmit} float>
          {isUploading ? (
            <FireworkSpinner
              loading={isUploading}
              size={20}
              color="#000"
              style={{ marginRight: "8px" }}
            />
          ) : (
            <Confetti></Confetti>
          )}
          <span style={{ marginLeft: "8px" }}>Encode</span>
        </Button>
      </div>
    </div>
  );
}

export default App;
