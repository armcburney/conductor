# frozen_string_literal: true

source "https://rubygems.org"

git_source(:github) do |repo_name|
  repo_name = "#{repo_name}/#{repo_name}" unless repo_name.include?("/")
  "https://github.com/#{repo_name}.git"
end

ruby "2.4.1"

gem "coffee-rails"
gem "devise"
gem "dotenv-rails"
gem "faye-websocket", "0.10.0"
gem "friendly_id", "~> 5.1.0"
gem "jbuilder", "~> 2.5"
gem "jquery-rails"
gem "pg", "~> 0.21.0"
gem "puma", "~> 3.0"
gem "rails", "~> 5.0.2"
gem "sass-rails", "~> 5.0"
gem "sidekiq"
gem "slim-rails", "~> 3.1"
gem "uglifier", ">= 1.3.0"
gem "webpacker"
gem "websocket-rails", github: "moaa/websocket-rails", branch: "threadsocket-rails"
gem "websocket-rails-js", github: "websocket-rails/websocket-rails-js", branch: "sub_protocols"

group :development, :test do
  gem "byebug", platform: :mri
  gem "foreman"
  gem "rspec-rails", "~> 3.5"
end

group :development do
  gem "listen", "~> 3.0.5"
  gem "pry"
  gem "rubocop"
  gem "spring"
  gem "spring-watcher-listen", "~> 2.0.0"
  gem "web-console", ">= 3.3.0"
end
