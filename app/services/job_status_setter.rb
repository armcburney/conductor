# frozen_string_literal: true

# Updates internal status of job based on return code
class JobStatusSetter
  include StatusCodeHelpers

  attr_reader :job, :return_code
  def initialize(job, return_code)
    @job         = job
    @return_code = return_code
  end

  def update
    Rails.logger.info "Set the job status to #{status}."
    job.update(status: status)
  end

  private

  def status
    @status ||= begin
      case return_code
      when ERROR_CODE  then "ERROR"
      when NORMAL_CODE then "NORMAL EXECUTION"
      else
        "UNDEFINED"
      end
    end
  end
end
