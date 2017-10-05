class ChangeJobWorkerIdNotNull < ActiveRecord::Migration[5.0]
  def change
    change_column_null :jobs, :worker_id, false
    change_column_null :jobs, :job_type_id, false
  end
end
