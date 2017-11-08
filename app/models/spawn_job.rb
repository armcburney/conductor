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
      Job.create(job_type: job_type, worker: worker, status: "DISPATCHED")
    else
      ScheduledWorker.perform_at(Worker::RETRY_TIME.from_now, id)
    end
  end
end
