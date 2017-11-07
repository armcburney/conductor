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

  def next_interval_time
    (((Time.zone.now.to_i - start_time) / interval).ceil + interval).seconds
  end

  private

  def create_internal_job!
    IntervalWorker.perform_at(start_time + next_interval_time, id)
  end
end
