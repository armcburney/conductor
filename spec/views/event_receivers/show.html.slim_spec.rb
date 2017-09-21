require 'rails_helper'

RSpec.describe "event_receivers/show", type: :view do
  before(:each) do
    @event_receiver = assign(:event_receiver, EventReceiver.create!(
      :interval => 2,
      :job_type => nil,
      :action => ""
    ))
  end

  it "renders attributes in <p>" do
    render
    expect(rendered).to match(/2/)
    expect(rendered).to match(//)
    expect(rendered).to match(//)
  end
end
