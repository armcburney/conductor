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
    job.update(status: status)
  end

  private

  def status
    case return_code
    when ERROR_CODE
      "ERROR"
    when NORMAL_CODE
      "NORMAL EXECUTION"
    end
  end
end
