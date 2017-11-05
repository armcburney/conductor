# frozen_string_literal: true

#
# EventAction derived class using Single Table Inheritance
#
# Public interface:
#   run!(user)
#
class Email < EventAction
  def run!(_user)
    ErrorMailer.email(job_type).deliver
  end
end
