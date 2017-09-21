json.extract! job_type, :id, :script, :working_directory, :environment_variables, :timeout, :name, :user_id, :created_at, :updated_at
json.url job_type_url(job_type, format: :json)
