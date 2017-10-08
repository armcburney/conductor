# frozen_string_literal: true

class Job < ApplicationRecord
  # Callbacks
  after_create :make_channel
  before_save :default_values, :send_email

  # Associations
  belongs_to :worker
  belongs_to :job_type
  has_one :user, through: :worker

  # Validations
  validates :status, inclusion: { in: %w(UNDEFINED ERROR NORMAL\ EXECUTION) }

  def channel
    WebsocketRails["job.#{id}"]
  end

  def make_channel
    channel.make_private
  end

  def request_json
    # Send the id of the current job, plus the information from the job type
    # needed to be able to spawn the job
    job_type.as_json.merge(id: id)
  end

  private

  def default_values
    self.status ||= "UNDEFINED"
  end

  def send_email
    return unless status == "ERROR"
    ErrorMailer.email(self).deliver
  end
end
