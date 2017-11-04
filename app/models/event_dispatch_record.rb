# frozen_string_literal: true

class EventDispatchRecord < ApplicationRecord
  belongs_to :event_receiver
  validates :triggered, presence: true

  def dispatch!(job)
    # Don't perform an action if it has already been performed on the rising edge trigger
    return if triggered

    # Only perform the dispatch if the event_receiver's trigger condition has been met
    return unless event_receiver.trigger_condition_met?

    # Run each of the event actions corresponding to the job
    job.event_actions.each(&:run!)

    # Set the record to be triggered
    self.triggered = true
  end
end
