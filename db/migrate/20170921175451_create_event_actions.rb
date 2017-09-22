class CreateEventActions < ActiveRecord::Migration[5.0]
  def change
    create_table :event_actions do |t|
      t.belongs_to :event_receiver, foreign_key: true
      # add has_one job type
      t.string :email_address
      t.string :webhook_url
      t.text :webhook_body

      t.timestamps
    end
  end
end
