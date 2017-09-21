require 'rails_helper'

RSpec.describe "event_actions/index", type: :view do
  before(:each) do
    assign(:event_actions, [
      EventAction.create!(
        :event_receiver => nil,
        :job_type => "",
        :email_address => "Email Address",
        :webhook_url => "Webhook Url",
        :webhook_body => "MyText"
      ),
      EventAction.create!(
        :event_receiver => nil,
        :job_type => "",
        :email_address => "Email Address",
        :webhook_url => "Webhook Url",
        :webhook_body => "MyText"
      )
    ])
  end

  it "renders a list of event_actions" do
    render
    assert_select "tr>td", :text => nil.to_s, :count => 2
    assert_select "tr>td", :text => "".to_s, :count => 2
    assert_select "tr>td", :text => "Email Address".to_s, :count => 2
    assert_select "tr>td", :text => "Webhook Url".to_s, :count => 2
    assert_select "tr>td", :text => "MyText".to_s, :count => 2
  end
end
