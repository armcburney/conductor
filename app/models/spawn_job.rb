# frozen_string_literal: true

#
# EventAction derived class using Single Table Inheritance
#
# Public interface:
#   run!
#
class SpawnJob < EventAction
  def run!
    Job.new(job_type: job_type, worker: user.workers.assignment_order.first, status: "DISPATCHED")
  end
end
