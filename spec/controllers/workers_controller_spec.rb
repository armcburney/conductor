# frozen_string_literal: true

require "rails_helper"

describe WorkersController, type: :controller do
  let(:valid_attributes) do
    skip("Add a hash of attributes valid for your model")
  end

  let(:invalid_attributes) do
    skip("Add a hash of attributes invalid for your model")
  end

  describe "GET #index" do
    it "returns a success response" do
      Worker.create! valid_attributes
      get :index, params: {}
      expect(response).to be_success
    end
  end

  describe "GET #show" do
    it "returns a success response" do
      Worker.create! valid_attributes
      get :show, params: {id: worker.to_param}
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
      worker = Worker.create! valid_attributes
      get :edit, params: {id: worker.to_param}
      expect(response).to be_success
    end
  end

  describe "POST #create" do
    context "with valid params" do
      it "creates a new Worker" do
        expect {
          post :create, params: {worker: valid_attributes}
        }.to change(Worker, :count).by(1)
      end

      it "redirects to the created worker" do
        post :create, params: {worker: valid_attributes}
        expect(response).to redirect_to(Worker.last)
      end
    end

    context "with invalid params" do
      it "returns a success response (i.e. to display the 'new' template)" do
        post :create, params: {worker: invalid_attributes}
        expect(response).to be_success
      end
    end
  end

  describe "PUT #update" do
    context "with valid params" do
      let(:new_attributes) {
        skip("Add a hash of attributes valid for your model")
      }

      it "updates the requested worker" do
        worker = Worker.create! valid_attributes
        put :update, params: {id: worker.to_param, worker: new_attributes}
        worker.reload
        skip("Add assertions for updated state")
      end

      it "redirects to the worker" do
        worker = Worker.create! valid_attributes
        put :update, params: {id: worker.to_param, worker: valid_attributes}
        expect(response).to redirect_to(worker)
      end
    end

    context "with invalid params" do
      it "returns a success response (i.e. to display the 'edit' template)" do
        worker = Worker.create! valid_attributes
        put :update, params: {id: worker.to_param, worker: invalid_attributes}
        expect(response).to be_success
      end
    end
  end

  describe "DELETE #destroy" do
    it "destroys the requested worker" do
      worker = Worker.create! valid_attributes
      expect {
        delete :destroy, params: {id: worker.to_param}
      }.to change(Worker, :count).by(-1)
    end

    it "redirects to the workers list" do
      worker = Worker.create! valid_attributes
      delete :destroy, params: {id: worker.to_param}
      expect(response).to redirect_to(workers_url)
    end
  end
end
