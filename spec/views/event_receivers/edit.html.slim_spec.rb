require 'rails_helper'

RSpec.describe "event_receivers/edit", type: :view do
  before(:each) do
    @event_receiver = assign(:event_receiver, EventReceiver.create!(
      :interval => 1,
      :job_type => nil,
      :action => ""
    ))
  end

  it "renders the edit event_receiver form" do
    render

    assert_select "form[action=?][method=?]", event_receiver_path(@event_receiver), "post" do

      assert_select "input#event_receiver_interval[name=?]", "event_receiver[interval]"

      assert_select "input#event_receiver_job_type_id[name=?]", "event_receiver[job_type_id]"

      assert_select "input#event_receiver_action[name=?]", "event_receiver[action]"
    end
  end
end
