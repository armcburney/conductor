# frozen_string_literal: true

class EventReceiver < ApplicationRecord
  belongs_to :job_type, optional: true
  belongs_to :user
  has_many :event_actions
  validate :owned_job_type?

  def owned_job_type?
    return unless job_type && job_type.user != user
    errors.add(:job_type, "must be one of your jobs")
  end
end
