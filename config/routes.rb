# frozen_string_literal: true

Rails.application.routes.draw do
  resources :event_actions
  resources :event_receivers
  resources :workers
  resources :jobs
  resources :job_types
  resources :users
  get  "home/index"
  root "home#index"
end
