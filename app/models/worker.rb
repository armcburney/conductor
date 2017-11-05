# frozen_string_literal: true

class Worker < ApplicationRecord
  # Callbacks
  before_commit :update_heartbeat
  after_create :make_info_channel

  # Associations
  belongs_to :user
  has_many :jobs

  # Scopes
  default_scope { order(deleted: :asc, last_heartbeat: :desc) }
  scope :current, -> { where(deleted: false) }
  scope :active, -> { current.where("last_heartbeat > ?", 10.minutes.ago) }
  scope :assignment_order, lambda {
    active
      .joins(
        "LEFT JOIN jobs ON jobs.worker_id = workers.id "\
        "AND jobs.return_code IS NULL"
      )
      .group("workers.id")
      .order("COUNT(DISTINCT jobs.id) ASC")
  }

  def soft_delete!
    update(deleted: true)
    channel.trigger(:delete, {}, namespace: :worker)
  end

  def update_heartbeat
    update(last_heartbeat: Time.zone.now)
  end

  def healthcheck_params
    %w(cpu_count load total_memory available_memory total_disk used_disk free_disk)
  end

  def health_info
    as_json.slice("id", *healthcheck_params)
  end

  def channel
    WebsocketRails["worker.#{id}"]
  end

  def info_channel
    WebsocketRails["worker_info.#{id}"]
  end

  private

  def make_info_channel
    info_channel.make_private
  end
end
