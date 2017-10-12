# frozen_string_literal: true

class AddTypeColumnForEventActions < ActiveRecord::Migration[5.0]
  def change
    add_column :event_actions, :type, :string, null: false, limit: 20
  end
end
