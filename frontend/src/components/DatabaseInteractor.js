import React, { Component } from 'react';


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
    fetch('http://127.0.0.1:8000/gsndb/district/')
    .then(res => res.json())
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
