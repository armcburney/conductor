require 'rails_helper'

RSpec.describe "api_keys/edit", type: :view do
  before(:each) do
    @api_key = assign(:api_key, ApiKey.create!())
  end

  it "renders the edit api_key form" do
    render

    assert_select "form[action=?][method=?]", api_key_path(@api_key), "post" do
    end
  end
end
