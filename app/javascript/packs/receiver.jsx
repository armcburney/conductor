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
      return_code: 0
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
    const updateActions = () => this.setState(state => {
      state = Object.assign({}, state);
      state.event_actions = state.event_actions.slice(0, props.event_actions.length);
      for (let i = 0; i < props.event_actions.length; i++) {
        const existing = state.event_actions[i];
        const updated = props.event_actions[i];
        if (!existing || existing.id != updated.id || existing.guid != updated.guid) {
          state.event_actions[i] = cloneDeep(updated);
        } else {
          state.event_actions[i] = Object.assign({}, existing, updated);
        }
      }
      return state;
    });

    if (props.updated_at != this.props.updated_at) {
      return this.reset(props, updateActions);
    } else {
      updateActions();
    }
  }

  reset(props, callback) {
    this.setState(state => {
      const event_actions = state.event_actions;
      state = Object.assign({}, state, this.nullState());
      state.dirty = props.id === null;
      state.type = props.type || state.type;

      state.start_time = props.start_time ? moment(props.start_time) : null;
      state.interval = props.interval;
      state.job_type_id = props.job_type_id;
      state.regex = props.regex;
      state.stream = props.stream;
      state.return_code = props.return_code;
      state.event_actions = cloneDeep(event_actions || props.event_actions);

      return state;
    }, callback);
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

  save(callback) {
    this.setState({loading: true}, () => {
      this.props.save(this.props.index, this.stateToRequest(), callback);
    });
  }

  updateType(event) {
    const type = event.target.value;
    this.setState(state => {
      const event_actions = state.event_actions;
      state = Object.assign({}, state, this.nullState(), {type, event_actions, dirty: true});

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
    const runSave = () => this.props.saveAction(
      this.props.index,
      actionIndex,
      Object.assign(data, {event_receiver_id: this.props.id})
    );

    // If this receiver hasn't been saved yet, save receiver first
    if (this.props.id === null) {
      this.save(runSave);

    // Otherwise, save the action immediately
    } else {
      runSave();
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
