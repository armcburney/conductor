# frozen_string_literal: true

class WorkerConnectionController < WebsocketRails::BaseController
  before_action :update_heartbeat

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

    unless @worker
      @worker = worker_user.workers.create(address: message["address"]) # Creates a new worker
      send_message :registered, { id: @worker.id }, namespace: :worker  # Sends worker id to slave
    end

    @worker
  end

  def update_heartbeat
    worker.update(last_heartbeat: Time.zone.now)
  end
end
