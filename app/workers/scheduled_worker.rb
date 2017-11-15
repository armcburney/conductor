# frozen_string_literal: true

class ScheduledWorker
  include Sidekiq::Worker
  attr_reader :receiver

  def perform(id)
    @receiver = EventReceiver.find_by(id: id)
    return unless receiver
    receiver.event_actions.each(&:run!)
  end
end
