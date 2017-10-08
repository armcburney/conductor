json.workers do
  json.array! @workers, partial: 'workers/worker', as: :worker
end
json.job_types job_types do |job_type|
  json.id job_type.id
  json.name job_type.name
end
#json.job_types do
  #json.array! job_types, partial: 'job_types/job_type', as: :job_type
#end
