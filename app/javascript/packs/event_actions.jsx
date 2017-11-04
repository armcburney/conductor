import React from 'react';
import { camelCase, upperFirst, snakeCase } from 'lodash';

class EventAction extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};

    this.DATA_FIELDS =
      ['email_address', 'webhook_url', 'webhook_body', 'job_type_id', 'type'];

    [
      'save',
      'remove',
      'cancel',
      'updateType'
    ].forEach(fn => this[fn] = this[fn].bind(this));

    this.DATA_FIELDS.slice(0, this.DATA_FIELDS.length-1).forEach(property => {
      const updaterName = `update${upperFirst(camelCase(property))}`;
      this[updaterName] =
        (event) => this.props.update({[property]: event.target.value, dirty: true});
    });
  }

  componentDidMount() {
    this.reset(this.props);
  }

  componentWillReceiveProps(props) {
    if (props.updated_at != this.props.updated_at) {
      this.reset(props);
    }
  }

  reset(props) {
    this.props.update(state => {
      state = Object.assign(state, this.nullState());
      state.dirty = props.id === null;

      this.DATA_FIELDS.forEach(field => state[field] = props[field] || state[field]);
      return state;
    });
  }

  nullState() {
    return {
      loading: false,
      type: 'EmailAction',
      email_address: null,
      webhook_url: null,
      webhook_body: null,
      job_type_id: null
    };
  }

  propsToRequest() {
    return this.DATA_FIELDS.reduce(
      (request, field) => Object.assign(request, {[field]: this.props[field]}),
      {}
    );
  }

  save() {
    this.props.update({loading: true}, () => {
      this.props.save(this.props.index, this.propsToRequest());
    });
  }

  remove() {
    this.props.remove(this.props.index);
  }

  cancel() {
    if (this.props.id !== null) {
      this.reset(this.props);
    } else {
      this.remove(this.props.index);
    }
  }

  updateType(event) {
    const type = event.target.value;
    this.props.update(state => {
      state = Object.assign(state, this.nullState(), {type, dirty: true});

      if (type == 'SpawnJobAction') {
        state.job_type_id = this.props.job_types[0].id;
      }
      return state;
    });
  }

  className() {
    return `entity ${this.props.dirty ? 'dirty' : ''} ${this.props.loading ? 'loading' : ''}`;
  }

  renderForm() {
    switch (this.props.type) {
      case 'EmailAction':
        return (
          <div className='field'>
            <label>Email</label>
            <input type='text' value={this.props.email_address || ''} onChange={this.updateEmailAddress} />
          </div>
        );
      case 'WebhookAction':
        return (
          <div>
            <div className='field'>
              <label>Webhook URL</label>
              <input type='text' value={this.props.webhook_url || ''} onChange={this.updateWebhookUrl} />
            </div>
            <div className='field'>
              <label>Webhook body</label>
              <textarea value={this.props.webhook_body || ''} onChange={this.updateWebhookBody} />
            </div>
          </div>
        );
      case 'SpawnJobAction':
        return (
          <select value={`${this.props.job_type_id}`} onChange={this.updateJobTypeId}>
          {this.props.job_types.map(
            (job_type, i) => <option key={i} value={`${job_type.id}`}>{job_type.name}</option>
          )}
          </select>
        );
    }
  }

  render() {
    return (
      <div className={this.className()}>
        <button className='button delete' onClick={this.remove}>
          Delete
        </button>
        <div className='controls'>
          <button className='button button--secondary' onClick={this.save}>Save</button>
          <button className='button' onClick={this.cancel}>Cancel</button>
        </div>
        <div className='form'>
          <div className='field'>
            <label>Type:</label>
            <select value={this.props.type} onChange={this.updateType}>
              <option value='EmailAction'>Send an email</option>
              <option value='WebhookAction'>Send a webhook</option>
              <option value='SpawnJobAction'>Spawn another job</option>
            </select>
          </div>
          {this.renderForm()}
        </div>
      </div>
    )
  }
}

export default function EventActions(props) {
  return (
    <div className='actions-list'>
    {props.actions.map(
      (action, index) =>
        <EventAction
          key={index}
          index={index}
          {...action}
          save={props.save}
          remove={props.remove}
          update={(update, callback) => props.update(index, update, callback)}
          job_types={props.job_types}
        />
    )}
    </div>
  );
}
