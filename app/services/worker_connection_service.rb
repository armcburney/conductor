# frozen_string_literal: true

class WorkerConnectionService
  attr_reader :worker
  def initialize(worker)
    @worker = worker
  end

  def connect(connection)
    subscribe_to_worker_channel(connection)
  end

  private

  def subscribe_to_worker_channel(connection)
    worker&.channel&.make_private
    worker&.channel&.subscribe(connection)
  end
end
