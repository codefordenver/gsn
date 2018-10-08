import React from "react";
import ReactDOM from "react-dom";


class HelloWorld extends Component {

  render() {
    return (
      <div> Welcome to the GSN website </div>
    );
  }
}

const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<HelloWorld />, wrapper) : null;
