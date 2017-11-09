import React from 'react';
import Datetime from 'react-datetime';
import moment from 'moment';
import { camelCase, upperFirst, snakeCase, isFunction, cloneDeep } from 'lodash';
import EventActions from './event_actions';

// To add to window
if (!window.Promise) {
  window.Promise = Promise;
}

export default class Receiver extends React.Component {
  constructor(props) {
    super(props);

    this.TRIGGER_SCHEDULED = 'TRIGGER_SCHEDULED';
    this.TRIGGER_INTERVAL = 'TRIGGER_INTERVAL';


    this.state = this.nullState();

    [
      'updateType',
      'updateStartTime',
      'cancelUpdate',
      'save',
      'delete',
      'saveAction',
      'addAction',
      'removeAction',
      'updateAction',
      'actionSavedState'
    ].forEach(fn => this[fn] = this[fn].bind(this));

    [
      'interval',
      'job_type_id',
      'regex',
      'stream',
      'return_code'
    ].forEach(property => {
      const updaterName = `update${upperFirst(camelCase(property))}`;
      this[updaterName] =
        (event) => this.setState({[property]: event.target.value, dirty: true});
    });
  }

  componentDidMount() {
    this.reset(this.props);
  }

  nullState() {
    return {
      dirty: false,
      loading: false,
      type: 'ScheduledReceiver',
      start_time: null,
      interval: null,
      job_type_id: null,
      regex: null,
      stream: 'stdout',
      return_code: 0,
      event_actions: []
    };
  }

  // Picks properties from `state` that are needed to be sent in a request.
  stateToRequest() {
    return (({ type, start_time, interval, job_type_id, regex, stream, return_code }) => {

      // Turn time into a string, if it exists
      if (start_time !== null) {
        start_time = start_time.format();
      }

      return { type, start_time, interval, job_type_id, regex, stream, return_code };
    })(this.state);
  }

  componentWillReceiveProps(props) {
    if (props.updated_at != this.props.updated_at) {
      this.reset(props);
    }
    this.setState(state => {
      state.event_actions = props.event_actions.map(a => cloneDeep(a));
      return state;
    });
  }

  reset(props) {
    this.setState(state => {
      state = Object.assign({}, state, this.nullState());
      state.dirty = props.id === null;
      state.type = props.type || state.type;

      state.start_time = props.start_time ? moment(props.start_time) : null;
      state.interval = props.interval;
      state.job_type_id = props.job_type_id;
      state.regex = props.regex;
      state.stream = props.stream;
      state.return_code = props.return_code;
      state.event_actions = cloneDeep(props.event_actions);

      return state;
    });
  }

  cancelUpdate() {
    if (this.props.id === null) {
      this.delete()
    } else {
      this.reset(this.props);
    }
  }

  delete() {
    this.props.delete(this.props.index);
  }

  save() {
    this.setState({loading: true}, () => {
      this.props.save(this.props.index, this.stateToRequest());
    });
  }

  saveWithActions() {
    this.setState({loading: true}, () => this.props.save(
      this.props.index,
      Object.assign(this.stateToRequest(), {event_actions_attributes: this.props.event_actions})
    ));
  }

  updateType(event) {
    const type = event.target.value;
    this.setState(state => {
      state = Object.assign({}, state, this.nullState(), {type, dirty: true});

      if (['RegexReceiver', 'TimeoutReceiver', 'ReturnCodeReceiver'].includes(type)) {
        state.job_type_id = this.props.job_types[0].id;
      }
      return state;
    });
  }

  updateStartTime(start_time) {
    this.setState({start_time, dirty: true});
  }

  saveAction(actionIndex, data) {
    data = Object.assign(data, {event_receiver_id: this.props.id});

    // If this receiver hasn't been saved yet, so save both at once
    if (this.props.id === null) {
      this.saveWithActions();

    // Otherwise, save the action immediately
    } else {
      this.props.saveAction(
        this.props.index,
        actionIndex,
        data
      );
    }
  }

  updateAction(index, update, callback) {
    if (isFunction(update)) {
      this.setState(state => {
        state.event_actions[index] = update(state.event_actions[index]);
        return state;
      }, callback);
    } else {
      this.setState(state => {
        state.event_actions[index] = Object.assign({}, state.event_actions[index], update);
      }, callback);
    }
  }

  actionSavedState(index) {
    return this.props.event_actions[index];
  }

  removeAction(actionIndex) {
    console.log(actionIndex);
    this.props.removeAction(this.props.index, actionIndex);
  }

  addAction() {
    this.props.addAction(this.props.index);
  }

  className() {
    return `entity ${this.state.dirty ? 'dirty' : ''} ${this.state.loading ? 'loading' : ''}`;
  }

  renderJobTypePicker() {
    return (
      <select value={`${this.state.job_type_id}`} onChange={this.updateJobTypeId}>
      {this.props.job_types.map(
        (job_type, i) => <option key={i} value={`${job_type.id}`}>{job_type.name}</option>
      )}
      </select>
    );
  }

  renderForm() {
    switch (this.state.type) {
      case 'ScheduledReceiver':
        return (
          <div className='form'>
            <div className='field'>
              At: <Datetime value={this.state.start_time} onChange={this.updateStartTime} />
            </div>
          </div>
        );
      case 'IntervalReceiver':
        return (
          <div className='form'>
            <div className='field'>
              <label>Every</label>
              <input type='number' value={this.state.interval || ''} onChange={this.updateInterval} /> seconds
            </div>
            <div className='field'>
              <label>Starting</label>
              <Datetime value={this.state.start_time || ''} onChange={this.updateStartTime} />
            </div>
          </div>
        );
      case 'RegexReceiver':
        return (
          <div className='form'>
            <div className='field'>
              <label>When</label>
              <select value={this.state.stream} onChange={this.updateStream}>
                <option value='stdout'>stdout</option>
                <option value='stderr'>stderr</option>
              </select>
            </div>
            <div className='field'>
              <label>From</label> {this.renderJobTypePicker()}
            </div>
            <div className='field'>
              <label>Matches regex</label>
              <textarea value={this.state.regex || ''} onChange={this.updateRegex} />
            </div>
          </div>
        );
      case 'TimeoutReceiver':
        return (
          <div className='form'>
            <div className='field'>
              <label>When</label> {this.renderJobTypePicker()} times out
            </div>
          </div>
        );
      case 'ReturnCodeReceiver':
        return (
          <div className='form'>
            <div className='field'>
              <label>When</label> {this.renderJobTypePicker()}
            </div>
            <div className='field'>
              <label>Returns</label>
              <input type="number" value={`${this.state.return_code}`} onChange={this.updateReturnCode} />
            </div>
          </div>
        );
    }
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
          <h3>Trigger:
            <select value={this.state.type} onChange={this.updateType}>
              <option value='ScheduledReceiver'>Schedule</option>
              <option value='IntervalReceiver'>Interval</option>
              <option value='RegexReceiver'>Job stream Regex match</option>
              <option value='ReturnCodeReceiver'>{'Job return code'}</option>
              <option value='TimeoutReceiver'>Job timeout</option>
            </select>
          </h3>
          {this.renderForm()}
        </div>
        <div className='actions'>
          <h3>Actions:</h3>
          <EventActions
            actions={this.state.event_actions}
            save={this.saveAction}
            remove={this.removeAction}
            update={this.updateAction}
            savedState={this.actionSavedState}
            job_types={this.props.job_types}
          />
          <button
            className='button button--secondary'
            onClick={this.addAction}>
            Add action
          </button>
        </div>
      </div>
    );
  }
}
