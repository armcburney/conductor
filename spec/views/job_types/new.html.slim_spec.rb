require 'rails_helper'

RSpec.describe "job_types/new", type: :view do
  before(:each) do
    assign(:job_type, JobType.new(
      :script => "MyText",
      :working_directory => "MyString",
      :environment_variables => "MyText",
      :timeout => 1,
      :name => "MyString",
      :user => nil
    ))
  end

  it "renders new job_type form" do
    render

    assert_select "form[action=?][method=?]", job_types_path, "post" do

      assert_select "textarea#job_type_script[name=?]", "job_type[script]"

      assert_select "input#job_type_working_directory[name=?]", "job_type[working_directory]"

      assert_select "textarea#job_type_environment_variables[name=?]", "job_type[environment_variables]"

      assert_select "input#job_type_timeout[name=?]", "job_type[timeout]"

      assert_select "input#job_type_name[name=?]", "job_type[name]"

      assert_select "input#job_type_user_id[name=?]", "job_type[user_id]"
    end
  end
end
