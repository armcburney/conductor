# frozen_string_literal: true

class ReturnCodeReceiver < EventReceiver
  validates :return_code, presence: true

  def trigger_condition_met?(job)
    @trigger_condition_met ||= job.return_code == return_code
  end
end
