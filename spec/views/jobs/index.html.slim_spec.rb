require 'rails_helper'

RSpec.describe "jobs/index", type: :view do
  before(:each) do
    assign(:jobs, [
      Job.create!(
        :stdout => "MyText",
        :stderr => "MyText",
        :status => "Status",
        :return_code => 2,
        :worker => nil,
        :job_type => nil
      ),
      Job.create!(
        :stdout => "MyText",
        :stderr => "MyText",
        :status => "Status",
        :return_code => 2,
        :worker => nil,
        :job_type => nil
      )
    ])
  end

  it "renders a list of jobs" do
    render
    assert_select "tr>td", :text => "MyText".to_s, :count => 2
    assert_select "tr>td", :text => "MyText".to_s, :count => 2
    assert_select "tr>td", :text => "Status".to_s, :count => 2
    assert_select "tr>td", :text => 2.to_s, :count => 2
    assert_select "tr>td", :text => nil.to_s, :count => 2
    assert_select "tr>td", :text => nil.to_s, :count => 2
  end
end
