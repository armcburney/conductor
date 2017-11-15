# frozen_string_literal: true

class ScheduledWorker
  include Sidekiq::Worker
  attr_reader :receiver

  def perform(id)
    @receiver = EventReceiver.find_by(id)
    return unless receiver
    schedule_job
  end

  private

  def schedule_job
    if worker
      @job = Job.new(job_type: receiver.job_type, worker: worker, status: "DISPATCHED")
    else
      ScheduledWorker.perform_at(Worker::RETRY_TIME.from_now, id)
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
