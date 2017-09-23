class CreateWorkers < ActiveRecord::Migration[5.0]
  def change
    create_table :workers do |t|
      t.belongs_to :user, foreign_key: true
      t.string :address
      t.datetime :last_heartbeat

      t.timestamps
    end
  end
end
