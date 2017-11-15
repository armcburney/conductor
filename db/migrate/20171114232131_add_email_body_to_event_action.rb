class AddEmailBodyToEventAction < ActiveRecord::Migration[5.0]
  def change
    add_column :event_actions, :email_body, :text
  end
end
