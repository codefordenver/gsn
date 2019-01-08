import React, { Component } from 'react';
import {getDistricts} from '../services/districtServices.js'

class DatabaseInteractor extends Component {
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
      this.setState({json: json})
      this.setState({dataIsLoaded: true})
    });
  }




  render(){
    return (
      <div className="DatabaseInteractor">
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

export default DatabaseInteractor;
