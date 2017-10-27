# frozen_string_literal: true

class EventDispatcher
  attr_reader :event_receiver
  def initialize(event_receiver)
    @event_receiver = event_receiver
  end

  def batch_dipatch!
    # iterate through all the jobs of a given job type for a given
    # event_receiver, and dispatch set the triggered to 'true' for a given
    # event_record
  end
end
