# frozen_string_literal: true

class JobConnectionController < WebsocketRails::BaseController
  def stdout
    Rails.logger.info "Updated stdout for #{message['id']}, with stdout: #{message['stdout']}."
    job&.update(message.slice("stdout"))
  end

  def stderr
    Rails.logger.info "Updated stderr for #{message['id']}, with stderr: #{message['stderr']}."
    job&.update(message.slice("stderr"))
  end

  def return_code
    Rails.logger.info "Updated return code for #{message['id']}, with return code #{message['return_code']}."
    job&.update(message.slice("return_code"))
  end

  private

  def job
    @job ||= Job.find_by(id: message["id"])

    # Triggers failure if it can't find the job
    @job ? @job : trigger_failure
  end
end
