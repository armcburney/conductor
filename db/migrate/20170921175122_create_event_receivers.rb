class CreateEventReceivers < ActiveRecord::Migration[5.0]
  def change
    create_table :event_receivers do |t|
      t.datetime :start_time
      t.integer :interval
      t.belongs_to :job_type, foreign_key: true

      t.timestamps
    end
  end
end
