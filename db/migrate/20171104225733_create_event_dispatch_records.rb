# frozen_string_literal: true

class CreateEventDispatchRecords < ActiveRecord::Migration[5.0]
  def change
    create_table :event_dispatch_records do |t|
      t.boolean :triggered
      t.belongs_to :event_receiver, foreign_key: true

      t.timestamps
    end
  end
end
