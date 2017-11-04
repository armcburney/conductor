# frozen_string_literal: true

class TimeoutReceiver < EventReceiver
  def trigger_condition_met?(job)
    # check if job.job_type.timeout exceeded
  end
end
