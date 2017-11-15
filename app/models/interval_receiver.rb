# frozen_string_literal: true

class IntervalReceiver < EventReceiver
  # Validations
  validates :start_time, :interval, presence: true

  # Sidekiq job scheduled after_create => trigger condition will always be met
  def trigger_condition_met?(_job)
    true
  end

  def next_interval_time
    return 0.seconds if start_time.future?
    (((Time.zone.now - start_time) / interval).ceil * interval).seconds
  end

  def create_internal_job!
    Rails.logger.info "Scheduling at #{(start_time + next_interval_time).inspect}"
    IntervalWorker.perform_at(start_time + next_interval_time, id)
  end
end
