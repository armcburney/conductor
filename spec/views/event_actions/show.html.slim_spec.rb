require 'rails_helper'

RSpec.describe "event_actions/show", type: :view do
  before(:each) do
    @event_action = assign(:event_action, EventAction.create!(
      :event_receiver => nil,
      :job_type => "",
      :email_address => "Email Address",
      :webhook_url => "Webhook Url",
      :webhook_body => "MyText"
    ))
  end

  it "renders attributes in <p>" do
    render
    expect(rendered).to match(//)
    expect(rendered).to match(//)
    expect(rendered).to match(/Email Address/)
    expect(rendered).to match(/Webhook Url/)
    expect(rendered).to match(/MyText/)
  end
end
