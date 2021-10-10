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
  height: 4em;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
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

const CoverContainer = (props) => {
  return (
    <HugeContainer type='Cover Object'>
      {props.optionObject.payloadType === "plaintext" && (
        <ButtonChooser
          buttons={["mp4"]}
          whenClick={(e) =>
            props.setOptionsObject({
              ...props.optionObject,
              coverType: e.target.name,
            })
          }
          title='File Type'
          defaultIndex='0'
        />
      )}
      {props.optionObject.payloadType !== "plaintext" && (
        <ButtonChooser
          buttons={["image", "wav"]}
          whenClick={(e) =>
            props.setOptionsObject({
              ...props.optionObject,
              coverType: e.target.name,
            })
          }
          title='File Type'
          defaultIndex='0'
        />
      )}
      <ButtonChooser
        buttons={["8", "7", "6", "5", "4", "3", "2", "1"]}
        whenClick={(e) =>
          props.setOptionsObject({
            ...props.optionObject,
            coverNumBits: e.target.name,
          })
        }
        title='Number of Bits'
        defaultIndex='6'
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
        <DragAndDrop data={props.coverData} dispatch={props.coverDispatch}>
          {props.coverData.fileList[0] ? (
            <>
              <img src={props.imgData} height='300px' width='100%' style={{ objectFit: "contain", overflow: "hidden" }}></img>
              <SelectedFile>
                {props.coverData.fileList.map((f) => (
                  <>
                    <span
                      style={{
                        fontSize: "16px",
                      }}
                    >
                      {f.name}
                    </span>
                    <span
                      style={{
                        padding: "5px",
                        background: "#ddd",
                        borderRadius: "8px",
                        marginTop: "8px",
                        fontSize: "12px",
                      }}
                    >
                      {(f.size / 1000).toFixed(2)}kb
                    </span>
                  </>
                ))}
              </SelectedFile>
            </>
          ) : (
            <FileUploadBox>
              <FileUpload size={88} color='white' style={{ strokeWidth: "1.2", marginBottom: "15px" }}></FileUpload>
              <span>Drag n' Drop your file here</span>
            </FileUploadBox>
          )}
        </DragAndDrop>
      </div>
    </HugeContainer>
  );
};

export default CoverContainer;
