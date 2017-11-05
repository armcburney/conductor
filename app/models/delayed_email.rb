# frozen_string_literal: true

#
# EventAction derived class using Single Table Inheritance
#
# Public interface:
#   run!(user)
#
class DelayedEmail < EventAction
  def run!(_user)
    MailWorker.perform_in(3.hours, job_type)
  end
end
