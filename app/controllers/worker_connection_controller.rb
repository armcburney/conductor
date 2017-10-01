# frozen_string_literal: true

class WorkerConnectionController < WebsocketRails::BaseController
  def connect
    worker ? trigger_success : trigger_failure
  end

  def healthcheck
    worker.update(
      cpu_count:        message["cpu_count"],
      load:             message["load"],
      total_memory:     message["total_memory"],
      available_memory: message["available_memory"],
      total_disk:       message["total_disk"],
      used_disk:        message["used_disk"],
      free_disk:        message["free_disk"]
    )
  end

  private

  def worker_user
    @worker_user ||= User.joins(:api_keys).where(api_keys: { key: message["key"] }).first
  end

  def worker
    @worker ||= Worker.find_by(address: message["address"])

    # Create if it doesn't exist
    @worker ||= worker_user.workers.create(address: message["address"])

    send_message :registered, { id: @workers.id }, namespace: :worker
  end
end
