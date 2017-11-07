# frozen_string_literal: true

class IntervalWorker
  include Sidekiq::Worker
  attr_reader :receiver

  def perform(id)
    @receiver = Receiver.find_by(id)
    return unless receiver
    receiver.event_actions.each(&:run!)
    IntervalWorker.perform_at(start_time + (n * interval.seconds), id)
  end

  private

  def n
    ((Time.zone.now.to_i - start_time) / interval).ceil
  end
end
