# frozen_string_literal: true

class AddTriggeredToEventReceiver < ActiveRecord::Migration[5.0]
  def change
    add_column :event_receivers, :triggered, :boolean, null: false, default: false
  end
end
