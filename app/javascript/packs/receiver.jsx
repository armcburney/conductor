import React from 'react';
import Datetime from 'react-datetime';
import moment from 'moment';

// To add to window
if (!window.Promise) {
  window.Promise = Promise;
}

export default class Receiver extends React.PureComponent {
  constructor(props) {
    super(props);

    this.TRIGGER_SCHEDULED = 'TRIGGER_SCHEDULED';
    this.TRIGGER_INTERVAL = 'TRIGGER_INTERVAL';


    console.log(props);
    this.state = {
      selectedTriggerOption: this.TRIGGER_SCHEDULED
    };

    this.updateScheduleTime = this.updateScheduleTime.bind(this);
    this.selectTriggerOption = this.selectTriggerOption.bind(this);
    this.updateInterval = this.updateInterval.bind(this);
    this.updateStartAtTime = this.updateStartAtTime.bind(this);
    this.cancelUpdate = this.cancelUpdate.bind(this);
    this.save = this.save.bind(this);
    this.delete = this.delete.bind(this);
  }

  componentDidMount() {
    this.componentWillReceiveProps(this.props);
  }

  componentWillReceiveProps(props) {
    if (props.interval) {
      this.setState({
        dirty: props.id === null,
        loading: false,
        selectedTriggerOption: this.TRIGGER_INTERVAL,
        scheduleTime: null,
        startAtTime: moment(props.start_time),
        interval: props.interval
      });
    } else {
      this.setState({
        dirty: props.id === null,
        loading: false,
        selectedTriggerOption: this.TRIGGER_SCHEDULED,
        scheduleTime: moment(props.start_time),
        startAtTime: null,
        interval: null
      });
    }
  }

  cancelUpdate() {
    if (this.props.id === null) {
      this.delete()
    } else {
      this.componentWillReceiveProps(this.props);
    }
  }

  delete() {
    this.props.delete(this.props.index);
  }

  save() {
    let startTime = null
    if (this.state.interval && this.state.startAtTime) {
      startTime = this.state.startAtTime.format();
    } else if (this.state.scheduleTime) {
      startTime = this.state.scheduleTime.format();
    }

    this.setState({loading: true});

    this.props.save(this.props.index, {
      start_time: startTime,
      interval: this.state.selectedTriggerOption == this.TRIGGER_INTERVAL ? this.state.interval : null
    });
  }

  updateScheduleTime(scheduleTime) {
    this.setState({scheduleTime, dirty: true});
  }

  updateInterval(event) {
    this.setState({interval: event.target.value, dirty: true});
  }

  updateStartAtTime(startAtTime) {
    this.setState({startAtTime, dirty: true});
  }

  selectTriggerOption(event) {
    this.setState({selectedTriggerOption: event.target.name, dirty: true});
  }

  className() {
    return `receiver ${this.state.dirty ? 'dirty' : ''} ${this.state.loading ? 'loading' : ''}`;
  }

  render() {
    return (
      <div className={this.className()}>
        <button className='button delete' onClick={this.delete}>
          Delete
        </button>
        <div className='controls'>
          <button className='button button--secondary' onClick={this.save}>Save</button>
          <button className='button' onClick={this.cancelUpdate}>Cancel</button>
        </div>
        <div className='trigger'>
          <h3>Trigger:</h3>
          <div className='trigger-option'>
            <input
              type='radio'
              name={this.TRIGGER_SCHEDULED}
              id={this.TRIGGER_SCHEDULED}
              checked={this.state.selectedTriggerOption == this.TRIGGER_SCHEDULED}
              onChange={this.selectTriggerOption} />
            <label htmlFor={this.TRIGGER_SCHEDULED}>
              {'At'}
              <Datetime value={this.state.scheduleTime} onChange={this.updateScheduleTime} />
            </label>
          </div>
          <div className='trigger-option'>
            <input
              type='radio'
              name={this.TRIGGER_INTERVAL}
              id={this.TRIGGER_INTERVAL}
              checked={this.state.selectedTriggerOption == this.TRIGGER_INTERVAL}
              onChange={this.selectTriggerOption} />
            <label htmlFor={this.TRIGGER_INTERVAL}>
              {'Every'}
              <input type='number' value={this.state.interval || ''} onChange={this.updateInterval} />
              {'seconds, starting at'}
              <Datetime value={this.state.startAtTime} onChange={this.updateStartAtTime} />
            </label>
          </div>
        </div>
        <div className='actions'>
          <h3>Actions:</h3>
          <div className='action-list'>
          </div>
        </div>
      </div>
    );
  }
}
