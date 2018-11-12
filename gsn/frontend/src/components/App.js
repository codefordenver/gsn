import React from "react";
import ReactDOM from "react-dom";
import BaseComponent from './BaseComponent';





const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<BaseComponent />, wrapper) : null;
