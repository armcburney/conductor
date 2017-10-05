class AddWorkerToJobs < ActiveRecord::Migration[5.0]
  def change
    add_reference :jobs, :worker, foreign_key: true
  end
end
