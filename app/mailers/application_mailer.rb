# frozen_string_literal: true

class ApplicationMailer < ActionMailer::Base
  default from: "andrewrobertmcburney@gmail.com"
  layout "mailer"
end
