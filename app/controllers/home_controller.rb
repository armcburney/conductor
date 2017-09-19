# frozen_string_literal: true

class HomeController < ApplicationController
  def index
    BaseWorker.perform_async("Test this out.")
  end
end
