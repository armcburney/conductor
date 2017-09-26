json.event_receivers do
  json.array! @event_receivers, partial: 'event_receivers/event_receiver', as: :event_receiver
end
json.job_types job_types do |job_type|
  json.id job_type.id
  json.name job_type.name
end
