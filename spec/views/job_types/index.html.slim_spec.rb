require 'rails_helper'

RSpec.describe "job_types/index", type: :view do
  before(:each) do
    assign(:job_types, [
      JobType.create!(
        :script => "MyText",
        :working_directory => "Working Directory",
        :environment_variables => "MyText",
        :timeout => 2,
        :name => "Name",
        :user => nil
      ),
      JobType.create!(
        :script => "MyText",
        :working_directory => "Working Directory",
        :environment_variables => "MyText",
        :timeout => 2,
        :name => "Name",
        :user => nil
      )
    ])
  end

  it "renders a list of job_types" do
    render
    assert_select "tr>td", :text => "MyText".to_s, :count => 2
    assert_select "tr>td", :text => "Working Directory".to_s, :count => 2
    assert_select "tr>td", :text => "MyText".to_s, :count => 2
    assert_select "tr>td", :text => 2.to_s, :count => 2
    assert_select "tr>td", :text => "Name".to_s, :count => 2
    assert_select "tr>td", :text => nil.to_s, :count => 2
  end
end
