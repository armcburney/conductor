# frozen_string_literal: true

class CreateEventRecords < ActiveRecord::Migration[5.0]
  def change
    create_table :event_records do |t|
      t.references :event_receiver, foreign_key: true
      t.boolean :triggered

      t.timestamps
    end
  end
end
