# frozen_string_literal: true

class WebsocketAuthenticationController < WebsocketRails::BaseController
  def authorize_channels
    if message[:channel].start_with?("job")
      authorize_job
    elsif message[:channel].start_with?("worker_info")
      authorize_worker_info
    elsif message[:channel].start_with?("user")
      authorize_user_channel
    else
      deny_channel
    end
  end

  private

  def authorize_job
    authorize_by_id("job", Job)
  end

  def authorize_worker_info
    authorize_by_id("worker_info", Worker)
  end

  def authorize_user_channel
    match = /^user\.(?<id>\w+)$/.match(message[:channel])
    return deny_channel unless match
    instance = User.find_by(id: match[:id].to_i)
    if instance == current_user
      accept_channel
    else
      deny_channel
    end
  end

  def authorize_by_id(channel_prefix, klass)
    match = /^#{channel_prefix}\.(?<id>\w+)$/.match(message[:channel])
    return deny_channel unless match

    instance = klass.find_by(id: match[:id].to_i)
    if instance && current_user && instance.user == current_user
      accept_channel instance.as_json
    else
      deny_channel
    end
  end
end
