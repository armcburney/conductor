# frozen_string_literal: true

class InternalWorker
  include Sidekiq::Worker
  attr_reader :receiver

  def perform(id)
    @receiver = Receiver.find_by(id)
    return unless receiver
    dispatch_events
    InternalWorker.perform_at(receiver.interval.from_now, id)
  end

  private

  def dispatch_events
    receiver.event_dispatches.each do |dispatcher|
      dispatcher.dispatch!(receiver.user)
      dispatcher.reset_trigger!
    end
  end
end
