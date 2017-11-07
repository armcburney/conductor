# frozen_string_literal: true

class ScheduledReceiver < EventReceiver
  # Callbacks
  after_create :create_scheduled_job!

  # Validations
  validates :start_time, presence: true

  # Sidekiq job scheduled after_create => trigger condition will always be met
  def trigger_condition_met?(_job)
    true
  end

  private

  def create_scheduled_job!
    ScheduledWorker.perform_at(Worker::RETRY_TIME.from_now, id)
  end
end
