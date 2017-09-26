class EventAction < ApplicationRecord
  belongs_to :event_receiver
  belongs_to :job_type, optional: true
  validate :has_owned_job_type

  def has_owned_job_type
    if job_type && job_type.user != event_action.user
      errors.add(:job_type, "must be one of your jobs")
    end
  end
end
