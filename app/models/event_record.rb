# frozen_string_literal: true

class EventRecord < ApplicationRecord
  # Associations
  belongs_to :event_receiver
  has_many   :jobs

  # Validations
  validates :job_id, presence: true

  def trigger!
    self.triggered = true
  end

  def triggered?
    triggered
  end
end
