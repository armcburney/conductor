# frozen_string_literal: true

#
# EventAction derived class using Single Table Inheritance
#
# Public interface:
#   run!
#
class DelayedEmail < EventAction
  def run!
    MailWorker.perform_in(3.hours, job_type)
  end
end
