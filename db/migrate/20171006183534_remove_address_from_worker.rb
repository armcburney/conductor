class RemoveAddressFromWorker < ActiveRecord::Migration[5.0]
  def change
    change_column_null :workers, :user_id, false
    remove_column :workers, :address
  end
end
