# frozen_string_literal: true

class IntervalReceiver < EventReceiver
  # Callbacks
  after_create :create_internal_job!

  # Validations
  validates :start_time, :interval, presence: true

  # Only called from sidekiq job, at certain intervals
  def trigger_condition_met?(_job)
    true
  end

  private

  def create_internal_job!
    InternalWorker.perform_at(interval.from_now, id)
  end
end
