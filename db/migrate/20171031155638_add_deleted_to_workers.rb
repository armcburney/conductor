# frozen_string_literal: true

class AddDeletedToWorkers < ActiveRecord::Migration[5.0]
  def change
    add_column :workers, :deleted, :boolean, null: false, default: false
  end
end
