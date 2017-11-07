# frozen_string_literal: true

class IntervalWorker
  include Sidekiq::Worker
  attr_reader :receiver

  def perform(id)
    @receiver = Receiver.find_by(id)
    return unless receiver
    receiver.event_actions.each(&:run!)
    IntervalWorker.perform_at(receiver.start_time + receiver.next_interval_time, id)
  end
end
