# frozen_string_literal: true

class WorkerConnectionController < WebsocketRails::BaseController
  def connect
    if worker
      trigger_success
      send_message :registered, { id: worker.id }, namespace: :worker  # Sends worker id to slave
      worker.channel.subscribe(connection)
    else
      trigger_failure
    end
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
    return @worker if @worker

    if message["id"]
      @worker = Worker.find_by(id: message["id"])
      verify_worker_key!
    else
      @worker = worker_user&.workers&.create! # Creates a new worker
    end

    @worker
  end

  def verify_worker_key!
    @worker = nil unless worker&.user == worker_user
  end
end
