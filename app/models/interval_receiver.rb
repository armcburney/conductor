# frozen_string_literal: true

class IntervalReceiver < EventReceiver
  validates :start_time, :interval, presence: true

  # Only called from sidekiq job, at certain intervals
  def trigger_condition_met?(_job)
    true
  end
end
