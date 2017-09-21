# frozen_string_literal: true

require "rails_helper"

describe JobTypesController, type: :controller do
  let(:valid_attributes) do
    skip("Add a hash of attributes valid for your model")
  end

  let(:invalid_attributes) do
    skip("Add a hash of attributes invalid for your model")
  end

  describe "GET #index" do
    it "returns a success response" do
      job_type = JobType.create! valid_attributes
      get :index, params: {}
      expect(response).to be_success
    end
  end

  describe "GET #show" do
    it "returns a success response" do
      job_type = JobType.create! valid_attributes
      get :show, params: {id: job_type.to_param}
      expect(response).to be_success
    end
  end

  describe "GET #new" do
    it "returns a success response" do
      get :new, params: {}
      expect(response).to be_success
    end
  end

  describe "GET #edit" do
    it "returns a success response" do
      job_type = JobType.create! valid_attributes
      get :edit, params: {id: job_type.to_param}
      expect(response).to be_success
    end
  end

  describe "POST #create" do
    context "with valid params" do
      it "creates a new JobType" do
        expect {
          post :create, params: {job_type: valid_attributes}
        }.to change(JobType, :count).by(1)
      end

      it "redirects to the created job_type" do
        post :create, params: {job_type: valid_attributes}
        expect(response).to redirect_to(JobType.last)
      end
    end

    context "with invalid params" do
      it "returns a success response (i.e. to display the 'new' template)" do
        post :create, params: {job_type: invalid_attributes}
        expect(response).to be_success
      end
    end
  end

  describe "PUT #update" do
    context "with valid params" do
      let(:new_attributes) {
        skip("Add a hash of attributes valid for your model")
      }

      it "updates the requested job_type" do
        job_type = JobType.create! valid_attributes
        put :update, params: {id: job_type.to_param, job_type: new_attributes}
        job_type.reload
        skip("Add assertions for updated state")
      end

      it "redirects to the job_type" do
        job_type = JobType.create! valid_attributes
        put :update, params: {id: job_type.to_param, job_type: valid_attributes}
        expect(response).to redirect_to(job_type)
      end
    end

    context "with invalid params" do
      it "returns a success response (i.e. to display the 'edit' template)" do
        job_type = JobType.create! valid_attributes
        put :update, params: {id: job_type.to_param, job_type: invalid_attributes}
        expect(response).to be_success
      end
    end
  end

  describe "DELETE #destroy" do
    it "destroys the requested job_type" do
      job_type = JobType.create! valid_attributes
      expect {
        delete :destroy, params: {id: job_type.to_param}
      }.to change(JobType, :count).by(-1)
    end

    it "redirects to the job_types list" do
      job_type = JobType.create! valid_attributes
      delete :destroy, params: {id: job_type.to_param}
      expect(response).to redirect_to(job_types_url)
    end
  end
end
