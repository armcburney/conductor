json.extract! worker, :id, :user_id, :address, :last_heartbeat, :job, :created_at, :updated_at
json.url worker_url(worker, format: :json)
