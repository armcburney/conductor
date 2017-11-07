# frozen_string_literal: true

class IntervalReceiver < EventReceiver
  # Callbacks
  after_create :create_internal_job!

  # Validations
  validates :start_time, :interval, presence: true

  # Sidekiq job scheduled after_create => trigger condition will always be met
  def trigger_condition_met?(_job)
    true
  end

  private

  def create_internal_job!
    InternalWorker.perform_at(interval.from_now, id)
  end
end
