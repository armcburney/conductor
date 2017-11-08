json.extract! event_receiver, :id, :type, :start_time, :interval, :job_type_id, :regex, :return_code, :stream, :created_at, :updated_at
json.event_actions do
  json.array! event_receiver.event_actions, partial: 'event_actions/event_action', as: :event_action
end
