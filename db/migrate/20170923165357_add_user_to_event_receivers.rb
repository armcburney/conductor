class AddUserToEventReceivers < ActiveRecord::Migration[5.0]
  def change
    add_reference :event_receivers, :user, foreign_key: true, null: false
  end
end
