# frozen_string_literal: true

#
# EventAction derived class using Single Table Inheritance
#
# Public interface:
#   run!
#
class Email < EventAction
  def run!
    NotificationMailer.email(email_address, email_body).deliver
  end
end
