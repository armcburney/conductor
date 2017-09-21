# frozen_string_literal: true

require "rails_helper"

describe EventActionsController, type: :controller do
  let(:valid_attributes) do
    skip("Add a hash of attributes valid for your model")
  end

  let(:invalid_attributes) do
    skip("Add a hash of attributes invalid for your model")
  end

  describe "GET #index" do
    it "returns a success response" do
      EventAction.create! valid_attributes
      get :index, params: {}
      expect(response).to be_success
    end
  end

  describe "GET #show" do
    it "returns a success response" do
      event_action = EventAction.create! valid_attributes
      get :show, params: {id: event_action.to_param}
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
      event_action = EventAction.create! valid_attributes
      get :edit, params: {id: event_action.to_param}
      expect(response).to be_success
    end
  end

  describe "POST #create" do
    context "with valid params" do
      it "creates a new EventAction" do
        expect {
          post :create, params: {event_action: valid_attributes}
        }.to change(EventAction, :count).by(1)
      end

      it "redirects to the created event_action" do
        post :create, params: {event_action: valid_attributes}
        expect(response).to redirect_to(EventAction.last)
      end
    end

    context "with invalid params" do
      it "returns a success response (i.e. to display the 'new' template)" do
        post :create, params: {event_action: invalid_attributes}
        expect(response).to be_success
      end
    end
  end

  describe "PUT #update" do
    context "with valid params" do
      let(:new_attributes) {
        skip("Add a hash of attributes valid for your model")
      }

      it "updates the requested event_action" do
        event_action = EventAction.create! valid_attributes
        put :update, params: {id: event_action.to_param, event_action: new_attributes}
        event_action.reload
        skip("Add assertions for updated state")
      end

      it "redirects to the event_action" do
        event_action = EventAction.create! valid_attributes
        put :update, params: {id: event_action.to_param, event_action: valid_attributes}
        expect(response).to redirect_to(event_action)
      end
    end

    context "with invalid params" do
      it "returns a success response (i.e. to display the 'edit' template)" do
        event_action = EventAction.create! valid_attributes
        put :update, params: {id: event_action.to_param, event_action: invalid_attributes}
        expect(response).to be_success
      end
    end
  end

  describe "DELETE #destroy" do
    it "destroys the requested event_action" do
      event_action = EventAction.create! valid_attributes
      expect {
        delete :destroy, params: {id: event_action.to_param}
      }.to change(EventAction, :count).by(-1)
    end

    it "redirects to the event_actions list" do
      event_action = EventAction.create! valid_attributes
      delete :destroy, params: {id: event_action.to_param}
      expect(response).to redirect_to(event_actions_url)
    end
  end
end
