# frozen_string_literal: true

class BaseWorker
  include Sidekiq::Worker

  def perform(message)
    3.times do
      puts "Hello from BaseWorker! #{message}"
      sleep 2
    end
  end
end
