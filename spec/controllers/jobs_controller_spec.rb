# frozen_string_literal: true

require "rails_helper"

describe JobsController, type: :controller do
  let(:valid_attributes) do
    skip("Add a hash of attributes valid for your model")
  end

  let(:invalid_attributes) do
    skip("Add a hash of attributes invalid for your model")
  end

  describe "GET #index" do
    it "returns a success response" do
      Job.create! valid_attributes
      get :index, params: {}
      expect(response).to be_success
    end
  end

  describe "GET #show" do
    it "returns a success response" do
      job = Job.create! valid_attributes
      get :show, params: {id: job.to_param}
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
      job = Job.create! valid_attributes
      get :edit, params: {id: job.to_param}
      expect(response).to be_success
    end
  end

  describe "POST #create" do
    context "with valid params" do
      it "creates a new Job" do
        expect {
          post :create, params: {job: valid_attributes}
        }.to change(Job, :count).by(1)
      end

      it "redirects to the created job" do
        post :create, params: {job: valid_attributes}
        expect(response).to redirect_to(Job.last)
      end
    end

    context "with invalid params" do
      it "returns a success response (i.e. to display the 'new' template)" do
        post :create, params: {job: invalid_attributes}
        expect(response).to be_success
      end
    end
  end

  describe "PUT #update" do
    context "with valid params" do
      let(:new_attributes) {
        skip("Add a hash of attributes valid for your model")
      }

      it "updates the requested job" do
        job = Job.create! valid_attributes
        put :update, params: {id: job.to_param, job: new_attributes}
        job.reload
        skip("Add assertions for updated state")
      end

      it "redirects to the job" do
        job = Job.create! valid_attributes
        put :update, params: {id: job.to_param, job: valid_attributes}
        expect(response).to redirect_to(job)
      end
    end

    context "with invalid params" do
      it "returns a success response (i.e. to display the 'edit' template)" do
        job = Job.create! valid_attributes
        put :update, params: {id: job.to_param, job: invalid_attributes}
        expect(response).to be_success
      end
    end
  end

  describe "DELETE #destroy" do
    it "destroys the requested job" do
      job = Job.create! valid_attributes
      expect {
        delete :destroy, params: {id: job.to_param}
      }.to change(Job, :count).by(-1)
    end

    it "redirects to the jobs list" do
      job = Job.create! valid_attributes
      delete :destroy, params: {id: job.to_param}
      expect(response).to redirect_to(jobs_url)
    end
  end
end
