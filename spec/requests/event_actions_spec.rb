require 'rails_helper'

RSpec.describe "EventActions", type: :request do
  describe "GET /event_actions" do
    it "works! (now write some real specs)" do
      get event_actions_path
      expect(response).to have_http_status(200)
    end
  end
end
