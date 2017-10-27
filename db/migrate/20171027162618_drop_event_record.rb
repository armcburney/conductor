# frozen_string_literal: true

class DropEventRecord < ActiveRecord::Migration[5.0]
  def change
    drop_table :event_records
  end
end
