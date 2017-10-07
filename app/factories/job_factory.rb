# frozen_string_literal: true

class JobFactory
  attr_reader :id, :worker
  def initialize(id, worker)
    @id     = id
    @worker = worker
  end

  def create
    Rails.logger.info "Create new job for worker" unless id
    Rails.logger.info "worker nil" unless worker
    id ? Job.find_by(id: id) : worker&.jobs&.create!
  end
end
