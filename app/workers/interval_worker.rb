# frozen_string_literal: true

class IntervalWorker
  include Sidekiq::Worker
  attr_reader :receiver

  def perform(id)
    @receiver = Receiver.find_by(id)
    return unless receiver
    dispatch_events
    IntervalWorker.perform_at(start_time + (n * interval.seconds), id)
  end

  private

  def dispatch_events
    receiver.event_dispatches.each do |dispatcher|
      dispatcher.dispatch!(receiver.user)
      dispatcher.reset_trigger!
    end
  end

  def n
    ((Time.zone.now.to_i - start_time) / interval).ceil
  end
end
