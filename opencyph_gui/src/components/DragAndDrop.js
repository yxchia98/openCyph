import React from "react";

const DragAndDrop = (props) => {
  const { data, dispatch } = props;

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dispatch({ type: "SET_DROP_DEPTH", dropDepth: data.dropDepth + 1 });
  };
  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dispatch({ type: "SET_DROP_DEPTH", dropDepth: data.dropDepth - 1 });
    if (data.dropDepth > 0) return;
    dispatch({ type: "SET_IN_DROP_ZONE", inDropZone: false });
  };
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.dataTransfer.dropEffect = "copy";
    dispatch({ type: "SET_IN_DROP_ZONE", inDropZone: true });
  };
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();

    let files = [...e.dataTransfer.files];
    data.fileList = [];

    dispatch({ type: "ADD_FILE_TO_LIST", files });
    dispatch({ type: "SET_DROP_DEPTH", dropDepth: 0 });
    dispatch({ type: "SET_IN_DROP_ZONE", inDropZone: false });
  };

  const handleAddImage = (e) => {
    e.preventDefault();
    let files = e.target.files[0];
    data.fileList = [];

    dispatch({ type: "ADD_FILE_TO_LIST", files });
  };

  return (
    <label
      className={
        data.inDropZone ? "drag-drop-zone inside-drag-area" : "drag-drop-zone"
      }
      onDrop={(e) => handleDrop(e)}
      onDragOver={(e) => handleDragOver(e)}
      onDragEnter={(e) => handleDragEnter(e)}
      onDragLeave={(e) => handleDragLeave(e)}
    >
      {props.children}
      <div class="file-input" for="file">
        <input
          style={{
            opacity: "0",
            width: "0.1px",
            height: "0.1px",
            position: "absolute",
          }}
          type="file"
          id="file"
          onChange={(e) => handleAddImage(e)}
        ></input>
        <label>Select file</label>
      </div>
    </label>
  );
};
export default DragAndDrop;
