# frozen_string_literal: true

class ScheduledWorker
  include Sidekiq::Worker
  attr_reader :receiver

  def perform(id)
    @receiver = EventReceiver.find_by(id: id)
    return unless receiver
    schedule_job(id)
  end

  private

  def schedule_job(id)
    if worker
      @job = Job.create(job_type: receiver.job_type, worker: worker, status: "DISPATCHED")
    else
      ScheduledWorker.perform_at(Worker::RETRY_TIME.seconds.from_now, id)
    end
  end

  def worker
    receiver
      &.user
      &.workers
      &.assignment_order
      &.first
  end
end
