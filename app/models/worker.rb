# frozen_string_literal: true

class Worker < ApplicationRecord
  belongs_to :user
  has_many :jobs

  before_commit :update_heartbeat

  def update_heartbeat
    update(last_heartbeat: Time.zone.now)
  end

  def channel
    WebsocketRails["worker.#{id}"]
  end
end
