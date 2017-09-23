require 'rails_helper'

RSpec.describe "EventReceivers", type: :request do
  describe "GET /event_receivers" do
    it "works! (now write some real specs)" do
      get event_receivers_path
      expect(response).to have_http_status(200)
    end
  end
end
