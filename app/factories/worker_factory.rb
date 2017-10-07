# frozen_string_literal: true

class WorkerFactory
  attr_reader :id, :user
  def initialize(id, user)
    @id   = id
    @user = user
  end

  # Modified 'find_or_create_by' method
  def create
    id ? Worker.find_by(id: id) : user&.workers&.create!
  end
end
