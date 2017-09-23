class CreateJobs < ActiveRecord::Migration[5.0]
  def change
    create_table :jobs do |t|
      t.text :stdout
      t.text :stderr
      t.string :status
      t.integer :return_code
      t.belongs_to :job_type, foreign_key: true

      t.timestamps
    end
  end
end
