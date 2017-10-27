# frozen_string_literal: true

class TimeoutReceiver < EventReceiver
  def dispatch!
  end

  def trigger_condition_met?(job)
  end
end
