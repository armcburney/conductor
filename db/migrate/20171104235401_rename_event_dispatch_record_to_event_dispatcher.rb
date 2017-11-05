# frozen_string_literal: true

class RenameEventDispatchRecordToEventDispatcher < ActiveRecord::Migration[5.0]
  def change
    rename_table :event_dispatch_records, :event_dispatchers
  end
end
