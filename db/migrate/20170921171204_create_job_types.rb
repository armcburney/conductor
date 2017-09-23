class CreateJobTypes < ActiveRecord::Migration[5.0]
  def change
    create_table :job_types do |t|
      t.text :script
      t.string :working_directory
      t.text :environment_variables
      t.integer :timeout
      t.string :name
      t.belongs_to :user, foreign_key: true

      t.timestamps
    end
    add_index :job_types, :name, unique: true
  end
end
