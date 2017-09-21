require 'rails_helper'

RSpec.describe "job_types/show", type: :view do
  before(:each) do
    @job_type = assign(:job_type, JobType.create!(
      :script => "MyText",
      :working_directory => "Working Directory",
      :environment_variables => "MyText",
      :timeout => 2,
      :name => "Name",
      :user => nil
    ))
  end

  it "renders attributes in <p>" do
    render
    expect(rendered).to match(/MyText/)
    expect(rendered).to match(/Working Directory/)
    expect(rendered).to match(/MyText/)
    expect(rendered).to match(/2/)
    expect(rendered).to match(/Name/)
    expect(rendered).to match(//)
  end
end
