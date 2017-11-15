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
    logger.info worker.inspect
    if worker
      job = Job.create(job_type: job_type, worker: worker, status: "DISPATCHED")
    else
      ScheduledWorker.perform_at(Worker::RETRY_TIME.seconds.from_now, event_receiver.id)
    end
  end
end
