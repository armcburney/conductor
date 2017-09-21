require 'rails_helper'

RSpec.describe "jobs/edit", type: :view do
  before(:each) do
    @job = assign(:job, Job.create!(
      :stdout => "MyText",
      :stderr => "MyText",
      :status => "MyString",
      :return_code => 1,
      :worker => nil,
      :job_type => nil
    ))
  end

  it "renders the edit job form" do
    render

    assert_select "form[action=?][method=?]", job_path(@job), "post" do

      assert_select "textarea#job_stdout[name=?]", "job[stdout]"

      assert_select "textarea#job_stderr[name=?]", "job[stderr]"

      assert_select "input#job_status[name=?]", "job[status]"

      assert_select "input#job_return_code[name=?]", "job[return_code]"

      assert_select "input#job_worker_id[name=?]", "job[worker_id]"

      assert_select "input#job_job_type_id[name=?]", "job[job_type_id]"
    end
  end
end
