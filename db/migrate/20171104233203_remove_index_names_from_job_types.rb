class RemoveIndexNamesFromJobTypes < ActiveRecord::Migration[5.0]
  def change
    remove_index :job_types, :name
  end
end
