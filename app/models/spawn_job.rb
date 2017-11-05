# frozen_string_literal: true

#
# EventAction derived class using Single Table Inheritance
#
# Public interface:
#   run!(user)
#
class SpawnJob < EventAction
  def run!(user)
    Job.new(job_params.merge(worker: user.workers.assignment_order.first, status: "DISPATCHED"))
  end
end
