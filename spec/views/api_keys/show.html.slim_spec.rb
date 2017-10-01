require 'rails_helper'

RSpec.describe "api_keys/show", type: :view do
  before(:each) do
    @api_key = assign(:api_key, ApiKey.create!())
  end

  it "renders attributes in <p>" do
    render
  end
end
