class AddJobToEventDispatcher < ActiveRecord::Migration[5.0]
  def change
    add_reference :event_dispatchers, :job, index: true, null: false
    change_column :event_dispatchers, :event_receiver_id, :integer, null: false
  end
end
