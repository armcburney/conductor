json.extract! job, :id, :stdout, :stderr, :status, :return_code, :worker_id, :job_type_id, :created_at, :updated_at
json.url job_url(job, format: :json)
