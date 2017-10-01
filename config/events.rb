# frozen_string_literal: true

WebsocketRails::EventMap.describe do
  namespace :worker do
    %(connect healthcheck).each do |method|
      subscribe method, to: WorkerConnectionController, with_method: method
    end
  end
end
