# frozen_string_literal: true

class NotificationMailer < ApplicationMailer
  def email(address, body)
    Rails.logger.info "Sending email to #{address}: #{body}"
    mail(
      to: address,
      subject: "Message from a Conductor job",
      body: body
    )
  end
end
