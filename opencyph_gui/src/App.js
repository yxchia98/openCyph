import "./App.css";
import ButtonChooser from "./components/ButtonChooser";
import ImageContainer from "./components/ImageContainer";
import styled from "styled-components";
import Button from "./components/Button";
import { FileUpload } from "tabler-icons-react";
import { useState } from "react";

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
    <div className="App">
      <h1>Steganography</h1>
      <OptionsContainer>
        <ButtonChooser
          buttons={["plaintext", "mp3", "mp4", "mylife"]}
          whenClick={(e) =>
            setOptionsObject({ ...optionObject, filetype: e.target.name })
          }
          title="File Type"
          defaultIndex="0"
        />
        <ButtonChooser
          buttons={["8", "7", "6", "5", "4", "3", "2", "1"]}
          whenClick={(e) =>
            setOptionsObject({ ...optionObject, numBits: e.target.name })
          }
          title="Number of Bits"
          defaultIndex="6"
        />
      </OptionsContainer>
      <div className="beforeAfter">
        <div style={{ display: "flex", flexDirection: "column" }}>
          <Button>
            <FileUpload style={{ marginRight: "10px" }}></FileUpload>
            Upload Payload
          </Button>
          <ImageContainer url="https://www.google.com/logos/doodles/2021/autumn-2021-northern-hemisphere-6753651837109082-law.gif"></ImageContainer>
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <Button>
            <FileUpload style={{ marginRight: "10px" }}></FileUpload>
            Upload Cover Object
          </Button>
          <ImageContainer url="https://www.google.com/logos/doodles/2021/autumn-2021-northern-hemisphere-6753651837109082-law.gif"></ImageContainer>
        </div>
      </div>
      {JSON.stringify(optionObject)}
      <Button handleClick={handleSubmit}>Encode</Button>
    </div>
  );
}

export default App;
