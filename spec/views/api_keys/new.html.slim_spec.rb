require 'rails_helper'

RSpec.describe "api_keys/new", type: :view do
  before(:each) do
    assign(:api_key, ApiKey.new())
  end

  it "renders new api_key form" do
    render

    assert_select "form[action=?][method=?]", api_keys_path, "post" do
    end
  end
end
