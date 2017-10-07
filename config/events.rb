# frozen_string_literal: true

WebsocketRails::EventMap.describe do
  namespace :worker do
    %i(connect healthcheck stdout stderr returncode).each do |method|
      subscribe method, to: WorkerConnectionController, with_method: method
    end
  end
end
