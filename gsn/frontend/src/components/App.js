import React from "react";
import ReactDOM from "react-dom";


const Index = () => {
  return <div>This is the future Landing page for GSN!</div>;
};


const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<Index />, wrapper) : null;
