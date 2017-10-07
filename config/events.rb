# frozen_string_literal: true

WebsocketRails::EventMap.describe do
  namespace :job do
    %i(stdout stderr return_code).each do |method|
      subscribe method, to: JobConnectionController, with_method: method
    end
  end

  namespace :worker do
    %i(connect healthcheck).each do |method|
      subscribe method, to: WorkerConnectionController, with_method: method
    end
  end
end
