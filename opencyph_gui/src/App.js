import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  NavLink,
} from "react-router-dom";
import "./App.css";
import styled from "styled-components";
import Button from "./components/Button";
import { Confetti, Download } from "tabler-icons-react";
import { useState, useReducer, useRef, useEffect } from "react";
import PayloadContainer from "./components/PayloadContainer";
import CoverContainer from "./components/CoverContainer";
import DecodeContainer from "./components/DecodeContainer";
import { FlagSpinner, ClassicSpinner } from "react-spinners-kit";
import HugeContainer from "./components/HugeContainer";

// const ENDPOINT_URL = "http://localhost:9999";
const ENDPOINT_URL = "https://stego-api.bongzy.me";

const LargeButton = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  .current {
    background-color: #0071e3 !important;
    color: #fff !important;
  }
`;
const linkStyle = {
  margin: "0",
  textDecoration: "none",
  color: "#000",
  borderRadius: "8px",
  padding: "14px 24px",
  fontSize: "22px",
  fontWeight: "bold",
  margin: "0 30px",
  backgroundColor: "#eee",
};
export default function App() {
  return (
    <Router>
      <h1>Steganography</h1>

      <div>
        <nav>
          {/* <li>
              <Link to="/">Home</Link>
            </li> */}
          <LargeButton>
            <NavLink to="/encode" style={linkStyle} activeClassName="current">
              Encode
            </NavLink>

            <NavLink to="/decode" style={linkStyle} activeClassName="current">
              Decode
            </NavLink>
          </LargeButton>
        </nav>

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route path="/encode">
            <Encode />
          </Route>
          <Route path="/decode">
            <Decode />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <>
      <h2>Welcome to LOCOL Steganography!</h2>
      <span>
        Kindly select <code>Encode</code> or <code>Decode</code> to get started.
      </span>
    </>
  );
}

function Encode() {
  const [optionObject, setOptionsObject] = useState({
    payloadType: "plaintext",
    coverType: "image",
    coverNumBits: "2",
    id: "0",
  });

  const [textData, setTextData] = useState("");

  const [isUploading, setIsUploading] = useState(false);
  const [resultsURL, setResultsURL] = useState();
  const [errorState, setErrorState] = useState();

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

  const [payloadPreviewUrl, setPayloadPreviewUrl] = useState("");
  const [coverPreviewUrl, setCoverPreviewUrl] = useState("");
  useEffect(() => {
    let reader = new FileReader();
    const [file] = payloadData.fileList;
    if (file) {
      console.log(payloadData.fileList[0]);
      reader.onloadend = (e) => {
        setPayloadPreviewUrl(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }, [payloadData]);
  useEffect(() => {
    let reader = new FileReader();
    const [file] = coverData.fileList;
    if (file) {
      console.log(coverData.fileList[0]);
      reader.onloadend = (e) => {
        setCoverPreviewUrl(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }, [coverData]);

  function handleSubmit() {
    setIsUploading(true);
    setResultsURL(null);
    setErrorState(null);
    const formData = new FormData();

    if (optionObject.coverType !== "mp4") {
      if (optionObject.payloadType !== "file") {
      } else {
        formData.append("payloadFile", payloadData.fileList[0]);
      }
      formData.append("coverFile", coverData.fileList[0]);
      formData.append(
        "optionObject",
        JSON.stringify({
          ...optionObject,
          id: Math.floor(Math.random() * 10000),
          payloadText: textData,
        })
      );
    } else {
      formData.append("coverFile", coverData.fileList[0]);
      formData.append(
        "optionObject",
        JSON.stringify({
          ...optionObject,
          id: Math.floor(Math.random() * 10000),
          payloadText: textData,
        })
      );
    }

    fetch(`${ENDPOINT_URL}/uploadFile`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((response) => {
        console.log("Response Success:", response);
        setIsUploading(false);
        if (response.error) {
          setErrorState(response.error);
        } else {
          setResultsURL(response.url + "&id=" + response.id);
        }
      })
      .catch((error) => {
        console.error("Error yo:", error);
        setIsUploading(false);
      });
  }

  return (
    <div className="App">
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
          textData={textData}
          setTextData={setTextData}
          payloadData={payloadData}
          payloadDispatch={payloadDispatch}
          imgData={payloadPreviewUrl}
        ></PayloadContainer>
        <CoverContainer
          setOptionsObject={setOptionsObject}
          optionObject={optionObject}
          coverData={coverData}
          coverDispatch={coverDispatch}
          imgData={coverPreviewUrl}
        ></CoverContainer>
      </div>
      {errorState && (
        <div
          style={{
            background: "#cc212735",
            padding: "20px",
            borderRadius: "15px",
            width: "70%",
            display: "flex",
            justifyContent: "center",
            margin: "0 auto",
          }}
        >
          {errorState}
        </div>
      )}
      {resultsURL && (
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "center",
            flexFlow: "wrap",
          }}
        >
          <HugeContainer type="Result">
            <img
              src={resultsURL}
              height="300px"
              width="100%"
              style={{ objectFit: "contain" }}
            ></img>
            <a href={resultsURL} target="_blank" download>
              <Button handleClick={() => console.log("download started")}>
                <Download />
                <span style={{ marginLeft: "8px" }}>Download</span>
              </Button>
            </a>
          </HugeContainer>
        </div>
      )}
      <div
        style={{ display: "flex", justifyContent: "center", margin: "50px" }}
      >
        <FlagSpinner loading={isUploading} size={50} color="#0071e3" />
      </div>
      <div style={{ margin: "20px 40px" }}>
        {JSON.stringify(optionObject)}

        <Button handleClick={handleSubmit} float>
          {isUploading ? (
            <ClassicSpinner
              loading={isUploading}
              size={20}
              color="#000"
              style={{ marginRight: "20px" }}
            />
          ) : (
            <Confetti></Confetti>
          )}
          <span style={{ marginLeft: "12px" }}>Encode</span>
        </Button>
      </div>
    </div>
  );
}

function Decode() {
  const [decodeOptionsObject, setDecodeOptionsObject] = useState({
    coverNumBits: "2",
    coverType: "image",
    id: "0",
  });

  const [isUploading, setIsUploading] = useState(false);
  const [resultsURL, setResultsURL] = useState();
  const [errorState, setErrorState] = useState();
  const [encodedPreviewUrl, setEncodedPreviewUrl] = useState("");

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

  const [encodedData, encodedDispatch] = useReducer(reducer, {
    dropDepth: 0,
    inDropZone: false,
    fileList: [],
  });

  useEffect(() => {
    let reader = new FileReader();
    const [file] = encodedData.fileList;
    if (file) {
      console.log(encodedData.fileList[0]);
      reader.onloadend = (e) => {
        setEncodedPreviewUrl(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }, [encodedData]);

  function handleSubmit() {
    setIsUploading(true);
    setResultsURL(null);
    setErrorState(null);
    const formData = new FormData();
    formData.append("encodedFile", encodedData.fileList[0]);
    formData.append(
      "decodeOptionsObject",
      JSON.stringify({
        ...decodeOptionsObject,
        id: Math.floor(Math.random() * 10000),
      })
    );

    fetch(`${ENDPOINT_URL}/decodeFile`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((response) => {
        console.log("Response Success:", response);
        setIsUploading(false);
        if (response.error) {
          setErrorState(response.error);
        } else {
          setResultsURL(response.url);
        }
      })
      .catch((error) => {
        console.error("Error yo:", error);
        setIsUploading(false);
      });
  }

  return (
    <div className="App">
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "center",
          flexFlow: "wrap",
        }}
      >
        <DecodeContainer
          setOptionsObject={setDecodeOptionsObject}
          optionObject={decodeOptionsObject}
          encodedData={encodedData}
          encodedDispatch={encodedDispatch}
          imgData={encodedPreviewUrl}
        ></DecodeContainer>
      </div>
      <div
        style={{ display: "flex", justifyContent: "center", margin: "50px" }}
      >
        <FlagSpinner loading={isUploading} size={50} color="#0071e3" />
      </div>
      {errorState && (
        <div
          style={{
            background: "#cc212735",
            padding: "20px",
            borderRadius: "15px",
            width: "70%",
            display: "flex",
            justifyContent: "center",
            margin: "0 auto",
          }}
        >
          {errorState}
        </div>
      )}
      {resultsURL && (
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "center",
            flexFlow: "wrap",
          }}
        >
          <HugeContainer type="Result">
            <img
              src={resultsURL}
              height="300px"
              width="100%"
              style={{ objectFit: "contain" }}
            ></img>
            <a href={resultsURL} target="_blank" download>
              <Button handleClick={() => console.log("download started")}>
                <Download />
                <span style={{ marginLeft: "8px" }}>Download</span>
              </Button>
            </a>
          </HugeContainer>
        </div>
      )}
      <div style={{ margin: "20px 40px" }}>
        {JSON.stringify(decodeOptionsObject)}

        <Button handleClick={handleSubmit} float>
          {isUploading ? (
            <ClassicSpinner
              loading={isUploading}
              size={20}
              color="#000"
              style={{ marginRight: "20px" }}
            />
          ) : (
            <Confetti></Confetti>
          )}
          <span style={{ marginLeft: "12px" }}>Decode</span>
        </Button>
      </div>
    </div>
  );
}
