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
    IntervalWorker.perform_at(start_time + (n * interval.seconds), id)
  end

  def n
    ((Time.zone.now.to_i - start_time) / interval).ceil
  end
end
