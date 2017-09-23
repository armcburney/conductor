class EventReceiver < ApplicationRecord
  belongs_to :job_type, optional: true
  belongs_to :user
  validate :has_owned_job_type

  def has_owned_job_type
    if job_type && job_type.user != user
      errors.add(:job_type, 'must be one of your jobs')
    end
  end
end
