# frozen_string_literal: true

class RemoveTriggeredFromReceiver < ActiveRecord::Migration[5.0]
  def change
    remove_column :event_receivers, :triggered, :boolean
  end
end
