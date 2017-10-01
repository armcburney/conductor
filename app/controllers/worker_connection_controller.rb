# frozen_string_literal: true

class WorkerConnectionController < WebsocketRails::BaseController
  def connect
    worker ? trigger_success : trigger_failure
  end

  def healthcheck
    # Update last_heartbeat
  end

  private

  def worker_user
    @worker_user ||= User.joins(:api_keys).where(api_keys: { key: message["key"] }).first
  end

  def worker
    @worker ||= Worker.find_by(address: message["address"])

    # Create if it doesn't exist
    @worker ||= worker_user.workers.create(address: message["address"])
  end
end
