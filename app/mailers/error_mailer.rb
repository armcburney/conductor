# frozen_string_literal: true

class ErrorMailer < ApplicationMailer
  def email(job)
    @job = job
    Rails.logger.info "Sending out error email for job #{job&.id}."
    mail(to: "andrewrobertmcburney@gmail.com", subject: "Error in job execution.")
  end
end
