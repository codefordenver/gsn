import React, { Component } from 'react';


class Test extends Component {
  constructor(props) {
    super(props);
    this.state = {
      is_list: true,
    };
  }

  render(){
    return (
      <h3> Welcome to GSN </h3>
    );
  }
}

export default Test;
