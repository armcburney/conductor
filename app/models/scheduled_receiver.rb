# frozen_string_literal: true

class ScheduledReceiver < EventReceiver
  validates :start_time, presence: true

  # Only called from sidekiq job, trigger condition will always be met
  def trigger_condition_met?(_job)
    true
  end
end
