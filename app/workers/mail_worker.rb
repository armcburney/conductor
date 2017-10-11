# frozen_string_literal: true

class MailWorker
  include Sidekiq::Worker

  def perform(job_type)
    Rails.logger.info "Queuing up error email for job_type #{job_type&.id}."
    ErrorMailer.email(job_type).deliver
  end
end
