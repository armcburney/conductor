# frozen_string_literal: true

class WorkerConnectionService
  attr_reader :worker
  def initialize(worker)
    @worker = worker
  end

  def connect(connection)
    subscribe_to_worker_channel(connection)
    worker.user.info_channel.trigger(:worker_connect, worker.as_json, namespace: :user)
    Rails.logger.info "Sent worker_connect to #{worker.user.id}"
  end

  private

  def subscribe_to_worker_channel(connection)
    worker&.channel&.make_private
    worker&.channel&.subscribe(connection)
  end
end
