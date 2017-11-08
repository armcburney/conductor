import React from 'react';
import ReactDOM from 'react-dom';
import Promise from 'promise-polyfill';
import 'whatwg-fetch';

// To add to window
if (!window.Promise) {
  window.Promise = Promise;
}

// from https://stackoverflow.com/questions/10420352/converting-file-size-in-bytes-to-human-readable-string
function humanFileSize(bytes, si) {
  const thresh = si ? 1000 : 1024;
  if (Math.abs(bytes) < thresh) {
    return bytes + ' B';
  }
  const units = si
    ? ['kB','MB','GB','TB','PB','EB','ZB','YB']
    : ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
  let unitIndex = -1;
  do {
    bytes /= thresh;
    ++unitIndex;
  } while(Math.abs(bytes) >= thresh && unitIndex < units.length - 1);
  return bytes.toFixed(1) + ' ' + units[unitIndex];
}

class Worker extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    this.INFO_PROPS = {
      cpu_count: 'CPUs',
      load: 'Load',
      total_memory: 'Total Memory',
      available_memory: 'Free Memory',
      total_disk: 'Total Disk',
      used_disk: 'Used Disk',
      free_disk: 'Free Disk'
    };

    this.renderInfoProp = this.renderInfoProp.bind(this);
    this.renderJob = this.renderJob.bind(this);
    this.deleteWorker = this.deleteWorker.bind(this);
  }

  deleteWorker() {
    this.props.deleteWorker(this.props.id);
  }

  formatInfo(prop, value) {
    if (!['total_disk', 'used_disk', 'free_disk', 'available_memory', 'total_memory'].includes(prop)) {
      return value;
    }

    // Format as memory size
    return humanFileSize(value, true);
  }

  renderInfoProp(prop) {
    return (
      <div className='datum' key={prop}>
        <span className='title'>{this.INFO_PROPS[prop]}</span>
        <span className='value'>{this.formatInfo(prop, this.props[prop] || 0)}</span>
      </div>
    )
  }

  renderJob(job) {
    return (
      <div
        className={`job ${job.id === this.props.selected ? 'selected' : ''}`}
        key={job.id}
        onClick={() => this.props.selectJob(job.id)}>
        <span className='job-id'>
          {job.id}
        </span>
        <span className='title'>
          {this.props.jobTypes[job.job_type_id].name}
        </span>
      </div>
    )
  }

  render() {
    return (
      <div className={`worker ${this.props.deleted ? 'deleted' : ''}`}>
        {this.props.deleted ? null :
          <button className='delete button button--secondary' onClick={this.deleteWorker}>
            Delete
          </button>
        }
        <h3>{this.props.id}</h3>
        <div className='section info'>
          {Object.keys(this.INFO_PROPS).map(this.renderInfoProp)}
        </div>
        <div className='section jobs'>
          {this.props.jobs.map(this.renderJob)}
        </div>
      </div>
    );
  }
}

class Workers extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selected: null,
      stdout: '',
      stderr: '',
      hideDeleted: true,
    };

    this.selectJob = this.selectJob.bind(this);
    this.healthcheck = this.healthcheck.bind(this);
    this.deleteWorker = this.deleteWorker.bind(this);
    this.setHideDeleted = this.setHideDeleted.bind(this);
  }

  setHideDeleted(event) {
    this.setState({ hideDeleted: event.target.checked });
  }

  healthcheck(data) {
    this.setState(state => {
      const worker = state.workers.find(w => w.id == data.id);
      Object.assign(worker, data);
      return state;
    });
  }

  selectJob(id) {
    // Unsubscribe from last job
    if (this.state.selected !== null) {
      dispatcher.unsubscribe(`job.${this.state.selected}`);
    }

    this.setState({selected: id});

    // Subscribe and get initial conditions
    this.channel = dispatcher.subscribe_private(`job.${id}`, (job) => {
      this.setState(state => {
        state.returnCode = job.return_code;
        state.stdout = job.stdout;
        state.stderr = job.stderr;
        return state;
      });
    }, (err) => console.error(err));

    // Handle updates
    ['stdout', 'stderr'].forEach(stream => {
      this.channel.bind(`job.${stream}`, addition => this.setState(state => {
        if (state[stream] === null) state[stream] = '';
        state[stream] += addition;
        return state;
      }));
    });
    this.channel.bind('job.return_code', rc => this.setState(state => {
      state.returnCode = rc;
      return state;
    }));
  }

  componentWillMount() {
    fetch('/workers.json', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Cache': 'no-cache'
      },
      credentials: 'include'
    })
      .then(res => res.json())
      .then(json => {
        this.setState(state => {
          Object.assign(state, json);

          state.jobTypes = {};
          json.job_types.forEach(jobType => {
            state.jobTypes[jobType.id] = jobType;
          });
          return state;
        });

        const firstWithJobs = json.workers.find(w => !w.deleted && w.jobs.length > 0);
        if (firstWithJobs) {
          this.selectJob(firstWithJobs.jobs[0].id);
        }

        json.workers.forEach(w => {
          console.log(`worker_info.${w.id}`);
          const channel = dispatcher.subscribe_private(`worker_info.${w.id}`);
          channel.bind('worker_info.healthcheck', this.healthcheck);
        });

        console.log(json);
      })
      .catch(e => console.error(e));
  }

  deleteWorker(id) {
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch(`/workers/${id}.json`, {
      method: 'DELETE',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Cache': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRF-Token': token
      },
      credentials: 'same-origin'
    })
      .then(
        () => this.setState(state => {
          const worker = state.workers.find(w => w.id == id);
          worker.deleted = true;

          // Deselect the job if the job was in the now-deleted worker
          if (worker.jobs.some(j => j.id === state.selected)) {
            state.selected = null;
          }
          return state;
        })
      )
      .catch(e => console.error(e));
  }

  renderJob() {
    if (this.state.selected === null) {
      return (
        <div>Select a job</div>
      );
    }

    return (
      <div>
        <h2>Job {this.state.selected}</h2>
        {this.state.returnCode !== null && <p>Returned {this.state.returnCode}</p>}
        <h3>stdout</h3>
        <pre>{this.state.stdout}</pre>
        <h3>stderr</h3>
        <pre>{this.state.stderr}</pre>
      </div>
    );
  }

  render() {
    if (!this.state.workers) return <p>Loading...</p>;

    return (
      <div className={`row ${this.state.hideDeleted ? 'hideDeleted' : ''}`}>
        <div className='column second'>
          <div>
            <input type='checkbox' onChange={this.setHideDeleted} checked={this.state.hideDeleted} name='hideDeleted' id='hideDeleted' />
            <label htmlFor='hideDeleted'>Hide deleted workers</label>
          </div>
          {this.state.workers.map((w) =>
            <Worker
              key={w.id}
              {...w}
              jobTypes={this.state.jobTypes}
              selected={this.state.selected}
              selectJob={this.selectJob}
              deleteWorker={this.deleteWorker}
            />
          )}
        </div>
        <div className='column first'>
          <div className='selected-job'>
            {this.renderJob()}
          </div>
        </div>
      </div>
    );
  }
}

document.addEventListener('DOMContentLoaded', () =>
  ReactDOM.render(<Workers />, document.getElementById('workers')));
