# frozen_string_literal: true

class RegexReceiver < EventReceiver
  validates :stream, inclusion: { in: %w(stdout stderr) }

  def trigger_condition_met?(job)
    @trigger_condition_met ||= job.read_attribute(stream) =~ regex
  end
end
