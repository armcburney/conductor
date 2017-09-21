require 'rails_helper'

RSpec.describe "workers/index", type: :view do
  before(:each) do
    assign(:workers, [
      Worker.create!(
        :user => nil,
        :address => "Address",
        :job => ""
      ),
      Worker.create!(
        :user => nil,
        :address => "Address",
        :job => ""
      )
    ])
  end

  it "renders a list of workers" do
    render
    assert_select "tr>td", :text => nil.to_s, :count => 2
    assert_select "tr>td", :text => "Address".to_s, :count => 2
    assert_select "tr>td", :text => "".to_s, :count => 2
  end
end
