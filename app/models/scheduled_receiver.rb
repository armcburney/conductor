# frozen_string_literal: true

class ScheduledReceiver < EventReceiver
  # Only called from sidekiq job, trigger condition will always be met
  def trigger_condition_met?(_job)
    true
  end
end
