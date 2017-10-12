# frozen_string_literal: true

class WebsocketAuthenticationController < WebsocketRails::BaseController
  def authorize_channels
    if message[:channel].start_with?("job")
      authorize_job
    elsif message[:channel].start_with?("worker_info")
      authorize_worker_info
    else
      deny_channel
    end
  end

  private

  def authorize_job
    match = /^job\.(?<id>\w+)$/.match(message[:channel])
    return deny_channel unless match

    job = Job.find_by(id: match[:id].to_i)
    if job && current_user && job.user == current_user
      accept_channel job.as_json
    else
      deny_channel
    end
  end

  def authorize_worker_info
    Rails.logger.info("Authorizing worker info")
    match = /^worker_info\.(?<id>\w+)$/.match(message[:channel])
    Rails.logger.info(match.inspect)
    return deny_channel unless match

    worker = Worker.find_by(id: match[:id].to_i)
    if worker && current_user && worker.user == current_user
      accept_channel
    else
      deny_channel
    end
  end
end
