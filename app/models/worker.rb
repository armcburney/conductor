# frozen_string_literal: true

class Worker < ApplicationRecord
  # Callbacks
  before_commit :update_heartbeat

  # Associations
  belongs_to :user
  has_many :jobs

  def update_heartbeat
    update(last_heartbeat: Time.zone.now)
  end

  def channel
    WebsocketRails["worker.#{id}"]
  end
end
