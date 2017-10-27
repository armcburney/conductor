# frozen_string_literal: true

class AddDataForEventReceivers < ActiveRecord::Migration[5.0]
  def change
    add_column :event_receivers, :type, :string, null: false # type for STI
    add_column :event_receivers, :regex, :text
    add_column :event_receivers, :stream, :text
    add_column :event_receivers, :return_code, :integer
  end
end
