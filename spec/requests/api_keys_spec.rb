require 'rails_helper'

RSpec.describe "ApiKeys", type: :request do
  describe "GET /api_keys" do
    it "works! (now write some real specs)" do
      get api_keys_path
      expect(response).to have_http_status(200)
    end
  end
end
