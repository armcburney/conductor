# frozen_string_literal: true

class AddSlugToWorkers < ActiveRecord::Migration[5.0]
  def change
    add_column :workers, :slug, :string
    add_index  :workers, :slug, unique: true
  end
end
