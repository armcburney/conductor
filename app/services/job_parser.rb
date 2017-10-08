# frozen_string_literal: true

# Updates internal status of job based on return code
class JobStatusSetter
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
    when -1
      "ERROR"
    when 0
      "NORMAL EXECUTION"
    end
  end
end
