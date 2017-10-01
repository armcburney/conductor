# frozen_string_literal: true

class AddWorkerHealthSpec < ActiveRecord::Migration[5.0]
  def change
    add_column :workers, :cpu_count,        :integer # NUMBER_OF_PROCESSORS,
    add_column :workers, :load,             :float   # Average number of processes in run queue
    add_column :workers, :total_memory,     :integer # Average number of processes in run queue
    add_column :workers, :available_memory, :integer # FREE RAM Bytes
    add_column :workers, :total_disk,       :integer # DISK SPACE Bytes
    add_column :workers, :used_disk,        :integer # USED SPACE Bytes
    add_column :workers, :free_disk,        :integer # FREE SPACE Bytes
  end
end
