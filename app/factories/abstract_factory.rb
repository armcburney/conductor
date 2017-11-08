# frozen_string_literal: true

class AbstractFactory
  attr_reader :id, :user
  def initialize(id, user)
    @id   = id
    @user = user
  end

  # Pure virtual create function
  def create
    raise NotImplementedError, "AbstractFactory::create is a pure virtual method."
  end
end
