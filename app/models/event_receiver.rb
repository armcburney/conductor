# frozen_string_literal: true

class EventReceiver < ApplicationRecord
  # Callbacks
  after_create :create_event_dispatcher!
  after_create :create_internal_job!

  # Associations
  belongs_to :job_type, optional: true
  belongs_to :user
  has_many :event_actions, dependent: :destroy
  has_many :event_dispatchers, dependent: :destroy

  # Validations
  validate :owned_job_type?
  accepts_nested_attributes_for :event_actions

  # Pure virtual method, overridden by derived concretions
  def trigger_condition_met?(_job)
    raise NotImplementedError, "EventReceiver::trigger_condition_met!(job) is a pure virtual method."
  end

  def owned_job_type?
    return unless job_type && job_type.user != user
    errors.add(:job_type, "must be one of your jobs")
  end

  private

  def create_event_dispatcher!
    return unless job_type

    job_type.jobs.each do |job|
      EventDispatcher.first_or_create(event_receiver: self, job: job)
    end
  end

  def create_internal_job!
    if type == "ScheduledReceiver"
      ScheduledReceiver.find(id).create_scheduled_job!
    elsif type == "IntervalReceiver"
      IntervalReceiver.find(id).create_scheduled_job!
    end
  end
end
