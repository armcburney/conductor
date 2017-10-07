class Job < ApplicationRecord
  belongs_to :worker
  belongs_to :job_type

  def request_json
    # Send the id of the current job, plus the information from the job type
    # needed to be able to spawn the job
    job_type.as_json.merge(id: id)
  end
end
