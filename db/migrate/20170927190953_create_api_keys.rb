class CreateApiKeys < ActiveRecord::Migration[5.0]
  def change
    create_table :api_keys do |t|
      t.string :key, null: false
      t.references :user, foreign_key: true
      t.string :name, null: false

      t.timestamps
    end
    add_index :api_keys, :key, unique: true
  end
end
