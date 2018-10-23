import React from "react";
import ReactDOM from "react-dom";
import UserForms from './UserForms';


const Index = () => {
  return <div>This is the future Landing page for GSN!</div>;
};


const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<UserForms />, wrapper) : null;
