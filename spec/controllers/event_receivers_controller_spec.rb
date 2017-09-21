# frozen_string_literal: true

require "rails_helper"

describe EventReceiversController, type: :controller do
  let(:valid_attributes) do
    skip("Add a hash of attributes valid for your model")
  end

  let(:invalid_attributes) do
    skip("Add a hash of attributes invalid for your model")
  end

  describe "GET #index" do
    it "returns a success response" do
      EventReceiver.create! valid_attributes
      get :index, params: {}
      expect(response).to be_success
    end
  end

  describe "GET #show" do
    it "returns a success response" do
      EventReceiver.create! valid_attributes
      get :show, params: { id: event_receiver.to_param }
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
      event_receiver = EventReceiver.create! valid_attributes
      get :edit, params: {id: event_receiver.to_param}
      expect(response).to be_success
    end
  end

  describe "POST #create" do
    context "with valid params" do
      it "creates a new EventReceiver" do
        expect {
          post :create, params: {event_receiver: valid_attributes}
        }.to change(EventReceiver, :count).by(1)
      end

      it "redirects to the created event_receiver" do
        post :create, params: {event_receiver: valid_attributes}
        expect(response).to redirect_to(EventReceiver.last)
      end
    end

    context "with invalid params" do
      it "returns a success response (i.e. to display the 'new' template)" do
        post :create, params: {event_receiver: invalid_attributes}
        expect(response).to be_success
      end
    end
  end

  describe "PUT #update" do
    context "with valid params" do
      let(:new_attributes) {
        skip("Add a hash of attributes valid for your model")
      }

      it "updates the requested event_receiver" do
        event_receiver = EventReceiver.create! valid_attributes
        put :update, params: {id: event_receiver.to_param, event_receiver: new_attributes}
        event_receiver.reload
        skip("Add assertions for updated state")
      end

      it "redirects to the event_receiver" do
        event_receiver = EventReceiver.create! valid_attributes
        put :update, params: {id: event_receiver.to_param, event_receiver: valid_attributes}
        expect(response).to redirect_to(event_receiver)
      end
    end

    context "with invalid params" do
      it "returns a success response (i.e. to display the 'edit' template)" do
        event_receiver = EventReceiver.create! valid_attributes
        put :update, params: {id: event_receiver.to_param, event_receiver: invalid_attributes}
        expect(response).to be_success
      end
    end
  end

  describe "DELETE #destroy" do
    it "destroys the requested event_receiver" do
      event_receiver = EventReceiver.create! valid_attributes
      expect {
        delete :destroy, params: {id: event_receiver.to_param}
      }.to change(EventReceiver, :count).by(-1)
    end

    it "redirects to the event_receivers list" do
      event_receiver = EventReceiver.create! valid_attributes
      delete :destroy, params: {id: event_receiver.to_param}
      expect(response).to redirect_to(event_receivers_url)
    end
  end
end
