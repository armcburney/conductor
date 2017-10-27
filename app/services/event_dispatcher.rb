# frozen_string_literal: true

class EventDispatcher
  attr_reader :event_receivers
  def initialize(event_receivers)
    @event_receivers = event_receivers
  end

  def batch_dipatch!
    event_receivers.each(&:dispatch!)
  end
end
