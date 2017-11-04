class ChangeHealthcheckTypes < ActiveRecord::Migration[5.0]
  def up
    change_column :workers, :total_memory, :float
    change_column :workers, :available_memory, :float
    change_column :workers, :total_disk, :float
    change_column :workers, :used_disk, :float
    change_column :workers, :free_disk, :float
  end

  def down
    change_column :workers, :total_memory, :integer
    change_column :workers, :available_memory, :integer
    change_column :workers, :total_disk, :integer
    change_column :workers, :used_disk, :integer
    change_column :workers, :free_disk, :integer
  end
end
