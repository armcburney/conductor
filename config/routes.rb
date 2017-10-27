# frozen_string_literal: true

Rails.application.routes.draw do
  devise_for :users, controllers: {
    sessions: 'users/sessions'
  }
  resources :event_actions

  resources :event_receivers
  # Use the same controller for the Eventreceiver subtypes
  resources :scheduled_receivers, controller: :event_receivers
  resources :interval_receivers, controller: :event_receivers
  resources :regex_receivers, controller: :event_receivers
  resources :return_code_receivers, controller: :event_receivers
  resources :timeout_receivers, controller: :event_receivers

  resources :workers
  resources :jobs
  resources :job_types
  resources :api_keys
  get  "home/index"
  root "home#index"
end
