# frozen_string_literal: true

class ScheduledReceiver < EventReceiver
  def dispatch!
  end

  def trigger_condition_met?(job)
  end
end
