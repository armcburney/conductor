module EventReceiversHelper
  def job_types
    @job_types ||= current_user.job_types
  end
end
