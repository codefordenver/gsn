import React, { Component } from 'react';
import {getDistricts} from 'services/districtServices.js';

class Districts extends Component {
  constructor(props) {
    super(props);
    this.state = {
      json: [],
      dataIsLoaded: false,
    };

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    e.preventDefault();
    getDistricts()
    .then(json => {
      this.setState({json})
      this.setState({dataIsLoaded: true})
    });
  }

  render(){
    return (
      <div className="District">
        <h1>District</h1>
        <button onClick={this.handleClick}>
           Get District Data
        </button>
        <pre>
          {this.state.dataIsLoaded
            ? JSON.stringify(this.state.json, null, 2)
            : null}
        </pre>
      </div>
    );
  }
}

export default Districts;
