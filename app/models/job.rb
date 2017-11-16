# frozen_string_literal: true

class Job < ApplicationRecord
  # Callbacks
  after_create :make_channel, :create_event_dispatchers!, :update_channels
  before_save :default_values

  # Associations
  belongs_to :worker
  belongs_to :job_type
  has_one :user, through: :worker
  has_many :event_dispatchers, dependent: :destroy

  # Validations
  validates :status, inclusion: { in: %w(DISPATCHED UNDEFINED ERROR NORMAL\ EXECUTION) }

  # Scopes
  default_scope { order("(return_code IS NULL) ASC, created_at DESC") }

  def channel
    WebsocketRails["job.#{id}"]
  end

  def request_json
    # Send the id of the current job, plus the information from the job type
    # needed to be able to spawn the job
    job_type.as_json.merge(id: id, worker_id: worker_id, job_type_id: job_type_id, environment_variables: env_var_hash)
  end

  def env_var_hash
    return JSON.parse(job_type.environment_variables)
  rescue
    Rails.logger.info "Invalid json: #{job_type.environment_variables}"
    return {}
  end

  def append_to_column(column, chunk)
    quoted_chunk = ActiveRecord::Base.connection.quote(chunk)
    quoted_id = ActiveRecord::Base.connection.quote(id)
    ActiveRecord::Base.connection.execute(<<~SQL)
      UPDATE jobs
      SET #{column} = (
        CASE WHEN #{column} IS NULL THEN #{quoted_chunk}
        ELSE #{column} || #{quoted_chunk} END
      )
      WHERE id = #{quoted_id}
    SQL
  end


  def make_channel
    channel.make_private
  end

  def default_values
    self.status ||= "UNDEFINED"
  end

  def update_channels
    Rails.logger.info "Sending channel updates for job #{id}"
    worker.channel.trigger(:spawn, request_json, namespace: :worker)
    worker.info_channel.trigger(:spawn, request_json, namespace: :worker_info)
  end

  def create_event_dispatchers!
    # If the event_receiver does not exist, it will be updated when the event_receiver is created
    job_type.event_receivers.each do |receiver|
      event_dispatchers.create(event_receiver: receiver)
    end
  end
end
