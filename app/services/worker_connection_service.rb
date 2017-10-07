# frozen_string_literal: true

class WorkerConnectionService
  attr_reader :worker
  def initialize(worker)
    @worker = worker
  end

  def connect
    subscribe_to_worker_channel
  end

  private

  def subscribe_to_worker_channel
    worker&.channel&.make_private
    worker&.channel&.subscribe(connection)
  end
end
