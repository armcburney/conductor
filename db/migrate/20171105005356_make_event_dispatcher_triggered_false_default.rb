# frozen_string_literal: true

class MakeEventDispatcherTriggeredFalseDefault < ActiveRecord::Migration[5.0]
  def up
    change_column :event_dispatchers, :triggered, :boolean, null: false, default: false
  end

  def down
    raise ActiveRecord::IrreversibleMigration, "Can't remove the default triggered value."
  end
end
