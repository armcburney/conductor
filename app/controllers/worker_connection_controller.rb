# frozen_string_literal: true

class WorkerConnectionController < WebsocketRails::BaseController
  def connect
    Rails.logger.info "Connect to worker with id: #{message[:id]}."
    worker ? trigger_connection : trigger_failure
  end

  def healthcheck
    Rails.logger.info "Set healthcheck for worker: #{worker.&id}."
    worker.update(message.slice(*worker_healthcheck_params))
  end

  private

  def trigger_connection
    trigger_success
    send_worker_id_to_slave
    WorkerConnectionService.new(worker).connect
  end

  def send_worker_id_to_slave
    send_message :registered, { id: worker.id }, namespace: :worker
  end

  def worker_user
    @worker_user ||= User.joins(:api_keys).find_by(api_keys: { key: message["key"] })
  end

  def worker
    # Finds a worker by id, creates a new worker if it does not exist
    @worker ||= WorkerFactory.new(message["id"], worker_user).create

    # Returns nil if the worker does not belong to the current 'worker_user'
    @worker.user != worker_user ? nil : @worker
  end

  def worker_healthcheck_params
    %w(cpu_count load total_memory available_memory total_disk used_disk free_disk)
  end
end
