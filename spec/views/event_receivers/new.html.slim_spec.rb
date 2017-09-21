require 'rails_helper'

RSpec.describe "event_receivers/new", type: :view do
  before(:each) do
    assign(:event_receiver, EventReceiver.new(
      :interval => 1,
      :job_type => nil,
      :action => ""
    ))
  end

  it "renders new event_receiver form" do
    render

    assert_select "form[action=?][method=?]", event_receivers_path, "post" do

      assert_select "input#event_receiver_interval[name=?]", "event_receiver[interval]"

      assert_select "input#event_receiver_job_type_id[name=?]", "event_receiver[job_type_id]"

      assert_select "input#event_receiver_action[name=?]", "event_receiver[action]"
    end
  end
end
