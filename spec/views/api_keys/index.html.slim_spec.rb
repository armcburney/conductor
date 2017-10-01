require 'rails_helper'

RSpec.describe "api_keys/index", type: :view do
  before(:each) do
    assign(:api_keys, [
      ApiKey.create!(),
      ApiKey.create!()
    ])
  end

  it "renders a list of api_keys" do
    render
  end
end
