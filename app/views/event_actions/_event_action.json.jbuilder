json.extract! event_action, :id, :event_receiver_id, :job_type, :email_address, :webhook_url, :webhook_body, :created_at, :updated_at
json.url event_action_url(event_action, format: :json)
