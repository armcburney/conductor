require "rails_helper"

RSpec.describe EventReceiversController, type: :routing do
  describe "routing" do

    it "routes to #index" do
      expect(:get => "/event_receivers").to route_to("event_receivers#index")
    end

    it "routes to #new" do
      expect(:get => "/event_receivers/new").to route_to("event_receivers#new")
    end

    it "routes to #show" do
      expect(:get => "/event_receivers/1").to route_to("event_receivers#show", :id => "1")
    end

    it "routes to #edit" do
      expect(:get => "/event_receivers/1/edit").to route_to("event_receivers#edit", :id => "1")
    end

    it "routes to #create" do
      expect(:post => "/event_receivers").to route_to("event_receivers#create")
    end

    it "routes to #update via PUT" do
      expect(:put => "/event_receivers/1").to route_to("event_receivers#update", :id => "1")
    end

    it "routes to #update via PATCH" do
      expect(:patch => "/event_receivers/1").to route_to("event_receivers#update", :id => "1")
    end

    it "routes to #destroy" do
      expect(:delete => "/event_receivers/1").to route_to("event_receivers#destroy", :id => "1")
    end

  end
end
