# frozen_string_literal: true

#
# EventAction derived class using Single Table Inheritance
#
# Public interface:
#   run!
#
class SpawnJob < EventAction
  def run!
    worker = user.workers.assignment_order.first
    if worker
      job = Job.create(job_type: job_type, worker: worker, status: "DISPATCHED")
      worker.channel.trigger(:spawn, job.request_json, namespace: :worker)
    else
      ScheduledWorker.perform_at(Worker::RETRY_TIME.from_now, event_receiver.id)
    end
  end
end
