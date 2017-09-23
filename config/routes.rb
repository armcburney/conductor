# frozen_string_literal: true

Rails.application.routes.draw do
  devise_for :users, controllers: {
    sessions: 'users/sessions'
  }
  resources :event_actions
  resources :event_receivers
  resources :workers
  resources :jobs
  resources :job_types
  get  "home/index"
  root "home#index"
end
