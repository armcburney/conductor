class Job < ApplicationRecord
  belongs_to :worker
  belongs_to :job_type
end
