require "rails_helper"

RSpec.describe EventActionsController, type: :routing do
  describe "routing" do

    it "routes to #index" do
      expect(:get => "/event_actions").to route_to("event_actions#index")
    end

    it "routes to #new" do
      expect(:get => "/event_actions/new").to route_to("event_actions#new")
    end

    it "routes to #show" do
      expect(:get => "/event_actions/1").to route_to("event_actions#show", :id => "1")
    end

    it "routes to #edit" do
      expect(:get => "/event_actions/1/edit").to route_to("event_actions#edit", :id => "1")
    end

    it "routes to #create" do
      expect(:post => "/event_actions").to route_to("event_actions#create")
    end

    it "routes to #update via PUT" do
      expect(:put => "/event_actions/1").to route_to("event_actions#update", :id => "1")
    end

    it "routes to #update via PATCH" do
      expect(:patch => "/event_actions/1").to route_to("event_actions#update", :id => "1")
    end

    it "routes to #destroy" do
      expect(:delete => "/event_actions/1").to route_to("event_actions#destroy", :id => "1")
    end

  end
end
