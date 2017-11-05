# frozen_string_literal: true

class EventReceiver < ApplicationRecord
  # Callbacks
  after_create :create_event_dispatcher!

  # Associations
  belongs_to :job_type, optional: true
  belongs_to :user
  has_many :event_actions
  has_many :event_dispatchers

  # Validations
  validate :owned_job_type?
  accepts_nested_attributes_for :event_actions

  def owned_job_type?
    return unless job_type && job_type.user != user
    errors.add(:job_type, "must be one of your jobs")
  end

  private

  def create_event_dispatcher!
    job_type.jobs.each do |job|
      EventDispatcher.first_or_create(event_receiver: self, job: job)
    end
  end
end
