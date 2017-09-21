require 'rails_helper'

RSpec.describe "event_actions/new", type: :view do
  before(:each) do
    assign(:event_action, EventAction.new(
      :event_receiver => nil,
      :job_type => "",
      :email_address => "MyString",
      :webhook_url => "MyString",
      :webhook_body => "MyText"
    ))
  end

  it "renders new event_action form" do
    render

    assert_select "form[action=?][method=?]", event_actions_path, "post" do

      assert_select "input#event_action_event_receiver_id[name=?]", "event_action[event_receiver_id]"

      assert_select "input#event_action_job_type[name=?]", "event_action[job_type]"

      assert_select "input#event_action_email_address[name=?]", "event_action[email_address]"

      assert_select "input#event_action_webhook_url[name=?]", "event_action[webhook_url]"

      assert_select "textarea#event_action_webhook_body[name=?]", "event_action[webhook_body]"
    end
  end
end
