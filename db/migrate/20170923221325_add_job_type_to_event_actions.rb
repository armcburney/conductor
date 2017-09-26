class AddJobTypeToEventActions < ActiveRecord::Migration[5.0]
  def change
    add_reference :event_actions, :job_type, foreign_key: true
  end
end
