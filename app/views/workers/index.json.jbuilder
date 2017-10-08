json.workers do
  json.array! @workers, partial: 'workers/worker', as: :worker
end
json.job_types job_types do |job_type|
  json.id job_type.id
  json.name job_type.name
end
