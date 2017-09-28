import React from 'react';
import ReactDOM from 'react-dom';
import Promise from 'promise-polyfill'; 
import 'whatwg-fetch';

// To add to window
if (!window.Promise) {
  window.Promise = Promise;
}

class Receiver extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div className="receiver">
      {JSON.stringify(this.props)}
      </div>
    );
  }
}

class EventReceivers extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentWillMount() {
    fetch('/event_receivers.json', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Cache': 'no-cache'
      },
      credentials: 'include'
    })
      .then(res => res.json())
      .then(json => {this.setState(json); console.log(json)})
      .catch(e => console.error(e));
  }

  render() {
    if (!this.state.event_receivers) return <p>Loading...</p>;

    return <div>{this.state.event_receivers.map((r) => <Receiver key={r.id} {...r} job_types={this.state.job_types} />)}</div>;
  }
}

document.addEventListener('DOMContentLoaded', () =>
  ReactDOM.render(<EventReceivers />, document.getElementById('event_receivers')));
