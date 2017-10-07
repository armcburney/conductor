# frozen_string_literal: true

class WorkerConnectionController < WebsocketRails::BaseController
  def connect
    worker ? trigger_connection : trigger_failure
  end

  def healthcheck
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
    @worker_user ||= User.joins(:api_keys).where(api_keys: { key: message["key"] }).first
  end

  def worker
    return nil if @worker && @worker&.user != user
    @worker ? @worker : WorkerFactory.new(message["id"], worker_user).create
  end

  def worker_healthcheck_params
    %w(cpu_count load total_memory available_memory total_disk used_disk free_disk)
  end
end
