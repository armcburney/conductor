import React from 'react';
import ReactDOM from 'react-dom';
import Receiver from './receiver.jsx';
import Promise from 'promise-polyfill'; 
import 'whatwg-fetch';

// To add to window
if (!window.Promise) {
  window.Promise = Promise;
}

class EventReceivers extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.saveReceiver = this.saveReceiver.bind(this);
  }

  componentWillMount() {
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('/event_receivers.json', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Cache': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRF-Token': token
      },
      credentials: 'same-origin'
    })
      .then(res => res.json())
      .then(json => {this.setState(json); console.log(json)})
      .catch(e => console.error(e));
  }

  saveReceiver(id, data) {
    console.log(id, data);
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    console.log(token);
    fetch(`/event_receivers/${id}.json`, {
      method: 'PATCH',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Cache': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRF-Token': token
      },
      body: JSON.stringify(data),
      credentials: 'same-origin'
    })
      .then(res => res.json())
      .then(json => this.setState(state => {
        const receiverIndex = state.event_receivers.findIndex(r => r.id == json.id);
        state.event_receivers[receiverIndex] = json;
        return state;
      }))
      .catch(e => console.error(e));
  }

  render() {
    if (!this.state.event_receivers) return <p>Loading...</p>;

    return <div>{this.state.event_receivers.map((r) =>
      <Receiver
        key={r.id}
        {...r}
        save={this.saveReceiver}
        job_types={this.state.job_types} />
    )}</div>;
  }
}

document.addEventListener('DOMContentLoaded', () =>
  ReactDOM.render(<EventReceivers />, document.getElementById('event_receivers')));
