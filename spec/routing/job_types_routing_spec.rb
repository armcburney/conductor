require "rails_helper"

RSpec.describe JobTypesController, type: :routing do
  describe "routing" do

    it "routes to #index" do
      expect(:get => "/job_types").to route_to("job_types#index")
    end

    it "routes to #new" do
      expect(:get => "/job_types/new").to route_to("job_types#new")
    end

    it "routes to #show" do
      expect(:get => "/job_types/1").to route_to("job_types#show", :id => "1")
    end

    it "routes to #edit" do
      expect(:get => "/job_types/1/edit").to route_to("job_types#edit", :id => "1")
    end

    it "routes to #create" do
      expect(:post => "/job_types").to route_to("job_types#create")
    end

    it "routes to #update via PUT" do
      expect(:put => "/job_types/1").to route_to("job_types#update", :id => "1")
    end

    it "routes to #update via PATCH" do
      expect(:patch => "/job_types/1").to route_to("job_types#update", :id => "1")
    end

    it "routes to #destroy" do
      expect(:delete => "/job_types/1").to route_to("job_types#destroy", :id => "1")
    end

  end
end
