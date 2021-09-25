import React from "react";
import ButtonChooser from "./ButtonChooser";
import { FileUpload } from "tabler-icons-react";
import Button from "./Button";
import ImageContainer from "./ImageContainer";
import DragAndDrop from "./DragAndDrop";
import HugeContainer from "./HugeContainer";
import styled from "styled-components";

const SelectedFile = styled.span`
  border-radius: 8px;
  background-color: #eee;
  font-weight: 600;
  padding: 10px;
  font-size: 14px;
  width: 90%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  height: 2em;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const InputText = styled.textarea`
  background: #efefef;
  outline: none;
  border: none;
  border-radius: 12px;
  padding: 12px;
  font-size: 16px;
  width: 100%;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  height: 100%;
  font-family: Inter;
  resize: none;
  transition: all 0.3s;

  :hover {
    box-shadow: 2px 4px 16px rgba(0, 0, 0, 0.16);
  }
  :active,
  :focus {
    box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.08);
    border: 3px solid #0071e3;
  }
`;

const FileUploadBox = styled.div`
  display: flex;
  width: 350px;
  height: 200px;
  justify-content: center;
  flex-direction: column;
  padding: 25px;
  display: flex;
  background: #0071e3;
  align-items: center;
  border-radius: 15px;
  transition: all 0.3s;
  :hover {
    box-shadow: 2px 4px 16px rgba(0, 0, 0, 0.16);
    transform: scale(1.01, 1.01);
  }
  color: white;
`;

const PayloadContainer = (props) => {
  return (
    <HugeContainer type="Payload Object">
      <ButtonChooser
        buttons={["plaintext", "mylife"]}
        whenClick={(e) =>
          props.setOptionsObject({
            ...props.optionObject,
            payloadType: e.target.name,
          })
        }
        title="File Type"
        defaultIndex="0"
      />

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          width: "100%",
          height: "100%",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {props.optionObject.payloadType === "plaintext" && (
          <InputText
            type="text"
            placeholder="Enter your text here..."
          ></InputText>
        )}
        {props.optionObject.payloadType !== "plaintext" && (
          <DragAndDrop
            data={props.payloadData}
            dispatch={props.payloadDispatch}
          >
            {props.payloadData.fileList[0] ? (
              <SelectedFile>
                {props.payloadData.fileList.map((f) => f.name)}
              </SelectedFile>
            ) : (
              <FileUploadBox>
                <FileUpload
                  size={88}
                  color="white"
                  style={{ strokeWidth: "1.2", marginBottom: "15px" }}
                ></FileUpload>
                <span>Drag n' Drop your file here</span>
              </FileUploadBox>
            )}
          </DragAndDrop>
        )}
      </div>
    </HugeContainer>
  );
};

export default PayloadContainer;
