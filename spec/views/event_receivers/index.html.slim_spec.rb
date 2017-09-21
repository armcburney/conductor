require 'rails_helper'

RSpec.describe "event_receivers/index", type: :view do
  before(:each) do
    assign(:event_receivers, [
      EventReceiver.create!(
        :interval => 2,
        :job_type => nil,
        :action => ""
      ),
      EventReceiver.create!(
        :interval => 2,
        :job_type => nil,
        :action => ""
      )
    ])
  end

  it "renders a list of event_receivers" do
    render
    assert_select "tr>td", :text => 2.to_s, :count => 2
    assert_select "tr>td", :text => nil.to_s, :count => 2
    assert_select "tr>td", :text => "".to_s, :count => 2
  end
end
