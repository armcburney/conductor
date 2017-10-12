# frozen_string_literal: true

class JobConnectionController < WebsocketRails::BaseController
  def stdout
    Rails.logger.info "Updated stdout for #{message['id']}, with stdout: #{message['stdout']}."
    job&.append_to_column("stdout", message["stdout"])
    job&.channel&.trigger(:stdout, message["stdout"], namespace: :job)
  end

  def stderr
    Rails.logger.info "Updated stderr for #{message['id']}, with stderr: #{message['stderr']}."
    job&.append_to_column("stderr", message["stderr"])
    job&.channel&.trigger(:stderr, message["stderr"], namespace: :job)
  end

  def return_code
    Rails.logger.info "Updated return code for #{message['id']}, with return code #{message['return_code']}."
    job&.update(message.slice("return_code"))
    job&.channel&.trigger(:return_code, message["return_code"], namespace: :job)
    JobStatusSetter.new(job, message["return_code"]).update
  end

  private

  def job
    @job ||= Job.find_by(id: message["id"])

    # Triggers failure if it can't find the job
    @job ? @job : trigger_failure
  end
end
