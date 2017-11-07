# frozen_string_literal: true

class JobWorker
  include Sidekiq::Worker
  attr_reader :receiver

  def perform(id)
    @receiver = Receiver.find_by(id)
    return unless receiver
    schedule_job
  end

  private

  def schedule_job
    if worker
      @job = Job.new(job_type: receiver.job_type, worker: worker, status: "DISPATCHED")
    else
      JobWorker.perform_at(receiver.start_time.from_now, id)
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
