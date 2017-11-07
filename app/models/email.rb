# frozen_string_literal: true

#
# EventAction derived class using Single Table Inheritance
#
# Public interface:
#   run!
#
class Email < EventAction
  def run!
    ErrorMailer.email(job_type).deliver
  end
end
