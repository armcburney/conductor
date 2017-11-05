# frozen_string_literal: true

class Job < ApplicationRecord
  # Callbacks
  after_create :make_channel, :create_event_dispatcher!
  before_save :default_values, :send_email

  # Associations
  belongs_to :worker
  belongs_to :job_type
  has_one :user, through: :worker
  has_one :event_dispatcher

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
    job_type.as_json.merge(id: id, environment_variables: env_var_hash)
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

  private

  def make_channel
    channel.make_private
  end

  def default_values
    self.status ||= "UNDEFINED"
  end

  def send_email
    return unless status == "ERROR"
    ErrorMailer.email(self).deliver
  end

  def create_event_dispatcher!
    # If the event_receiver does not exist, it will be updated when the event_receiver is created
    EventDispatcher.new(event_receiver: job_type.event_receiver, job: self, triggered: false)
  end
end
