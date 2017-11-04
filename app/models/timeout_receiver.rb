# frozen_string_literal: true

class TimeoutReceiver < EventReceiver
  def trigger_condition_met?(job)
    job.created_at.between?(job.created_at + job.timeout.seconds, job.created_at)
  end
end
